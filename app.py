import logging
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime

import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

from ducks.analysis import (
    analyze_chart_patterns,
    analyze_dividends,
    run_ai_technical_analysis,
)
from ducks.market import get_dividend_history, get_fundamentals, get_price_history
from ducks.portfolio import (
    QUERY_KEY,
    allocate_capital,
    build_candidate_tickers,
    build_projected_portfolio,
    build_rebalance_actions,
    classify_ticker,
    compare_strategies,
    encode_prefs,
    evaluate_alerts,
    format_positions_as_text,
    parse_current_portfolio,
    parse_extra_tickers,
    projected_positions_for_session,
    save_prefs_file,
    score_assets,
)
from ducks.ui import (
    display_portfolio,
    display_projected_portfolio,
    display_rebalance_plan,
    display_strategy_comparison,
    display_summary_metrics,
    display_watchlist_alerts,
    render_disclaimer,
    render_empty_state,
    render_header,
    render_sidebar,
)
from shared.config.config import (
    AI_ACCESS_PASSWORD,
    APP_ICON,
    APP_TITLE,
    DEFAULT_BASE_CURRENCY,
    DEFAULT_BROKERAGE_PCT,
    DEFAULT_IR_PCT,
    FETCH_MAX_WORKERS,
    LOG_LEVEL,
    MAX_AI_CALLS_PER_SESSION,
    RUN_HISTORY_MAX,
    STRATEGY_WEIGHTS,
)
from shared.models import AssetAnalysis
from shared.utils import (
    convert_amount,
    fetch_usd_brl_rate,
    normalize_currency,
    normalize_ticker,
)

logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper(), logging.INFO))
logger = logging.getLogger(__name__)


def convert_positions_to_value_map(
    positions: dict[str, float],
    portfolio_mode: str,
    analyzed_assets: list[AssetAnalysis],
    base_currency: str = "BRL",
    usd_brl: float = 5.0,
) -> dict[str, float]:
    """Converte posições em mapa de valor na moeda-base (SPEC-016)."""
    base = normalize_currency(base_currency)
    assets_by_ticker = {a.ticker: a for a in analyzed_assets}

    if portfolio_mode == "Valor atual (R$)":
        # Valores digitados tratados como já na moeda-base do seletor
        # (label UI indica base)
        return {t: float(v) for t, v in positions.items()}

    value_map: dict[str, float] = {}
    for ticker, qty in positions.items():
        asset = assets_by_ticker.get(ticker)
        if not asset:
            value_map[ticker] = 0.0
            continue
        native = float(asset.current_price) * float(qty)
        cur = asset.currency or ("BRL" if (asset.market or "") == "BR" else "USD")
        value_map[ticker] = convert_amount(native, cur, base, usd_brl)
    return value_map


def _process_single_ticker(
    ticker: str,
    period: str,
    base_currency: str,
    usd_brl: float,
    quick_mode: bool = False,
):
    ticker = normalize_ticker(ticker)
    price_df = get_price_history(ticker, period=period)
    fundamentals = get_fundamentals(ticker) or {}

    if price_df.empty and not fundamentals:
        return None

    current_price = fundamentals.get("current_price", 0.0)
    if current_price == 0.0 and not price_df.empty:
        current_price = float(price_df["Close"].iloc[-1])

    currency = normalize_currency(fundamentals.get("currency"))
    # BDRs/BR listados em BRL tipicamente
    asset_class, market = classify_ticker(ticker)
    if market == "BR" and currency == "USD" and ticker.endswith(".SA"):
        currency = "BRL"

    price_in_base = convert_amount(
        float(current_price), currency, base_currency, usd_brl
    )

    tech_indicators = analyze_chart_patterns(ticker, price_df)
    if quick_mode:
        from shared.models.schemas import DividendMetrics

        div_metrics = DividendMetrics(
            dy=0.0,
            dividend_score=0.0,
            stability_note="Histórico insuficiente",
            volatility_flag="medium",
            summary_pt="Modo rápido: dividendos não calculados.",
        )
    else:
        dividend_history = get_dividend_history(ticker)
        div_metrics = analyze_dividends(
            ticker,
            fundamentals,
            price_df,
            dividend_history,
            is_crypto=(asset_class == "Cripto" or market == "CRYPTO"),
        )

    closes: list[float] = []
    if not price_df.empty and "Close" in price_df.columns:
        closes = [float(x) for x in price_df["Close"].tail(120).tolist()]

    return AssetAnalysis(
        ticker=ticker,
        market=market,
        asset_class=asset_class,
        current_price=float(current_price),
        technical=tech_indicators,
        ai_analysis=None,
        dividends=div_metrics,
        currency=currency,
        price_in_base=price_in_base,
        close_series=closes,
    )


