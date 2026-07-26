import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

from allocator.portfolio_allocator import (
    allocate_capital,
    build_projected_portfolio,
    build_rebalance_actions,
    projected_positions_for_session,
    score_assets,
)
from analysis.ai_chart_engine import run_ai_technical_analysis
from analysis.dividend_analysis import analyze_dividends
from analysis.technical_analysis import analyze_chart_patterns
from config.config import (
    AI_ACCESS_PASSWORD,
    APP_ICON,
    APP_TITLE,
    DEFAULT_TICKERS_BR_FIIS,
    DEFAULT_TICKERS_BR_STOCKS,
    DEFAULT_TICKERS_CRYPTO,
    DEFAULT_TICKERS_US,
    DEFAULT_TICKERS_US_ETFS,
    DEFAULT_TICKERS_US_STOCKS,
    MAX_AI_CALLS_PER_SESSION,
)
from data_fetcher.market_data import (
    get_dividend_history,
    get_fundamentals,
    get_price_history,
)
from models.schemas import AssetAnalysis
from portfolio.import_portfolio import format_positions_as_text
from ui.layout import (
    display_portfolio,
    display_projected_portfolio,
    display_rebalance_plan,
    display_summary_metrics,
    render_disclaimer,
    render_empty_state,
    render_header,
    render_sidebar,
)
from utils.tickers import is_crypto_ticker, normalize_ticker

_BR_FII_SUFFIX_PATTERN = re.compile(r"1[12]B?\.SA$")
_US_STOCK_PATTERN = re.compile(r"^[A-Z]{1,5}$")


def classify_ticker(ticker: str) -> tuple[str, str]:
    """
    Best-effort classificação de classe e mercado com base em heurísticas simples.
    Ativos fora das listas padrão (ex.: digitados manualmente na carteira atual)
    caem nos fallbacks por padrão de sufixo/formato antes de "Desconhecido".
    """
    ticker = normalize_ticker(ticker)
    if ticker in DEFAULT_TICKERS_BR_FIIS:
        return "FIIs", "BR"
    if ticker in DEFAULT_TICKERS_BR_STOCKS:
        return "Ações", "BR"
    if ticker in DEFAULT_TICKERS_US_ETFS:
        return "ETFs", "US"
    if ticker in DEFAULT_TICKERS_US_STOCKS:
        return "Ações", "US"
    if ticker in DEFAULT_TICKERS_US:
        return "Ações/ETF", "US"
    if ticker in DEFAULT_TICKERS_CRYPTO or is_crypto_ticker(ticker):
        return "Cripto", "CRYPTO"
    if ticker.endswith(".SA"):
        if _BR_FII_SUFFIX_PATTERN.search(ticker):
            return "FIIs", "BR"
        return "Ações", "BR"
    if _US_STOCK_PATTERN.match(ticker):
        return "Ações", "US"
    return "Desconhecido", "US/CRYPTO"


def build_candidate_tickers(asset_classes, universe) -> list[str]:
    """
    Monta lista de tickers respeitando filtro de classes e geografia.
    """
    tickers: list[str] = []

    if universe in ["Nacional", "Ambos"]:
        if "Ações" in asset_classes:
            tickers.extend(DEFAULT_TICKERS_BR_STOCKS)
        if "FIIs" in asset_classes:
            tickers.extend(DEFAULT_TICKERS_BR_FIIS)

    if universe in ["Internacional", "Ambos"]:
        if "Ações" in asset_classes:
            tickers.extend(DEFAULT_TICKERS_US_STOCKS)
        if "ETFs" in asset_classes:
            tickers.extend(DEFAULT_TICKERS_US_ETFS)

    if "Cripto" in asset_classes:
        tickers.extend(DEFAULT_TICKERS_CRYPTO)

    return list(dict.fromkeys(tickers))


def _parse_numeric_value(value: str) -> float:
    clean = value.strip().replace("R$", "").replace(" ", "")
    if "," in clean and "." in clean:
        if clean.rfind(",") > clean.rfind("."):
            clean = clean.replace(".", "").replace(",", ".")
        else:
            clean = clean.replace(",", "")
    elif "," in clean:
        clean = clean.replace(".", "").replace(",", ".")
    return float(clean)


