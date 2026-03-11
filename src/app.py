import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px # Para gráficos mais profissionais

st.set_page_config(page_title="Simulado - Data Intelligence", layout="wide")

st.title("🚀 Simulado - Intelligence Hub")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Simulação de Crescimento")
crescimento_2025 = st.sidebar.slider("Crescimento 2025 (%)", 0, 20, 8) / 100
crescimento_2026 = st.sidebar.slider("Crescimento 2026 (%)", 0, 20, 10) / 100

try:
    df = pd.read_csv('data/vendas_brutas.csv')
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    
    # Criando abas para diferentes análises
    tab_previsao, tab_abc = st.tabs(["📈 Previsão de Demanda", "🎯 Estratégia de Produtos (ABC)"])

    with tab_previsao:
        st.subheader("Projeção de Faturamento 2026")
        fator = (1 + crescimento_2025) * (1 + crescimento_2026)
        
        df_diario = df.groupby('data_venda')['faturamento'].sum().reset_index()
        df_2026 = df_diario.copy()
        df_2026['faturamento'] = df_2026['faturamento'] * fator
        df_2026['Dia_Mes'] = df_2026['data_venda'].dt.strftime('%m-%d')
        df_diario['Dia_Mes'] = df_diario['data_venda'].dt.strftime('%m-%d')

        col1, col2, col3 = st.columns(3)
        col1.metric("Real 2024", f"R$ {df['faturamento'].sum():,.2f}")
        col2.metric("Projeção 2026", f"R$ {df['faturamento'].sum() * fator:,.2f}")
        col3.metric("CAGR Simulado", f"{((fator**(1/2)-1)*100):.1f}% ao ano")

        chart_data = pd.merge(df_diario[['Dia_Mes', 'faturamento']], 
                              df_2026[['Dia_Mes', 'faturamento']], 
                              on='Dia_Mes', suffixes=('_2024', '_2026')).set_index('Dia_Mes')
        st.line_chart(chart_data)

    with tab_abc:
        st.subheader("Análise de Pareto - Curva ABC")
        st.markdown("Identificação dos produtos que geram **80% do faturamento**.")

        # Lógica da Curva ABC
        abc = df.groupby('produto')['faturamento'].sum().sort_values(ascending=False).reset_index()
        abc['perc_total'] = abc['faturamento'] / abc['faturamento'].sum()
        abc['perc_acumulado'] = abc['perc_total'].cumsum()
        
        # Classificação
        abc['Classe'] = np.where(abc['perc_acumulado'] <= 0.8, 'A (Alta Relevância)',
                        np.where(abc['perc_acumulado'] <= 0.95, 'B (Médio Impacto)', 'C (Baixo Giro)'))

        col_left, col_right = st.columns([1, 1])

        with col_left:
            fig_pie = px.pie(abc, values='faturamento', names='Classe', 
                             title="Distribuição por Classe",
                             color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_pie)

        with col_right:
            st.write("### Detalhamento por Produto")
            st.dataframe(abc[['produto', 'faturamento', 'Classe']].style.format({'faturamento': 'R$ {:,.2f}'}))

        st.info("💡 **Dica de Negócio:** Produtos Classe A devem ter prioridade total no estoque para evitar ruptura (falta de produto).")

except Exception as e:
    st.error(f"Erro ao carregar dados. Rode os scripts .py primeiro! {e}")