def _split_results(
    tickers: list[str],
    results: dict[str, AssetAnalysis | None],
) -> tuple[list[AssetAnalysis], list[str]]:
    analyzed_assets: list[AssetAnalysis] = []
    failed_tickers: list[str] = []
    for ticker in tickers:
        if results[ticker] is not None:
            analyzed_assets.append(results[ticker])
        else:
            failed_tickers.append(ticker)
    return analyzed_assets, failed_tickers


def _tickers_with_insufficient_history(assets: list[AssetAnalysis]) -> list[str]:
    return [
        a.ticker
        for a in assets
        if a.technical is not None and a.technical.insufficient_history
    ]


def analyze_assets(
    tickers: list[str],
    period: str,
    run_ai: bool,
    max_ai_assets: int,
    ai_password: str = "",
    progress_callback=None,
    llm_provider: str | None = None,
    llm_model: str | None = None,
    base_currency: str = DEFAULT_BASE_CURRENCY,
    usd_brl: float = 5.0,
    quick_mode: bool = False,
    phase_callback=None,
):
    if run_ai and not quick_mode:
        if AI_ACCESS_PASSWORD and ai_password != AI_ACCESS_PASSWORD:
            st.warning("Senha da IA incorreta. A análise com IA foi desativada para esta execução.")
            run_ai = False
        if "ai_calls_session" not in st.session_state:
            st.session_state.ai_calls_session = 0
        if st.session_state.ai_calls_session >= MAX_AI_CALLS_PER_SESSION:
            st.warning(
                f"Limite de chamadas IA por sessão ({MAX_AI_CALLS_PER_SESSION}) atingido. "
                "A análise com IA foi desativada."
            )
            run_ai = False
    else:
        run_ai = False if quick_mode else run_ai

    ai_calls = 0
    completed_count = 0
    results: dict[str, AssetAnalysis | None] = {ticker: None for ticker in tickers}
    ctx = get_script_run_ctx()
    workers = max(1, min(FETCH_MAX_WORKERS, 10))

    if phase_callback:
        phase_callback("coleta")

    def _process_with_context(ticker_arg, period_arg, run_ctx):
        if run_ctx:
            add_script_run_ctx(ctx=run_ctx)
        return _process_single_ticker(
            ticker_arg, period_arg, base_currency, usd_brl, quick_mode=quick_mode
        )

    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_ticker = {
            executor.submit(_process_with_context, ticker, period, ctx): ticker
            for ticker in tickers
        }
        for future in as_completed(future_to_ticker):
            completed_count += 1
            if progress_callback:
                progress_callback(completed_count - 1, len(tickers))
            ticker = future_to_ticker[future]
            try:
                asset = future.result()
                if asset:
                    results[ticker] = asset
            except Exception:
                logger.exception("Erro ao processar %s", ticker)
    fetch_ms = (time.perf_counter() - t0) * 1000

    analyzed_assets, failed_tickers = _split_results(tickers, results)

    if phase_callback:
        phase_callback("ia" if run_ai else "score")

    t1 = time.perf_counter()
    if run_ai:
        for asset in analyzed_assets:
            if (
                ai_calls >= max_ai_assets
                or st.session_state.ai_calls_session >= MAX_AI_CALLS_PER_SESSION
            ):
                break
            asset.ai_analysis = run_ai_technical_analysis(
                asset.ticker,
                asset.technical,
                provider_id=llm_provider,
                model=llm_model,
            )
            ai_calls += 1
            st.session_state.ai_calls_session += 1
    ai_ms = (time.perf_counter() - t1) * 1000

    return analyzed_assets, ai_calls, failed_tickers, fetch_ms, ai_ms


