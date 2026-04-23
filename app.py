import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title("📊 Dashboard Farmacêutico")

# =========================
# CARREGAR DADOS
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/silver.csv")
    df['data'] = pd.to_datetime(df['data'])
    return df

df = load_data()

# =========================
# FILTROS
# =========================
st.sidebar.header("Filtros")

empresa = st.sidebar.multiselect(
    "Empresa",
    df['empresa'].unique(),
    default=df['empresa'].unique()
)

regiao = st.sidebar.multiselect(
    "Região",
    df['regiao'].dropna().unique(),
    default=df['regiao'].dropna().unique()
)

df_filtro = df[
    (df['empresa'].isin(empresa)) &
    (df['regiao'].isin(regiao))
]

# =========================
# KPIs (NumPy)
# =========================
precos = df_filtro['preco_unitario'].values
receita = df_filtro['receita'].values
volume = df_filtro['volume'].values

col1, col2, col3 = st.columns(3)

df_filtro['receita'] = pd.to_numeric(df_filtro['receita'], errors='coerce')
df_filtro['preco_unitario'] = pd.to_numeric(df_filtro['preco_unitario'], errors='coerce')
df_filtro['volume'] = pd.to_numeric(df_filtro['volume'], errors='coerce')

df_filtro = df_filtro.fillna(0)
# =========================
# GRÁFICOS
# =========================
st.subheader("📈 Evolução de Preço")

st.line_chart(
    df_filtro.groupby('data')['preco_unitario'].mean()
)

st.subheader("📊 Receita por Produto")

st.bar_chart(
    df_filtro.groupby('produto_id')['receita'].sum()
)

st.subheader("🌎 Receita por Região")

st.bar_chart(
    df_filtro.groupby('regiao')['receita'].sum()
)

# =========================
# ANÁLISE
# =========================
st.subheader("📉 Estatísticas")

st.write("Desvio padrão:", np.std(precos))
st.write("Mediana:", np.median(precos))

# =========================
# TABELA
# =========================
st.subheader("📋 Dados")

st.dataframe(df_filtro)