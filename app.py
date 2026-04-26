import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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

#++++++++++++++++++++++++++++
# seaborn      ##############
sns.set_theme(style="whitegrid")
st.subheader("📈 Evolução de Preço (Seaborn)")

fig, ax = plt.subplots()

sns.lineplot(
    data=df_filtro,
    x="data",
    y="preco_unitario",
    estimator="mean",
    ax=ax
)

ax.set_title("Preço médio ao longo do tempo")
ax.set_xlabel("Data")
ax.set_ylabel("Preço")

st.pyplot(fig)

st.subheader("📊 Receita por Produto")

df_prod = df_filtro.groupby("produto_id")["receita"].sum().reset_index()

fig, ax = plt.subplots()

sns.barplot(
    data=df_prod,
    x="produto_id",
    y="receita",
    ax=ax
)

ax.set_title("Receita por Produto")
ax.set_xlabel("Produto")
ax.set_ylabel("Receita")

plt.xticks(rotation=45)

st.pyplot(fig)

st.subheader("🌎 Receita por Região")

df_reg = df_filtro.groupby("regiao")["receita"].sum().reset_index()

fig, ax = plt.subplots()

sns.barplot(
    data=df_reg,
    x="regiao",
    y="receita",
    ax=ax
)

ax.set_title("Receita por Região")

st.pyplot(fig)

st.subheader("🌎 Receita por Região")

df_reg = df_filtro.groupby("regiao")["receita"].sum().reset_index()

fig, ax = plt.subplots()

sns.barplot(
    data=df_reg,
    x="regiao",
    y="receita",
    ax=ax
)

ax.set_title("Receita por Região")

st.pyplot(fig)

st.subheader("📊 Histórico SCD Tipo 2")

gold = pd.read_csv("data/gold/gold_produto.csv")

gold['data_inicio_validade'] = pd.to_datetime(gold['data_inicio_validade'])
gold['data_fim_validade'] = pd.to_datetime(gold['data_fim_validade'])

st.dataframe(gold)

# =========================
# TABELA
# =========================
st.subheader("📋 Dados")

st.dataframe(df_filtro)