def process_portfolio(
    tickers: list[str],
    current_positions: dict[str, float],
    period: str,
    run_ai: bool,
    max_ai_assets: int,
    strategy: str,
    portfolio_mode: str,
    capital: float,
    max_portfolio_assets: int,
    ai_password: str = "",
    progress_callback=None,
    llm_provider: str | None = None,
    llm_model: str | None = None,
    rebalance_threshold_pct: float = 0.0,
    base_currency: str = "BRL",
    usd_brl: float = 5.0,
    fx_ok: bool = True,
    quick_mode: bool = False,
    score_weights: dict | None = None,
    class_targets: dict[str, float] | None = None,
    phase_callback=None,
):
    analyzed_assets, ai_calls, failed_tickers, fetch_ms, ai_ms = analyze_assets(
        tickers,
        period,
        run_ai,
        max_ai_assets,
        ai_password,
        progress_callback,
        llm_provider=llm_provider,
        llm_model=llm_model,
        base_currency=base_currency,
        usd_brl=usd_brl,
        quick_mode=quick_mode,
        phase_callback=phase_callback,
    )

    if phase_callback:
        phase_callback("score")
    t_score = time.perf_counter()
    scored_assets = score_assets(analyzed_assets, strategy, weights=score_weights)
    score_ms = (time.perf_counter() - t_score) * 1000

    current_value_map = convert_positions_to_value_map(
        current_positions,
        portfolio_mode,
        scored_assets,
        base_currency=base_currency,
        usd_brl=usd_brl,
    )
    current_total_value = sum(current_value_map.values())
    target_total_value = current_total_value + capital
    final_portfolio = allocate_capital(
        scored_assets,
        target_total_value,
        max_assets=max_portfolio_assets,
        class_targets=class_targets,
    )
    rebalance_actions = build_rebalance_actions(
        current_value_map,
        final_portfolio,
        threshold_pct=rebalance_threshold_pct,
        target_total=target_total_value,
        brokerage_pct=DEFAULT_BROKERAGE_PCT,
        ir_pct=DEFAULT_IR_PCT,
    )
    projected_rows = build_projected_portfolio(current_value_map, final_portfolio)
    short_history_tickers = _tickers_with_insufficient_history(scored_assets)

    return {
        "scored_assets": scored_assets,
        "final_portfolio": final_portfolio,
        "rebalance_actions": rebalance_actions,
        "projected_rows": projected_rows,
        "current_total_value": current_total_value,
        "target_total_value": target_total_value,
        "ai_calls": ai_calls,
        "failed_tickers": failed_tickers,
        "short_history_tickers": short_history_tickers,
        "fetch_ms": fetch_ms,
        "score_ms": score_ms,
        "ai_ms": ai_ms,
        "base_currency": base_currency,
        "usd_brl": usd_brl,
        "fx_ok": fx_ok,
    }


def _push_run_history(run: dict):
    hist = st.session_state.setdefault("run_history", [])
    hist.insert(0, run)
    del hist[RUN_HISTORY_MAX:]


