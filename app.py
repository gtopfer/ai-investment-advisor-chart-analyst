import streamlit as st
from config.config import (
    APP_TITLE,
    APP_ICON,
    DEFAULT_TICKERS_BR_STOCKS,
    DEFAULT_TICKERS_BR_FIIS,
    DEFAULT_TICKERS_US,
    DEFAULT_TICKERS_US_ETFS,
    DEFAULT_TICKERS_US_STOCKS,
    DEFAULT_TICKERS_CRYPTO,
)
from ui.layout import render_header, render_sidebar, display_portfolio, render_disclaimer
from data_fetcher.market_data import get_price_history, get_fundamentals
from analysis.technical_analysis import analyze_chart_patterns
from analysis.dividend_analysis import analyze_dividends
from analysis.ai_chart_engine import run_ai_technical_analysis
from allocator.portfolio_allocator import score_assets, allocate_capital
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


def main():
    render_header(APP_TITLE, APP_ICON)
    
    # Sidebar Inputs
    asset_classes, universe, strategy, capital, period, run_ai, max_ai_assets = render_sidebar()
    
    if st.sidebar.button("Gerar Carteira Recomendada", type="primary"):
        with st.spinner("Analisando mercado e processando dados..."):
            
            # 1. Seleção de Tickers Candidatos
            tickers = build_candidate_tickers(asset_classes, universe)

            if not tickers:
                st.error("Nenhum ativo selecionado. Verifique os filtros.")
                return

            analyzed_assets = []
            ai_calls = 0
            progress_bar = st.progress(0)
            
            for idx, ticker in enumerate(tickers):
                # Atualiza barra de progresso
                progress_bar.progress((idx + 1) / len(tickers))
                
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
                if run_ai and ai_calls < max_ai_assets:
                    ai_result = run_ai_technical_analysis(ticker, tech_indicators)
                    ai_calls += 1
                
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
            final_portfolio = allocate_capital(scored_assets, capital)
            
            # 5. Exibição
            st.success("Análise concluída!")
            if run_ai:
                st.caption(f"IA executada em {ai_calls} ativos (limite configurado: {max_ai_assets}).")
            else:
                st.caption("IA desativada nesta rodada. Ative na barra lateral se quiser as justificativas da Groq.")
            display_portfolio(final_portfolio)
            
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
