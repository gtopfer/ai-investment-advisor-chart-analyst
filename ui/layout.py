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
        "Capital Total (R$)",
        min_value=100.0,
        value=10000.0,
        step=100.0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Avançado")
    period = st.sidebar.selectbox("Período de Análise", ["6mo", "1y", "2y", "5y"], index=1)
    
    return asset_classes, universe, strategy, capital, period

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

def render_disclaimer():
    st.markdown("---")
    st.warning(
        "⚠️ **AVISO LEGAL**: Esta ferramenta tem finalidade estritamente **EDUCACIONAL**. "
        "Os dados apresentados não constituem recomendação de compra ou venda de ativos. "
        "Rentabilidade passada não é garantia de resultados futuros. "
        "Consulte um profissional certificado antes de investir."
    )
