import streamlit as st
from typing import Dict, List

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
from data_fetcher.market_data import get_price_history, get_fundamentals
from analysis.technical_analysis import analyze_chart_patterns
from analysis.dividend_analysis import analyze_dividends
from analysis.ai_chart_engine import run_ai_technical_analysis
from allocator.portfolio_allocator import score_assets, allocate_capital, build_rebalance_actions
from models.schemas import AssetAnalysis


def classify_ticker(ticker: str) -> tuple[str, str]:
    """
    Best-effort classificação de classe e mercado com base em heurísticas simples.
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
        return "Ações", "BR"
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


import re

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

        # Split by the first occurrence of , ; or :
        parts = [part.strip() for part in re.split(r'[,;:]', line, maxsplit=1) if part.strip()]
        if len(parts) != 2:
            continue

        ticker = parts[0].upper()
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
    analyzed_assets = []
    ai_calls = 0

    if run_ai:
        if AI_ACCESS_PASSWORD and ai_password != AI_ACCESS_PASSWORD:
            st.warning("Senha da IA incorreta. A análise com IA foi desativada para esta execução.")
            run_ai = False

        if "ai_calls_session" not in st.session_state:
            st.session_state.ai_calls_session = 0

        if st.session_state.ai_calls_session >= MAX_AI_CALLS_PER_SESSION:
            st.warning(f"Limite de chamadas IA por sessão ({MAX_AI_CALLS_PER_SESSION}) atingido. A análise com IA foi desativada.")
            run_ai = False

    for idx, ticker in enumerate(tickers):
        if progress_callback:
            progress_callback(idx, len(tickers))

        # 2. Coleta de Dados
        price_df = get_price_history(ticker, period=period)
        fundamentals = get_fundamentals(ticker) or {}

        if price_df.empty and not fundamentals:
            continue

        current_price = fundamentals.get("current_price", 0.0)
        if current_price == 0.0 and not price_df.empty:
            current_price = price_df['Close'].iloc[-1]

        asset_class, market = classify_ticker(ticker)

        # 3. Análises
        tech_indicators = analyze_chart_patterns(ticker, price_df)

        # Dividendos (apenas se fizer sentido)
        div_metrics = analyze_dividends(ticker, fundamentals, price_df)

        # IA (opcional)
        ai_result = None
        if run_ai and ai_calls < max_ai_assets and st.session_state.ai_calls_session < MAX_AI_CALLS_PER_SESSION:
            ai_result = run_ai_technical_analysis(ticker, tech_indicators)
            ai_calls += 1
            st.session_state.ai_calls_session += 1

        # Monta objeto
        asset = AssetAnalysis(
            ticker=ticker,
            market=market,
            asset_class=asset_class,
            current_price=current_price,
            technical=tech_indicators,
            ai_analysis=ai_result,
            dividends=div_metrics
        )
        analyzed_assets.append(asset)

    # 4. Scoring e Alocação
    scored_assets = score_assets(analyzed_assets, strategy)
    current_value_map = convert_positions_to_value_map(current_positions, portfolio_mode, scored_assets)
    current_total_value = sum(current_value_map.values())
    target_total_value = current_total_value + capital
    final_portfolio = allocate_capital(scored_assets, target_total_value, max_assets=max_portfolio_assets)
    rebalance_actions = build_rebalance_actions(current_value_map, final_portfolio)

    return scored_assets, final_portfolio, rebalance_actions, current_total_value, target_total_value, ai_calls


def main():
    render_header(APP_TITLE, APP_ICON)
    
    # Sidebar Inputs
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
        with st.spinner("Analisando mercado e processando dados..."):
            
            # 1. Seleção de Tickers Candidatos
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

            scored_assets, final_portfolio, rebalance_actions, current_total_value, target_total_value, ai_calls = process_portfolio(
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
            
            # 5. Exibição
            st.success("Análise concluída!")
            if run_ai:
                st.caption(f"IA executada em {ai_calls} ativos (limite configurado: {max_ai_assets}).")
            else:
                st.caption("IA desativada nesta rodada. Ative na barra lateral se quiser as justificativas da Groq.")
            display_portfolio(final_portfolio)
            display_rebalance_plan(rebalance_actions, current_total_value, capital, target_total_value)
            
            # Detalhes Expandidos (Opcional)
            with st.expander("Ver Detalhes Técnicos de Todos os Ativos"):
                for asset in scored_assets:
                    st.markdown(f"**{asset.ticker}** - Score: {asset.total_score:.2f}")
                    if asset.ai_analysis:
                        st.caption(f"IA: {asset.ai_analysis.short_summary_pt}")
                    st.write(f"RSI: {asset.technical.rsi:.1f} | Tendência: {asset.technical.ema_trend}")
                    st.divider()

    render_disclaimer()

if __name__ == "__main__":
    main()
