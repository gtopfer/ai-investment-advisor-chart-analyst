import streamlit as st
import pandas as pd

def render_header(title: str, icon: str):
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    st.title(f"{icon} {title}")
    st.markdown("---")

def render_sidebar():
    st.sidebar.header("Configurações de Investimento")
    
    # Classes de Ativos
    asset_classes = st.sidebar.multiselect(
        "Classes de Ativos",
        ["Ações", "FIIs", "ETFs", "BDRs", "Cripto"],
        default=["Ações", "FIIs"]
    )
    
    # Universo
    universe = st.sidebar.radio(
        "Universo Geográfico",
        ["Nacional", "Internacional", "Ambos"],
        index=0
    )
    
    # Estratégia
    strategy = st.sidebar.select_slider(
        "Estratégia",
        options=["Growth", "Equilíbrio", "Dividendos"],
        value="Equilíbrio"
    )
    
    # Capital
    capital = st.sidebar.number_input(
        "Novo aporte para investir (R$)",
        min_value=100.0,
        value=10000.0,
        step=100.0
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Carteira atual")
    portfolio_mode = st.sidebar.selectbox(
        "Formato da carteira atual",
        ["Valor atual (R$)", "Quantidade de cotas/unidades"],
        index=0,
    )
    current_portfolio_text = st.sidebar.text_area(
        "Posições atuais (uma por linha)",
        value="PETR4.SA, 3000\nHGLG11.SA, 2000\nAAPL, 1500",
        height=120,
        help="Formato: TICKER, VALOR ou TICKER, QUANTIDADE (dependendo da opção acima).",
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Avançado")
    period = st.sidebar.selectbox("Período de Análise", ["6mo", "1y", "2y", "5y"], index=1)
    run_ai = st.sidebar.checkbox("Rodar análise IA (Groq)", value=False, help="Desative para acelerar. Ative se houver chave GROQ_API_KEY.")
    max_ai_assets = st.sidebar.slider("Limite de ativos para IA", min_value=1, max_value=30, value=5, step=1, help="Limita quantos tickers recebem análise de IA nesta rodada.")
    max_portfolio_assets = st.sidebar.slider(
        "Máximo de ativos na carteira alvo",
        min_value=3,
        max_value=20,
        value=10,
        step=1,
    )
    
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
    )

def display_portfolio(portfolio):
    if not portfolio:
        st.warning("Nenhum ativo qualificado encontrado para os critérios selecionados.")
        return

    # Prepara DataFrame para exibição
    data = []
    for p in portfolio:
        data.append({
            "Ticker": p.ticker,
            "Recomendação": p.recommendation,
            "Score": f"{p.total_score:.2f}",
            "Alocação %": f"{p.suggested_allocation_pct:.1f}%",
            "Valor (R$)": f"R$ {p.suggested_value:,.2f}",
            "Motivo": p.reason,
            "Preço Atual": f"{p.current_price:.2f}"
        })
    
    df = pd.DataFrame(data)
    
    st.subheader("Carteira Recomendada")
    st.dataframe(df, use_container_width=True)
    
    # Gráfico de Pizza
    if len(df) > 0:
        st.subheader("Distribuição de Alocação")
        chart_data = pd.DataFrame({
            "Ticker": [p.ticker for p in portfolio],
            "Alocação": [p.suggested_allocation_pct for p in portfolio]
        })
        st.bar_chart(chart_data.set_index("Ticker"))


def display_rebalance_plan(actions, current_total: float, new_investment: float, target_total: float):
    st.subheader("Plano de Rebalanceamento Automático")
    st.caption(
        f"Carteira atual: R$ {current_total:,.2f} | Aporte novo: R$ {new_investment:,.2f} | "
        f"Carteira alvo: R$ {target_total:,.2f}"
    )

    if not actions:
        st.info("Sem ajustes relevantes para rebalanceamento no momento.")
        return

    rows = []
    for item in actions:
        rows.append(
            {
                "Ticker": item["ticker"],
                "Ação": item["action"],
                "Valor Atual (R$)": f"R$ {item['current_value']:,.2f}",
                "Valor Alvo (R$)": f"R$ {item['target_value']:,.2f}",
                "Ajuste (R$)": f"R$ {item['delta_value']:,.2f}",
            }
        )

    st.dataframe(pd.DataFrame(rows), use_container_width=True)

def render_disclaimer():
    st.markdown("---")
    st.warning(
        "⚠️ **AVISO LEGAL**: Esta ferramenta tem finalidade estritamente **EDUCACIONAL**. "
        "Os dados apresentados não constituem recomendação de compra ou venda de ativos. "
        "Rentabilidade passada não é garantia de resultados futuros. "
        "Consulte um profissional certificado antes de investir."
    )
