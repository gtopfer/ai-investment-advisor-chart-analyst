import streamlit as st
from typing import Dict, List, Optional
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

from config.config import (
    APP_TITLE,
    APP_ICON,
    DEFAULT_TICKERS_BR_STOCKS,
    DEFAULT_TICKERS_BR_FIIS,
    DEFAULT_TICKERS_US,
    DEFAULT_TICKERS_US_ETFS,
    DEFAULT_TICKERS_US_STOCKS,
    DEFAULT_TICKERS_CRYPTO,
    AI_ACCESS_PASSWORD,
    MAX_AI_CALLS_PER_SESSION,
)
from ui.layout import (
    render_header,
    render_sidebar,
    display_portfolio,
    display_rebalance_plan,
    render_disclaimer,
)
from data_fetcher.market_data import get_price_history, get_fundamentals, get_dividend_history
from analysis.technical_analysis import analyze_chart_patterns
from analysis.dividend_analysis import analyze_dividends
from analysis.ai_chart_engine import run_ai_technical_analysis
from allocator.portfolio_allocator import score_assets, allocate_capital, build_rebalance_actions
from models.schemas import AssetAnalysis


_BR_FII_SUFFIX_PATTERN = re.compile(r"1[12]B?\.SA$")
_US_STOCK_PATTERN = re.compile(r"^[A-Z]{1,5}$")


def classify_ticker(ticker: str) -> tuple[str, str]:
    """
    Best-effort classificação de classe e mercado com base em heurísticas simples.
    Ativos fora das listas padrão (ex.: digitados manualmente na carteira atual)
    caem nos fallbacks por padrão de sufixo/formato antes de "Desconhecido".
    """
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
    if ticker in DEFAULT_TICKERS_CRYPTO or "-USD" in ticker:
        return "Cripto", "CRYPTO"
    if ticker.endswith(".SA"):
        # FIIs brasileiros seguem o padrão "XXXX11.SA"/"XXXX12.SA" (fallback
        # para tickers fora da lista padrão, ex.: digitados na carteira atual)
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

    # Remove duplicados preservando ordem inicial
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


def parse_current_portfolio(raw_text: str) -> Dict[str, float]:
    """
    Parseia carteira informada pelo usuário.
    Formatos aceitos por linha: TICKER,VALOR | TICKER:VALOR | TICKER;VALOR
    """
    positions: Dict[str, float] = {}
    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = [part.strip() for part in re.split(r'[,;:]', line, maxsplit=1) if part.strip()]
        if len(parts) != 2:
            continue

        ticker = parts[0].upper()
        if not re.match(r"^[A-Z0-9.\-]+$", ticker):
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
    positions: Dict[str, float],
    portfolio_mode: str,
    analyzed_assets: List[AssetAnalysis],
) -> Dict[str, float]:
    """
    Converte posições atuais em mapa de valor monetário por ticker.
    """
    if portfolio_mode == "Valor atual (R$)":
        return positions

    prices = {asset.ticker: float(asset.current_price) for asset in analyzed_assets}
    value_map: Dict[str, float] = {}
    for ticker, qty in positions.items():
        value_map[ticker] = qty * prices.get(ticker, 0.0)
    return value_map


def _process_single_ticker(ticker: str, period: str):
    price_df = get_price_history(ticker, period=period)
    fundamentals = get_fundamentals(ticker) or {}

    if price_df.empty and not fundamentals:
        return None

    current_price = fundamentals.get("current_price", 0.0)
    if current_price == 0.0 and not price_df.empty:
        current_price = price_df['Close'].iloc[-1]

    asset_class, market = classify_ticker(ticker)
    tech_indicators = analyze_chart_patterns(ticker, price_df)
    dividend_history = get_dividend_history(ticker)
    div_metrics = analyze_dividends(ticker, fundamentals, price_df, dividend_history)

    return AssetAnalysis(
        ticker=ticker,
        market=market,
        asset_class=asset_class,
        current_price=current_price,
        technical=tech_indicators,
        ai_analysis=None,
        dividends=div_metrics
    )