def handle_generate_portfolio(
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
    ai_password="",
    llm_provider=None,
    llm_model=None,
    rebalance_threshold_pct=0.0,
    base_currency="BRL",
    extra_tickers_raw="",
    quick_mode=False,
    score_weights=None,
    class_targets=None,
    watchlist=None,
    compare_strats=False,
    lang="pt",
):
    run_id = str(uuid.uuid4())[:8]
    with st.spinner("Analisando mercado e processando dados..."):
        extras = parse_extra_tickers(extra_tickers_raw)
        tickers = build_candidate_tickers(asset_classes, universe, extra_tickers=extras)
        current_positions = parse_current_portfolio(current_portfolio_text)
        if current_positions:
            tickers = list(dict.fromkeys(tickers + list(current_positions.keys())))
        if watchlist:
            tickers = list(dict.fromkeys(tickers + list(watchlist)))

        if not tickers:
            st.error(
                "Nenhum ativo selecionado. Adicione classes, tickers extras ou carteira atual."
            )
            return

        usd_brl, fx_ok = fetch_usd_brl_rate()
        progress_bar = st.progress(0)
        status = st.empty()

        def update_progress(idx, total):
            progress_bar.progress((idx + 1) / total)

        def phase_callback(name):
            status.caption(f"Fase: {name} · run `{run_id}`")

        result = process_portfolio(
            tickers=tickers,
            current_positions=current_positions,
            period=period,
            run_ai=run_ai,
            max_ai_assets=max_ai_assets,
            strategy=strategy,
            portfolio_mode=portfolio_mode,
            capital=capital,
            max_portfolio_assets=max_portfolio_assets,
            ai_password=ai_password,
            progress_callback=update_progress,
            llm_provider=llm_provider,
            llm_model=llm_model,
            rebalance_threshold_pct=rebalance_threshold_pct,
            base_currency=base_currency,
            usd_brl=usd_brl,
            fx_ok=fx_ok,
            quick_mode=quick_mode,
            score_weights=score_weights,
            class_targets=class_targets,
            phase_callback=phase_callback,
        )

        comparison = None
        if compare_strats:
            comparison = compare_strategies(
                result["scored_assets"],
                list(STRATEGY_WEIGHTS.keys()),
                result["target_total_value"],
                max_assets=max_portfolio_assets,
            )

        wl_alerts = []
        if watchlist:
            wl_assets = [a for a in result["scored_assets"] if a.ticker in set(watchlist)]
            wl_alerts = evaluate_alerts(wl_assets)

        run = {
            **result,
            "capital": capital,
            "run_ai": run_ai and not quick_mode,
            "rebalance_threshold_pct": rebalance_threshold_pct,
            "run_id": run_id,
            "strategy": strategy,
            "ts": datetime.now(UTC).isoformat(timespec="seconds"),
            "comparison": comparison,
            "watchlist_alerts": [
                {"ticker": a.ticker, "rule": a.rule, "message": a.message} for a in wl_alerts
            ],
            "lang": lang,
        }
        st.session_state.last_run = run
        _push_run_history(run)

        logger.info(
            "run_id=%s tickers=%s ok=%s fail=%s fetch_ms=%.0f score_ms=%.0f ai_ms=%.0f",
            run_id,
            len(tickers),
            len(result["scored_assets"]),
            len(result["failed_tickers"]),
            result["fetch_ms"],
            result["score_ms"],
            result["ai_ms"],
        )

        prefs = {
            "portfolio_text": current_portfolio_text,
            "asset_classes": list(asset_classes or []),
            "universe": universe,
            "strategy": strategy,
            "capital": float(capital),
            "portfolio_mode": portfolio_mode,
            "rebalance_threshold_pct": float(rebalance_threshold_pct),
            "base_currency": base_currency,
            "extra_tickers": extra_tickers_raw or "",
            "watchlist": list(watchlist or []),
            "lang": lang,
        }
        try:
            st.query_params[QUERY_KEY] = encode_prefs(prefs)
        except Exception:
            logger.debug("URL prefs fail", exc_info=True)
        save_prefs_file(prefs)
        st.success(f"Análise concluída · run `{run_id}`")


def _apply_projection_to_portfolio(projected_rows):
    positions = projected_positions_for_session(projected_rows)
    st.session_state.portfolio_text = format_positions_as_text(positions)
    st.success("Carteira atual atualizada com a projeção. Ajuste se quiser e gere novamente.")


