import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Simulado-Previsão de Faturamento", layout="wide")

st.title("📊 SIMULADO - Intelligence & Demand Planning")

# Barra lateral para simulação
st.sidebar.header("Parâmetros de Crescimento")
crescimento_2025 = st.sidebar.slider("Crescimento esperado 2025 (%)", 0, 20, 8) / 100
crescimento_2026 = st.sidebar.slider("Crescimento esperado 2026 (%)", 0, 20, 10) / 100

try:
    # 1. Carregar dados reais de 2024
    df = pd.read_csv('data/vendas_brutas.csv')
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    df_diario = df.groupby('data_venda')['faturamento'].sum().reset_index()
    
    # 2. Calcular Projeção 2026 (Sazonalidade 2024 * Crescimento Composto)
    # Fator total = (1 + growth25) * (1 + growth26)
    fator_acumulado = (1 + crescimento_2025) * (1 + crescimento_2026)
    
    df_2026 = df_diario.copy()
    df_2026['data_venda'] = df_2026['data_venda'] + pd.DateOffset(years=2)
    df_2026['faturamento'] = df_2026['faturamento'] * fator_acumulado
    df_2026['Tipo'] = 'Projeção 2026'
    
    df_diario['Tipo'] = 'Real 2024'
    
    # 3. Métricas de Negócio
    fat_2024 = df['faturamento'].sum()
    fat_2026 = fat_2024 * fator_acumulado
    
    col1, col2 = st.columns(2)
    col1.metric("Faturamento Real 2024", f"R$ {fat_2024:,.2f}")
    col2.metric("Projeção 2026 (Simulada)", f"R$ {fat_2026:,.2f}", 
                delta=f"{((fator_acumulado-1)*100):.1f}% acumulado")

    # 4. Gráfico Comparativo
    st.write("### Comparativo: Sazonalidade 2024 vs Projeção 2026")
    
    # Combinar dados para o gráfico
    df_concat = pd.concat([df_diario, df_2026])
    
    # Criar abas para organizar a visão
    tab1, tab2 = st.tabs(["Gráfico de Tendência", "Dados Brutos"])
    
    with tab1:
        # Criamos um gráfico onde o eixo X ignora o ano para sobrepor as linhas
        df_diario['Dia_Mes'] = df_diario['data_venda'].dt.strftime('%m-%d')
        df_2026['Dia_Mes'] = df_2026['data_venda'].dt.strftime('%m-%d')
        
        chart_data = pd.merge(
            df_diario[['Dia_Mes', 'faturamento']], 
            df_2026[['Dia_Mes', 'faturamento']], 
            on='Dia_Mes', suffixes=('_2024', '_2026')
        ).set_index('Dia_Mes')
        
        st.line_chart(chart_data)

    with tab2:
        st.dataframe(df_2026[['data_venda', 'faturamento']].head(10))

except Exception as e:
    st.error(f"Certifique-se de rodar os scripts de dados primeiro! Erro: {e}")