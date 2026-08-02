import logging
from collections.abc import Callable

import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)

from config.config import ASSET_CLASS_OPTIONS, DEFAULT_REBALANCE_THRESHOLD_PCT
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
    decode_prefs,
    encode_prefs,
)

_DARK_CSS = """
<style>
    .stApp {
        background-color: #0f1419;
        color: #e7ecf1;
    }
    [data-testid="stSidebar"] {
        background-color: #151b23;
        border-right: 1px solid #243041;
    }
    [data-testid="stSidebar"] * {
        color: #e7ecf1;
    }
    h1, h2, h3 {
        color: #f3f6f9 !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }
    .main-subtitle {
        color: #8b9bb0;
        font-size: 0.95rem;
        margin-top: -0.5rem;
        margin-bottom: 1.25rem;
    }
    .empty-state {
        border: 1px dashed #2a3a4d;
        border-radius: 12px;
        padding: 2rem 1.5rem;
        text-align: center;
        color: #9aabbf;
        background: #121820;
        margin: 1rem 0 1.5rem 0;
    }
    .empty-state strong {
        color: #e7ecf1;
    }
    div[data-testid="stMetric"] {
        background: #151b23;
        border: 1px solid #243041;
        border-radius: 10px;
        padding: 0.75rem 1rem;
    }
    .block-container {
        padding-top: 1.5rem;
        max-width: 1100px;
    }
    .legal-note {
        color: #8b9bb0;
        font-size: 0.85rem;
        border-top: 1px solid #243041;
        padding-top: 1rem;
        margin-top: 2rem;
    }
</style>
"""


def apply_theme():
    st.markdown(_DARK_CSS, unsafe_allow_html=True)


def render_header(title: str, icon: str):
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    apply_theme()
    st.markdown(f"# {title}")
    st.markdown(
        '<p class="main-subtitle">Análise técnica, dividendos e alocação — uso educacional</p>',
        unsafe_allow_html=True,
    )


