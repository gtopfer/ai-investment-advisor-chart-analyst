"""UI Streamlit — sidebar e resultados (SPEC-024 fachada)."""

from __future__ import annotations

import logging
from collections.abc import Callable

import pandas as pd
import streamlit as st

from config.config import (
    ASSET_CLASS_OPTIONS,
    DEFAULT_BASE_CURRENCY,
    DEFAULT_REBALANCE_THRESHOLD_PCT,
    STRATEGY_WEIGHTS,
)
from llm.registry import (
    default_model_for,
    get_enabled_providers,
    resolve_default_provider_id,
)
from portfolio.export_csv import portfolio_target_to_csv, rebalance_actions_to_csv
from portfolio.import_portfolio import PORTFOLIO_CSV_TEMPLATE, import_portfolio_file
from portfolio.persistence import (
    DEFAULT_PORTFOLIO_TEXT,
    DEFAULT_PREFS,
    QUERY_KEY,
    clear_prefs_file,
    decode_prefs,
    encode_prefs,
    load_prefs_file,
    save_prefs_file,
)
from ui.i18n import t
from ui.theme import dark_css

logger = logging.getLogger(__name__)


def apply_theme():
    st.markdown(dark_css(), unsafe_allow_html=True)


def render_header(title: str, icon: str, lang: str = "pt"):
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    apply_theme()
    st.markdown(f"# {title}")
    st.markdown(
        f'<p class="main-subtitle">{t("subtitle", lang)}</p>',
        unsafe_allow_html=True,
    )