def parse_current_portfolio(raw_text: str) -> dict[str, float]:
    """
    Parseia carteira informada pelo usuário.
    Formatos aceitos por linha: TICKER,VALOR | TICKER:VALOR | TICKER;VALOR
    """
    positions: dict[str, float] = {}
    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = [part.strip() for part in re.split(r"[,;:]", line, maxsplit=1) if part.strip()]
        if len(parts) != 2:
            continue

        ticker = normalize_ticker(parts[0])
        if not ticker or not re.match(r"^[A-Z0-9.\-]+$", ticker):
            continue

        try:
            amount = _parse_numeric_value(parts[1])
        except ValueError:
            continue

        if amount <= 0:
            continue

        positions[ticker] = positions.get(ticker, 0.0) + amount
    return positions


def convert_positions_to_value_map(
    positions: dict[str, float],
    portfolio_mode: str,
    analyzed_assets: list[AssetAnalysis],
) -> dict[str, float]:
    """
    Converte posições atuais em mapa de valor monetário por ticker.
    """
    if portfolio_mode == "Valor atual (R$)":
        return positions

    prices = {asset.ticker: float(asset.current_price) for asset in analyzed_assets}
    value_map: dict[str, float] = {}
    for ticker, qty in positions.items():
        value_map[ticker] = qty * prices.get(ticker, 0.0)
    return value_map


def _process_single_ticker(ticker: str, period: str):
    ticker = normalize_ticker(ticker)
    price_df = get_price_history(ticker, period=period)
    fundamentals = get_fundamentals(ticker) or {}

    if price_df.empty and not fundamentals:
        return None

    current_price = fundamentals.get("current_price", 0.0)
    if current_price == 0.0 and not price_df.empty:
        current_price = price_df["Close"].iloc[-1]

    asset_class, market = classify_ticker(ticker)
    tech_indicators = analyze_chart_patterns(ticker, price_df)
    dividend_history = get_dividend_history(ticker)
    div_metrics = analyze_dividends(
        ticker,
        fundamentals,
        price_df,
        dividend_history,
        is_crypto=(asset_class == "Cripto" or market == "CRYPTO"),
    )

    return AssetAnalysis(
        ticker=ticker,
        market=market,
        asset_class=asset_class,
        current_price=current_price,
        technical=tech_indicators,
        ai_analysis=None,
        dividends=div_metrics,
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


def analyze_assets(
    tickers: list[str],
    period: str,
    run_ai: bool,
    max_ai_assets: int,
    ai_password: str = "",
    progress_callback=None,
    llm_provider: str | None = None,
    llm_model: str | None = None,
):
    """
    Executa coleta de dados e análises (técnica, dividendos, IA) em paralelo para cada ativo.
    """
    if run_ai:
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

    ai_calls = 0
    completed_count = 0
    results: dict[str, AssetAnalysis | None] = {ticker: None for ticker in tickers}
    ctx = get_script_run_ctx()

    def _process_with_context(ticker_arg, period_arg, run_ctx):
        if run_ctx:
            add_script_run_ctx(ctx=run_ctx)
        return _process_single_ticker(ticker_arg, period_arg)

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ticker = {
            executor.submit(_process_with_context, ticker, period, ctx): ticker for ticker in tickers
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
            except Exception as e:
                print(f"Erro ao processar {ticker}: {e}")

    analyzed_assets, failed_tickers = _split_results(tickers, results)

    if run_ai:
        for asset in analyzed_assets:
            if ai_calls >= max_ai_assets or st.session_state.ai_calls_session >= MAX_AI_CALLS_PER_SESSION:
                break
            asset.ai_analysis = run_ai_technical_analysis(
                asset.ticker,
                asset.technical,
                provider_id=llm_provider,
                model=llm_model,
            )
            ai_calls += 1
            st.session_state.ai_calls_session += 1

    return analyzed_assets, ai_calls, failed_tickers


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
):
    analyzed_assets, ai_calls, failed_tickers = analyze_assets(
        tickers,
        period,
        run_ai,
        max_ai_assets,
        ai_password,
        progress_callback,
        llm_provider=llm_provider,
        llm_model=llm_model,
    )

    scored_assets = score_assets(analyzed_assets, strategy)
    current_value_map = convert_positions_to_value_map(current_positions, portfolio_mode, scored_assets)
    current_total_value = sum(current_value_map.values())
    target_total_value = current_total_value + capital
    final_portfolio = allocate_capital(scored_assets, target_total_value, max_assets=max_portfolio_assets)
    rebalance_actions = build_rebalance_actions(current_value_map, final_portfolio)
    projected_rows = build_projected_portfolio(current_value_map, final_portfolio)

    return (
        scored_assets,
        final_portfolio,
        rebalance_actions,
        projected_rows,
        current_total_value,
        target_total_value,
        ai_calls,
        failed_tickers,
    )


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
):
    with st.spinner("Analisando mercado e processando dados..."):
        tickers = build_candidate_tickers(asset_classes, universe)
        current_positions = parse_current_portfolio(current_portfolio_text)
        if current_positions:
            tickers = list(dict.fromkeys(tickers + list(current_positions.keys())))

        if not tickers:
            st.error("Nenhum ativo selecionado. Verifique os filtros.")
            return

        progress_bar = st.progress(0)

        def update_progress(idx, total):
            progress_bar.progress((idx + 1) / total)

        (
            scored_assets,
            final_portfolio,
            rebalance_actions,
            projected_rows,
            current_total_value,
            target_total_value,
            ai_calls,
            failed_tickers,
        ) = process_portfolio(
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
        )

        st.session_state.last_run = {
            "scored_assets": scored_assets,
            "final_portfolio": final_portfolio,
            "rebalance_actions": rebalance_actions,
            "projected_rows": projected_rows,
            "current_total_value": current_total_value,
            "target_total_value": target_total_value,
            "capital": capital,
            "ai_calls": ai_calls,
            "failed_tickers": failed_tickers,
            "run_ai": run_ai,
        }
        st.success("Análise concluída.")