def render_empty_state():
    st.markdown(
        """
        <div class="empty-state">
            <strong>Comece pela barra lateral</strong><br/>
            1. Ajuste classes, universo, estratégia e capital<br/>
            2. Informe ou importe a carteira atual (opcional)<br/>
            3. Clique em <strong>Gerar carteira recomendada</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _hydrate_prefs_once():
    """SPEC-013: carrega preferências da URL (query params) uma vez por sessão."""
    if st.session_state.get("_prefs_hydrated"):
        return
    st.session_state._prefs_hydrated = True
    token = None
    try:
        token = st.query_params.get(QUERY_KEY)
    except Exception:
        logger.debug("query_params indisponível no hydrate", exc_info=True)
        token = None
    prefs = decode_prefs(token) if token else None
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
    st.session_state.pref_portfolio_mode = prefs.get(
        "portfolio_mode", "Valor atual (R$)"
    )
    st.session_state.pref_rebalance_threshold_pct = float(
        prefs.get("rebalance_threshold_pct", DEFAULT_REBALANCE_THRESHOLD_PCT)
    )


def _save_prefs_to_query(
    asset_classes,
    universe,
    strategy,
    capital,
    portfolio_mode,
    portfolio_text,
    rebalance_threshold_pct,
):
    prefs = {
        "portfolio_text": portfolio_text or "",
        "asset_classes": list(asset_classes or []),
        "universe": universe,
        "strategy": strategy,
        "capital": float(capital),
        "portfolio_mode": portfolio_mode,
        "rebalance_threshold_pct": float(rebalance_threshold_pct),
    }
    try:
        st.query_params[QUERY_KEY] = encode_prefs(prefs)
    except Exception:
        logger.debug("Falha ao gravar preferências na URL", exc_info=True)


def _clear_saved_prefs():
    try:
        if QUERY_KEY in st.query_params:
            del st.query_params[QUERY_KEY]
    except Exception:
        logger.debug("Falha ao limpar query_params", exc_info=True)
    st.session_state.portfolio_text = DEFAULT_PORTFOLIO_TEXT
    st.session_state.pref_asset_classes = list(DEFAULT_PREFS["asset_classes"])
    st.session_state.pref_universe = DEFAULT_PREFS["universe"]
    st.session_state.pref_strategy = DEFAULT_PREFS["strategy"]
    st.session_state.pref_capital = DEFAULT_PREFS["capital"]
    st.session_state.pref_portfolio_mode = DEFAULT_PREFS["portfolio_mode"]
    st.session_state.pref_rebalance_threshold_pct = DEFAULT_PREFS["rebalance_threshold_pct"]
    st.session_state._prefs_hydrated = True


def render_sidebar():
    _hydrate_prefs_once()
    if "portfolio_text" not in st.session_state:
        st.session_state.portfolio_text = DEFAULT_PORTFOLIO_TEXT

    with st.sidebar:
        st.markdown("### Configuração")

        with st.expander("Essencial", expanded=True):
            default_classes = st.session_state.get("pref_asset_classes", ["Ações", "FIIs"])
            asset_classes = st.multiselect(
                "Classes de ativos",
                ASSET_CLASS_OPTIONS,
                default=default_classes,
                help="BDRs: recibos B3. Cripto: BTC-USD ou atalhos BTC, ETH, SOL.",
            )
            universe_opts = ["Nacional", "Internacional", "Ambos"]
            uni = st.session_state.get("pref_universe", "Nacional")
            universe = st.radio(
                "Universo",
                universe_opts,
                index=universe_opts.index(uni) if uni in universe_opts else 0,
                horizontal=True,
            )
            strategy_opts = ["Growth", "Equilíbrio", "Dividendos"]
            strat = st.session_state.get("pref_strategy", "Equilíbrio")
            strategy = st.select_slider(
                "Estratégia",
                options=strategy_opts,
                value=strat if strat in strategy_opts else "Equilíbrio",
            )
            capital = st.number_input(
                "Novo aporte (R$)",
                min_value=100.0,
                value=float(st.session_state.get("pref_capital", 10000.0)),
                step=100.0,
            )

        with st.expander("Carteira atual", expanded=False):
            mode_opts = ["Valor atual (R$)", "Quantidade de cotas/unidades"]
            pm = st.session_state.get("pref_portfolio_mode", mode_opts[0])
            portfolio_mode = st.selectbox(
                "Formato",
                mode_opts,
                index=mode_opts.index(pm) if pm in mode_opts else 0,
            )
            uploaded = st.file_uploader(
                "Importar CSV ou TXT",
                type=["csv", "txt"],
                help="Substitui a carteira atual se houver linhas válidas.",
            )
            if uploaded is not None:
                file_id = f"{uploaded.name}:{getattr(uploaded, 'size', len(uploaded.getvalue()))}"
                if st.session_state.get("_last_import_id") != file_id:
                    raw = uploaded.getvalue()
                    result = import_portfolio_file(uploaded.name, raw)
                    st.session_state._last_import_id = file_id
                    if result.imported_count > 0:
                        st.session_state.portfolio_text = result.text
                        st.session_state._import_feedback = (
                            "ok",
                            f"Importadas {result.imported_count} posições"
                            + (f" ({result.skipped_count} ignoradas)" if result.skipped_count else ""),
                        )
                    else:
                        st.session_state._import_feedback = (
                            "warn",
                            "Nenhuma linha válida — carteira anterior preservada."
                            + (
                                f" Motivos: {'; '.join(result.skip_reasons[:3])}"
                                if result.skip_reasons
                                else ""
                            ),
                        )
                feedback = st.session_state.get("_import_feedback")
                if feedback:
                    kind, msg = feedback
                    if kind == "ok":
                        st.success(msg)
                    else:
                        st.warning(msg)

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
                help="Formato: TICKER, VALOR ou TICKER, QUANTIDADE. Cripto: BTC ou BTC-USD.",
            )

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
                help="Só mostra no plano de rebalance ações com |delta|/patrimônio_alvo ≥ este %.",
            )
            run_ai = st.checkbox(
                "Rodar análise IA",
                value=False,
                help="Requer provedor configurado (GROQ_API_KEY ou OPENAI_BASE_URL).",
            )
            ai_password = ""
            llm_provider = None
            llm_model = None
            if run_ai:
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
                    st.caption("Chave detectada para este provedor.")
                ai_password = st.text_input(
                    "Senha de acesso IA",
                    type="password",
                    help="Necessária se o administrador configurou proteção.",
                )

            max_ai_assets = st.slider(
                "Limite de ativos para IA",
                min_value=1,
                max_value=30,
                value=5,
                step=1,
            )
            max_portfolio_assets = st.slider(
                "Máximo de ativos na carteira alvo",
                min_value=3,
                max_value=20,
                value=10,
                step=1,
            )

        with st.expander("Preferências salvas", expanded=False):
            st.caption("Preferências e carteira neste navegador (URL). Sem senhas nem API keys.")
            if st.button("Salvar neste navegador"):
                _save_prefs_to_query(
                    asset_classes,
                    universe,
                    strategy,
                    capital,
                    portfolio_mode,
                    current_portfolio_text,
                    rebalance_threshold_pct,
                )
                st.success("Preferências salvas na URL deste navegador.")
            if st.button("Limpar dados salvos"):
                _clear_saved_prefs()
                st.success("Dados salvos limpos. Recarregue se os widgets não atualizarem.")
                st.rerun()

    return (
        asset_classes,
        universe,
        strategy,
        capital,
        period,
        run_ai,
        max_ai_assets,
        portfolio_mode,
        current_portfolio_text,
        max_portfolio_assets,
        ai_password,
        llm_provider,
        llm_model,
        rebalance_threshold_pct,
    )


def display_summary_metrics(
    asset_count: int,
    current_total: float,
    new_investment: float,
    target_total: float,
):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ativos na carteira", f"{asset_count}")
    c2.metric("Carteira atual", f"R$ {current_total:,.0f}")
    c3.metric("Aporte", f"R$ {new_investment:,.0f}")
    c4.metric("Carteira alvo", f"R$ {target_total:,.0f}")


def _price_label(asset) -> str:
    if (getattr(asset, "asset_class", "") or "") == "Cripto" or (
        getattr(asset, "market", "") or ""
    ).upper() == "CRYPTO":
        return f"USD {asset.current_price:,.2f}"
    return f"{asset.current_price:.2f}"


def display_portfolio(portfolio):
    if not portfolio:
        st.warning("Nenhum ativo qualificado encontrado para os critérios selecionados.")
        return

    has_crypto = any(
        (getattr(p, "asset_class", "") or "") == "Cripto"
        or (getattr(p, "market", "") or "").upper() == "CRYPTO"
        for p in portfolio
    )
    if has_crypto:
        st.caption(
            "Preços de cripto em USD. Valores de alocação/aporte são unidade de simulação "
            "e podem misturar moedas se a carteira tiver ativos multi-mercado."
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
                "Preço": _price_label(p),
            }
        )

    st.subheader("Carteira recomendada")
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

    if len(data) > 0:
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
):
    st.subheader("Plano de rebalanceamento")
    st.caption(
        f"Atual: R$ {current_total:,.2f} · Aporte: R$ {new_investment:,.2f} · "
        f"Alvo: R$ {target_total:,.2f}"
        + (f" · Limiar: {threshold_pct:g}%" if threshold_pct and threshold_pct > 0 else "")
    )

    if not actions:
        if threshold_pct and threshold_pct > 0:
            st.info(
                f"Nenhuma ação acima do limiar de {threshold_pct:g}% "
                "(desvio em relação ao patrimônio alvo)."
            )
        else:
            st.info("Sem ajustes relevantes para rebalanceamento no momento.")
        return

    rows = []
    for item in actions:
        rows.append(
            {
                "Ticker": item["ticker"],
                "Ação": item["action"],
                "Valor atual (R$)": f"R$ {item['current_value']:,.2f}",
                "Valor alvo (R$)": f"R$ {item['target_value']:,.2f}",
                "Ajuste (R$)": f"R$ {item['delta_value']:,.2f}",
                "Desvio %": f"{float(item.get('deviation_pct', 0.0)):.2f}%",
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
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
):
    st.subheader("Como deve ficar")
    st.caption(
        f"Atual: R$ {current_total:,.2f} · Aporte: R$ {new_investment:,.2f} · "
        f"Projetado: R$ {target_total:,.2f}"
    )

    if not rows:
        st.info("Sem projeção disponível nesta rodada.")
        return

    table = []
    for item in rows:
        table.append(
            {
                "Ticker": item["ticker"],
                "Atual (R$)": f"R$ {item['current_value']:,.2f}",
                "Projetado (R$)": f"R$ {item['projected_value']:,.2f}",
                "% projetado": f"{item['projected_pct']:.1f}%",
                "Variação (R$)": f"R$ {item['delta_value']:,.2f}",
                "Status": item["status"],
            }
        )
    st.dataframe(pd.DataFrame(table), use_container_width=True, hide_index=True)

    if on_apply is not None and st.button("Aplicar na carteira atual", type="secondary"):
        on_apply()


def render_disclaimer():
    st.markdown(
        """
        <div class="legal-note">
        <strong>Aviso legal.</strong> Ferramenta de finalidade estritamente educacional.
        Os dados não constituem recomendação de compra ou venda. Rentabilidade passada
        não garante resultados futuros. Consulte um profissional certificado antes de investir.
        </div>
        """,
        unsafe_allow_html=True,
    )
