import streamlit as st
import pandas as pd

st.title("Inteligencia de Dados")
try:
    df = pd.read_csv('data/vendas_brutas.csv')
    st.write("### Visão Geral de Vendas")
    st.line_chart(df.groupby('data_venda')['faturamento'].sum())
    st.metric("Faturamento Total", f"R$ {df['faturamento'].sum():,.2f}")
except:
    st.error("Rode 'python src/data_ingestion.py' primeiro!")