def _split_results(
    tickers: list[str],
    results: Dict[str, Optional[AssetAnalysis]],
) -> tuple[List[AssetAnalysis], List[str]]:
    """
    Separa resultados em (ativos analisados, tickers que falharam),
    preservando a ordem original de `tickers`.
    """
    analyzed_assets: List[AssetAnalysis] = []
    failed_tickers: List[str] = []
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
            st.warning(f"Limite de chamadas IA por sessão ({MAX_AI_CALLS_PER_SESSION}) atingido. A análise com IA foi desativada.")
            run_ai = False

    ai_calls = 0
    completed_count = 0
    results: Dict[str, Optional[AssetAnalysis]] = {ticker: None for ticker in tickers}
    ctx = get_script_run_ctx()

    def _process_with_context(ticker_arg, period_arg, run_ctx):
        if run_ctx:
            add_script_run_ctx(ctx=run_ctx)
        return _process_single_ticker(ticker_arg, period_arg)

    with ThreadPoolExecutor(max_workers=10) as executor:
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
            except Exception as e:
                print(f"Erro ao processar {ticker}: {e}")

    # Reconstrói a lista preservando a ordem original dos tickers e separa falhas
    analyzed_assets, failed_tickers = _split_results(tickers, results)

    # IA executada sequencialmente para respeitar limite global de chamadas
    if run_ai:
        for asset in analyzed_assets:
            if ai_calls >= max_ai_assets or st.session_state.ai_calls_session >= MAX_AI_CALLS_PER_SESSION:
                break
            asset.ai_analysis = run_ai_technical_analysis(asset.ticker, asset.technical)
            ai_calls += 1
            st.session_state.ai_calls_session += 1

    return analyzed_assets, ai_calls, failed_tickers


def process_portfolio(
    tickers: list[str],
    current_positions: Dict[str, float],
    period: str,
    run_ai: bool,
    max_ai_assets: int,
    strategy: str,
    portfolio_mode: str,
    capital: float,
    max_portfolio_assets: int,
    ai_password: str = "",
    progress_callback=None,
):
    analyzed_assets, ai_calls, failed_tickers = analyze_assets(
        tickers, period, run_ai, max_ai_assets, ai_password, progress_callback
    )

    scored_assets = score_assets(analyzed_assets, strategy)
    current_value_map = convert_positions_to_value_map(current_positions, portfolio_mode, scored_assets)
    current_total_value = sum(current_value_map.values())
    target_total_value = current_total_value + capital
    final_portfolio = allocate_capital(scored_assets, target_total_value, max_assets=max_portfolio_assets)
    rebalance_actions = build_rebalance_actions(current_value_map, final_portfolio)

    return scored_assets, final_portfolio, rebalance_actions, current_total_value, target_total_value, ai_calls, failed_tickers


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

        scored_assets, final_portfolio, rebalance_actions, current_total_value, target_total_value, ai_calls, failed_tickers = process_portfolio(
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
        )

        st.success("Análise concluída!")
        if failed_tickers:
            st.warning(
                f"Não foi possível obter dados para: {', '.join(failed_tickers)}. "
                "Podem estar indisponíveis na fonte de dados ou o ticker está incorreto."
            )
        if run_ai:
            st.caption(f"IA executada em {ai_calls} ativos (limite configurado: {max_ai_assets}).")
        else:
            st.caption("IA desativada nesta rodada. Ative na barra lateral se quiser as justificativas da Groq.")
        display_portfolio(final_portfolio)
        display_rebalance_plan(rebalance_actions, current_total_value, capital, target_total_value)

        with st.expander("Ver Detalhes Técnicos de Todos os Ativos"):
            for asset in scored_assets:
                st.markdown(f"**{asset.ticker}** - Score: {asset.total_score:.2f}")
                if asset.ai_analysis:
                    st.caption(f"IA: {asset.ai_analysis.short_summary_pt}")
                st.write(f"RSI: {asset.technical.rsi:.1f} | Tendência: {asset.technical.ema_trend}")
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
    ) = render_sidebar()

    if st.sidebar.button("Gerar Carteira Recomendada", type="primary"):
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
        )

    render_disclaimer()

if __name__ == "__main__":
    main()