def render_empty_state(lang: str = "pt"):
    st.markdown(
        f"""
        <div class="empty-state">
            <strong>{t("empty_title", lang)}</strong><br/>
            {t("empty_steps", lang)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _hydrate_prefs_once():
    if st.session_state.get("_prefs_hydrated"):
        return
    st.session_state._prefs_hydrated = True
    prefs = load_prefs_file()
    token = None
    try:
        token = st.query_params.get(QUERY_KEY)
    except Exception:
        logger.debug("query_params hydrate", exc_info=True)
    if not prefs and token:
        prefs = decode_prefs(token)
    if not prefs:
        prefs = dict(DEFAULT_PREFS)

    if "portfolio_text" not in st.session_state:
        st.session_state.portfolio_text = prefs.get("portfolio_text", DEFAULT_PORTFOLIO_TEXT)
    st.session_state.pref_asset_classes = [
        c for c in prefs.get("asset_classes", ["Ações", "FIIs"]) if c in ASSET_CLASS_OPTIONS
    ] or ["Ações", "FIIs"]
    st.session_state.pref_universe = prefs.get("universe", "Nacional")
    st.session_state.pref_strategy = prefs.get("strategy", "Equilíbrio")
    st.session_state.pref_capital = float(prefs.get("capital", 10000.0))
    st.session_state.pref_portfolio_mode = prefs.get("portfolio_mode", "Valor atual (R$)")
    st.session_state.pref_rebalance_threshold_pct = float(
        prefs.get("rebalance_threshold_pct", DEFAULT_REBALANCE_THRESHOLD_PCT)
    )
    st.session_state.pref_base_currency = prefs.get("base_currency", DEFAULT_BASE_CURRENCY)
    st.session_state.pref_extra_tickers = prefs.get("extra_tickers", "")
    st.session_state.pref_watchlist = prefs.get("watchlist") or []
    st.session_state.pref_lang = prefs.get("lang", "pt")


def _prefs_payload(
    asset_classes,
    universe,
    strategy,
    capital,
    portfolio_mode,
    portfolio_text,
    rebalance_threshold_pct,
    base_currency,
    extra_tickers,
    watchlist,
    lang,
):
    return {
        "portfolio_text": portfolio_text or "",
        "asset_classes": list(asset_classes or []),
        "universe": universe,
        "strategy": strategy,
        "capital": float(capital),
        "portfolio_mode": portfolio_mode,
        "rebalance_threshold_pct": float(rebalance_threshold_pct),
        "base_currency": base_currency,
        "extra_tickers": extra_tickers or "",
        "watchlist": list(watchlist or []),
        "lang": lang,
    }


def render_sidebar():
    _hydrate_prefs_once()
    if "portfolio_text" not in st.session_state:
        st.session_state.portfolio_text = DEFAULT_PORTFOLIO_TEXT

    lang = st.session_state.get("pref_lang", "pt")

    with st.sidebar:
        st.markdown("### Configuração")
        lang = st.selectbox(
            "Idioma / Language",
            ["pt", "en"],
            index=0 if lang != "en" else 1,
        )
        st.session_state.pref_lang = lang

        with st.expander("Essencial", expanded=True):
            default_classes = st.session_state.get("pref_asset_classes", ["Ações", "FIIs"])
            asset_classes = st.multiselect(
                "Classes de ativos",
                ASSET_CLASS_OPTIONS,
                default=default_classes,
                help="BDRs: B3. Cripto: BTC-USD ou atalhos.",
            )
            universe_opts = ["Nacional", "Internacional", "Ambos"]
            uni = st.session_state.get("pref_universe", "Nacional")
            universe = st.radio(
                "Universo",
                universe_opts,
                index=universe_opts.index(uni) if uni in universe_opts else 0,
                horizontal=True,
            )
            strategy_opts = list(STRATEGY_WEIGHTS.keys())
            strat = st.session_state.get("pref_strategy", "Equilíbrio")
            strategy = st.select_slider(
                "Estratégia",
                options=strategy_opts,
                value=strat if strat in strategy_opts else "Equilíbrio",
            )
            capital = st.number_input(
                "Novo aporte (moeda-base)",
                min_value=100.0,
                value=float(st.session_state.get("pref_capital", 10000.0)),
                step=100.0,
            )
            base_currency = st.selectbox(
                "Moeda-base",
                ["BRL", "USD"],
                index=0
                if st.session_state.get("pref_base_currency", "BRL") == "BRL"
                else 1,
                help="Totais e rebalance convertidos para esta moeda (SPEC-016).",
            )

        with st.expander("Carteira atual", expanded=False):
            mode_opts = ["Valor atual (R$)", "Quantidade de cotas/unidades"]
            # label: valores já na moeda-base
            mode_opts = ["Valor na moeda-base", "Quantidade de cotas/unidades"]
            pm = st.session_state.get("pref_portfolio_mode", mode_opts[0])
            # migrate old label
            if pm == "Valor atual (R$)":
                pm = mode_opts[0]
            portfolio_mode = st.selectbox(
                "Formato",
                mode_opts,
                index=mode_opts.index(pm) if pm in mode_opts else 0,
            )
            uploaded = st.file_uploader(
                "Importar CSV ou TXT",
                type=["csv", "txt"],
            )
            if uploaded is not None:
                file_id = f"{uploaded.name}:{getattr(uploaded, 'size', len(uploaded.getvalue()))}"
                if st.session_state.get("_last_import_id") != file_id:
                    result = import_portfolio_file(uploaded.name, uploaded.getvalue())
                    st.session_state._last_import_id = file_id
                    if result.imported_count > 0:
                        st.session_state.portfolio_text = result.text
                        st.success(f"Importadas {result.imported_count} posições")
                    else:
                        st.warning("Nenhuma linha válida — carteira anterior preservada.")

            st.download_button(
                "Baixar modelo CSV",
                data=PORTFOLIO_CSV_TEMPLATE,
                file_name="carteira_modelo.csv",
                mime="text/csv",
            )
            current_portfolio_text = st.text_area(
                "Posições (uma por linha)",
                key="portfolio_text",
                height=120,
            )
            extra_tickers_raw = st.text_area(
                "Tickers extras (universo)",
                value=st.session_state.get("pref_extra_tickers", ""),
                height=80,
                help="Um por linha ou separados por vírgula (SPEC-017).",
            )
            watchlist_raw = st.text_area(
                "Watchlist",
                value="\n".join(st.session_state.get("pref_watchlist") or []),
                height=60,
                help="Alertas RSI/DY (SPEC-030).",
            )
            watchlist = [
                x.strip().upper()
                for x in watchlist_raw.replace(",", "\n").splitlines()
                if x.strip()
            ]

        with st.expander("Avançado", expanded=False):
            period = st.selectbox("Período de análise", ["6mo", "1y", "2y", "5y"], index=1)
            rebalance_threshold_pct = st.slider(
                "Ignorar desvios menores que (%)",
                min_value=0.0,
                max_value=20.0,
                value=float(
                    st.session_state.get(
                        "pref_rebalance_threshold_pct", DEFAULT_REBALANCE_THRESHOLD_PCT
                    )
                ),
                step=0.5,
            )
            quick_mode = st.checkbox(
                "Modo rápido (sem IA / dividendos leves)",
                value=False,
            )
            compare_strats = st.checkbox("Comparar estratégias", value=False)
            run_ai = st.checkbox("Rodar análise IA", value=False, disabled=quick_mode)
            ai_password = ""
            llm_provider = None
            llm_model = None
            if run_ai and not quick_mode:
                enabled = get_enabled_providers()
                if not enabled:
                    st.caption("Nenhum provedor com credenciais detectadas.")
                else:
                    default_id = resolve_default_provider_id(enabled) or enabled[0].provider_id
                    labels = {p.provider_id: p.display_name for p in enabled}
                    ids = [p.provider_id for p in enabled]
                    try:
                        default_index = ids.index(default_id)
                    except ValueError:
                        default_index = 0
                    llm_provider = st.selectbox(
                        "Provedor",
                        options=ids,
                        format_func=lambda x: labels.get(x, x),
                        index=default_index,
                    )
                    model_key = f"llm_model_{llm_provider}"
                    if model_key not in st.session_state:
                        st.session_state[model_key] = default_model_for(llm_provider)
                    llm_model = st.text_input("Modelo", key=model_key)
                ai_password = st.text_input("Senha de acesso IA", type="password")

            max_ai_assets = st.slider("Limite de ativos para IA", 1, 30, 5, 1)
            max_portfolio_assets = st.slider("Máximo de ativos na carteira alvo", 3, 20, 10, 1)

            st.markdown("**Pesos do score** (estratégia atual)")
            defaults = STRATEGY_WEIGHTS.get(strategy, STRATEGY_WEIGHTS["Equilíbrio"])
            w_tech = st.slider(
                "Peso técnico",
                0.0,
                1.0,
                float(defaults["technical"]),
                0.05,
            )
            w_div = st.slider(
                "Peso dividendos",
                0.0,
                1.0,
                float(defaults["dividend"]),
                0.05,
            )
            s = w_tech + w_div
            score_weights = {
                "technical": w_tech / s if s > 0 else 0.5,
                "dividend": w_div / s if s > 0 else 0.5,
            }

            st.markdown("**Metas % por classe** (opcional, soma 100)")
            use_targets = st.checkbox("Usar metas por classe", value=False)
            class_targets = None
            if use_targets and asset_classes:
                class_targets = {}
                for cls in asset_classes:
                    class_targets[cls] = st.number_input(
                        f"% {cls}",
                        min_value=0.0,
                        max_value=100.0,
                        value=round(100.0 / len(asset_classes), 1),
                        step=1.0,
                        key=f"tgt_{cls}",
                    )
                tot = sum(class_targets.values()) or 1.0
                class_targets = {k: v / tot for k, v in class_targets.items()}

        with st.expander("Preferências salvas", expanded=False):
            st.caption("Arquivo local (~/.ai_investment_advisor) + URL opcional. Sem senhas.")
            if st.button("Salvar neste navegador/máquina"):
                payload = _prefs_payload(
                    asset_classes,
                    universe,
                    strategy,
                    capital,
                    portfolio_mode,
                    current_portfolio_text,
                    rebalance_threshold_pct,
                    base_currency,
                    extra_tickers_raw,
                    watchlist,
                    lang,
                )
                save_prefs_file(payload)
                try:
                    st.query_params[QUERY_KEY] = encode_prefs(payload)
                except Exception:
                    logger.debug("save url", exc_info=True)
                st.success("Preferências salvas.")
            if st.button("Limpar dados salvos"):
                clear_prefs_file()
                try:
                    if QUERY_KEY in st.query_params:
                        del st.query_params[QUERY_KEY]
                except Exception:
                    logger.debug("clear query prefs", exc_info=True)
                st.session_state.portfolio_text = DEFAULT_PORTFOLIO_TEXT
                st.session_state._prefs_hydrated = False
                st.rerun()

    # Compat: modo antigo de valor
    if portfolio_mode == "Valor na moeda-base":
        portfolio_mode_internal = "Valor atual (R$)"
    else:
        portfolio_mode_internal = portfolio_mode

    return (
        asset_classes,
        universe,
        strategy,
        capital,
        period,
        run_ai and not quick_mode,
        max_ai_assets,
        portfolio_mode_internal,
        current_portfolio_text,
        max_portfolio_assets,
        ai_password,
        llm_provider,
        llm_model,
        rebalance_threshold_pct,
        base_currency,
        extra_tickers_raw,
        quick_mode,
        score_weights,
        class_targets,
        watchlist,
        compare_strats,
        lang,
    )


def display_summary_metrics(
    asset_count: int,
    current_total: float,
    new_investment: float,
    target_total: float,
    currency_label: str = "R$",
):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ativos na carteira", f"{asset_count}")
    c2.metric("Carteira atual", f"{currency_label} {current_total:,.0f}")
    c3.metric("Aporte", f"{currency_label} {new_investment:,.0f}")
    c4.metric("Carteira alvo", f"{currency_label} {target_total:,.0f}")


def _price_label(asset, currency_label: str = "R$") -> str:
    if getattr(asset, "price_in_base", 0):
        return f"{currency_label} {asset.price_in_base:,.2f}"
    if (getattr(asset, "asset_class", "") or "") == "Cripto" or (
        getattr(asset, "market", "") or ""
    ).upper() == "CRYPTO":
        return f"USD {asset.current_price:,.2f}"
    return f"{asset.current_price:.2f}"


def display_portfolio(portfolio, currency_label: str = "R$"):
    if not portfolio:
        st.warning(
            "Nenhum ativo qualificado. Amplie classes, adicione tickers extras "
            "ou reduza filtros."
        )
        return

    has_crypto = any(
        (getattr(p, "asset_class", "") or "") == "Cripto"
        or (getattr(p, "market", "") or "").upper() == "CRYPTO"
        for p in portfolio
    )
    if has_crypto:
        st.caption(
            f"Valores de alocação em {currency_label} (moeda-base). "
            "Preços nativos de cripto podem ser USD antes da conversão."
        )

    data = []
    for p in portfolio:
        data.append(
            {
                "Ticker": p.ticker,
                "Classe": p.asset_class,
                "Recomendação": p.recommendation,
                "Score": f"{p.total_score:.2f}",
                "Alocação %": f"{p.suggested_allocation_pct:.1f}%",
                "Valor simulado": f"{p.suggested_value:,.2f}",
                "Motivo": p.reason,
                "Preço (base)": _price_label(p, currency_label),
            }
        )

    st.subheader("Carteira recomendada")
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    if data:
        st.download_button(
            "Baixar carteira alvo (CSV)",
            data=portfolio_target_to_csv(portfolio),
            file_name="carteira_alvo.csv",
            mime="text/csv",
            key="dl_portfolio_target",
        )
        st.subheader("Distribuição de alocação")
        chart_data = pd.DataFrame(
            {
                "Ticker": [p.ticker for p in portfolio],
                "Alocação": [p.suggested_allocation_pct for p in portfolio],
            }
        )
        st.bar_chart(chart_data.set_index("Ticker"))


def display_rebalance_plan(
    actions,
    current_total: float,
    new_investment: float,
    target_total: float,
    threshold_pct: float = 0.0,
    currency_label: str = "R$",
):
    st.subheader("Plano de rebalanceamento")
    st.caption(
        f"Atual: {currency_label} {current_total:,.2f} · Aporte: {currency_label} {new_investment:,.2f} · "
        f"Alvo: {currency_label} {target_total:,.2f}"
        + (f" · Limiar: {threshold_pct:g}%" if threshold_pct and threshold_pct > 0 else "")
    )

    if not actions:
        if threshold_pct and threshold_pct > 0:
            st.info(
                f"Nenhuma ação acima do limiar de {threshold_pct:g}%. "
                "Abaixe o limiar na sidebar ou ajuste a carteira."
            )
        else:
            st.info("Sem ajustes relevantes para rebalanceamento no momento.")
        return

    rows = []
    total_cost = 0.0
    for item in actions:
        total_cost += float(item.get("cost_est") or 0)
        rows.append(
            {
                "Ticker": item["ticker"],
                "Ação": item["action"],
                f"Atual ({currency_label})": f"{item['current_value']:,.2f}",
                f"Alvo ({currency_label})": f"{item['target_value']:,.2f}",
                f"Ajuste ({currency_label})": f"{item['delta_value']:,.2f}",
                "Desvio %": f"{float(item.get('deviation_pct', 0.0)):.2f}%",
                "Custo est.": f"{float(item.get('cost_est', 0.0)):.2f}",
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.caption(
        f"Custo estimado total (corretagem/IR educacional): {currency_label} {total_cost:,.2f}. "
        "Não é cálculo fiscal oficial."
    )
    st.download_button(
        "Baixar plano de rebalance (CSV)",
        data=rebalance_actions_to_csv(actions),
        file_name="plano_rebalance.csv",
        mime="text/csv",
        key="dl_rebalance_plan",
    )


def display_projected_portfolio(
    rows: list[dict],
    current_total: float,
    new_investment: float,
    target_total: float,
    on_apply: Callable[[], None] | None = None,
    currency_label: str = "R$",
):
    st.subheader("Como deve ficar")
    st.caption(
        f"Atual: {currency_label} {current_total:,.2f} · Aporte: {currency_label} {new_investment:,.2f} · "
        f"Projetado: {currency_label} {target_total:,.2f}"
    )
    if not rows:
        st.info("Sem projeção disponível nesta rodada.")
        return
    table = []
    for item in rows:
        table.append(
            {
                "Ticker": item["ticker"],
                "Atual": f"{item['current_value']:,.2f}",
                "Projetado": f"{item['projected_value']:,.2f}",
                "% projetado": f"{item['projected_pct']:.1f}%",
                "Variação": f"{item['delta_value']:,.2f}",
                "Status": item["status"],
            }
        )
    st.dataframe(pd.DataFrame(table), use_container_width=True, hide_index=True)
    if on_apply is not None and st.button("Aplicar na carteira atual", type="secondary"):
        on_apply()


def display_strategy_comparison(comparison: dict):
    st.subheader("Comparação de estratégias")
    cols = st.columns(max(1, len(comparison)))
    for i, (strat, assets) in enumerate(comparison.items()):
        with cols[i % len(cols)]:
            st.markdown(f"**{strat}**")
            if not assets:
                st.caption("Sem alocação")
                continue
            lines = [
                f"{a.ticker}: {a.suggested_allocation_pct:.1f}% ({a.suggested_value:,.0f})"
                for a in assets[:8]
            ]
            st.write("\n".join(lines))


def display_watchlist_alerts(alerts: list[dict]):
    st.subheader("Alertas da watchlist")
    for a in alerts:
        st.warning(a.get("message") or str(a))


def render_disclaimer(lang: str = "pt"):
    st.markdown(
        f"""
        <div class="legal-note">
        <strong>Disclaimer.</strong> {t("disclaimer", lang)}
        </div>
        """,
        unsafe_allow_html=True,
    )