def _apply_projection_to_portfolio(projected_rows):
    positions = projected_positions_for_session(projected_rows)
    st.session_state.portfolio_text = format_positions_as_text(positions)
    st.success("Carteira atual atualizada com a projeção. Ajuste se quiser e gere novamente.")


def _render_last_run():
    run = st.session_state.get("last_run")
    if not run:
        render_empty_state()
        return

    final_portfolio = run["final_portfolio"]
    display_summary_metrics(
        asset_count=len(final_portfolio),
        current_total=run["current_total_value"],
        new_investment=run["capital"],
        target_total=run["target_total_value"],
    )

    if run["failed_tickers"]:
        st.warning(
            f"Não foi possível obter dados para: {', '.join(run['failed_tickers'])}. "
            "Podem estar indisponíveis na fonte de dados ou o ticker está incorreto."
        )
    if run["run_ai"]:
        st.caption(f"IA executada em {run['ai_calls']} ativos.")
    else:
        st.caption("IA desativada nesta rodada.")

    display_portfolio(final_portfolio)
    display_rebalance_plan(
        run["rebalance_actions"],
        run["current_total_value"],
        run["capital"],
        run["target_total_value"],
    )
    display_projected_portfolio(
        run["projected_rows"],
        run["current_total_value"],
        run["capital"],
        run["target_total_value"],
        on_apply=lambda: _apply_projection_to_portfolio(run["projected_rows"]),
    )

    with st.expander("Detalhes técnicos de todos os ativos"):
        for asset in run["scored_assets"]:
            st.markdown(f"**{asset.ticker}** — score {asset.total_score:.2f}")
            if asset.ai_analysis:
                st.caption(f"IA: {asset.ai_analysis.short_summary_pt}")
            st.write(f"RSI: {asset.technical.rsi:.1f} · Tendência: {asset.technical.ema_trend}")
            st.divider()


def main():
    render_header(APP_TITLE, APP_ICON)

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
    ) = render_sidebar()

    if st.sidebar.button("Gerar carteira recomendada", type="primary"):
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
        )

    _render_last_run()
    render_disclaimer()


if __name__ == "__main__":
    main()