def _render_last_run():
    hist = st.session_state.get("run_history") or []
    if hist:
        labels = [
            f"{r.get('ts', '?')} · {r.get('strategy', '?')} · {r.get('run_id', '')}"
            for r in hist
        ]
        idx = st.selectbox(
            "Histórico de runs (sessão)",
            options=list(range(len(hist))),
            format_func=lambda i: labels[i],
            key="run_history_select",
        )
        run = hist[int(idx)]
        st.session_state.last_run = run
    else:
        run = st.session_state.get("last_run")

    if not run:
        render_empty_state(lang=st.session_state.get("pref_lang", "pt"))
        return

    base = run.get("base_currency", "BRL")
    cur_label = "R$" if base == "BRL" else "USD"
    final_portfolio = run["final_portfolio"]
    display_summary_metrics(
        asset_count=len(final_portfolio),
        current_total=run["current_total_value"],
        new_investment=run["capital"],
        target_total=run["target_total_value"],
        currency_label=cur_label,
    )

    if not run.get("fx_ok", True):
        st.warning(
            f"Câmbio USD/BRL indisponível — usando taxa fallback. "
            f"Totais em {base} podem estar imprecisos."
        )
    else:
        st.caption(
            f"Moeda-base: {base} · USD/BRL={float(run.get('usd_brl', 0)):.4f} · "
            f"run `{run.get('run_id', '')}`"
        )

    if run["failed_tickers"]:
        st.warning(
            f"Não foi possível obter dados para: {', '.join(run['failed_tickers'])}. "
            "Verifique o ticker ou tente novamente."
        )
    short_hist = run.get("short_history_tickers") or []
    if short_hist:
        st.warning(
            "Histórico insuficiente para indicadores completos: "
            f"{', '.join(short_hist)}. Scores técnicos desses ativos tendem a ser neutros."
        )
    if run.get("run_ai"):
        st.caption(f"IA executada em {run['ai_calls']} ativos.")
    else:
        st.caption("IA desativada nesta rodada.")

    if run.get("rebalance_actions") == [] and float(run.get("rebalance_threshold_pct") or 0) > 0:
        st.info(
            f"Nenhuma ação de rebalance acima do limiar "
            f"{run.get('rebalance_threshold_pct')}%. Tente abaixar o limiar na sidebar."
        )

    display_portfolio(final_portfolio, currency_label=cur_label)
    display_rebalance_plan(
        run["rebalance_actions"],
        run["current_total_value"],
        run["capital"],
        run["target_total_value"],
        threshold_pct=float(run.get("rebalance_threshold_pct") or 0.0),
        currency_label=cur_label,
    )
    display_projected_portfolio(
        run["projected_rows"],
        run["current_total_value"],
        run["capital"],
        run["target_total_value"],
        on_apply=lambda: _apply_projection_to_portfolio(run["projected_rows"]),
        currency_label=cur_label,
    )

    if run.get("comparison"):
        display_strategy_comparison(run["comparison"])

    if run.get("watchlist_alerts"):
        display_watchlist_alerts(run["watchlist_alerts"])

    if any(a.ai_analysis for a in run["scored_assets"]):
        from ducks.ui.i18n import t as _t

        st.info(_t("ai_risks", run.get("lang", "pt")))

    with st.expander("Detalhes técnicos de todos os ativos"):
        for asset in run["scored_assets"]:
            st.markdown(f"**{asset.ticker}** — score {asset.total_score:.2f}")
            if asset.score_breakdown:
                st.caption(
                    "Breakdown: "
                    + ", ".join(f"{k}={v:.3f}" for k, v in asset.score_breakdown.items())
                )
            if asset.ai_analysis:
                st.caption(f"IA: {asset.ai_analysis.short_summary_pt}")
            if asset.technical:
                st.write(
                    f"RSI: {asset.technical.rsi:.1f} · Tendência: {asset.technical.ema_trend} · "
                    f"Moeda nativa: {asset.currency} · Preço base: {asset.price_in_base:.2f}"
                )
            if asset.close_series and len(asset.close_series) > 2:
                import pandas as pd

                st.line_chart(pd.Series(asset.close_series, name="Close"))
            st.divider()

    st.caption(
        f"Latências ms — fetch: {run.get('fetch_ms', 0):.0f} · "
        f"score: {run.get('score_ms', 0):.0f} · ia: {run.get('ai_ms', 0):.0f}"
    )


def main():
    render_header(APP_TITLE, APP_ICON)

    sidebar = render_sidebar()
    (
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
        base_currency,
        extra_tickers_raw,
        quick_mode,
        score_weights,
        class_targets,
        watchlist,
        compare_strats,
        lang,
    ) = sidebar

    if st.sidebar.button(
        __import__("ui.i18n", fromlist=["t"]).t("generate", lang),
        type="primary",
    ):
        handle_generate_portfolio(
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
            base_currency=base_currency,
            extra_tickers_raw=extra_tickers_raw,
            quick_mode=quick_mode,
            score_weights=score_weights,
            class_targets=class_targets,
            watchlist=watchlist,
            compare_strats=compare_strats,
            lang=lang,
        )

    _render_last_run()
    render_disclaimer(lang=lang)


if __name__ == "__main__":
    main()
