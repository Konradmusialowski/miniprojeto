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
Q1 = df_filtro['preco_unitario'].quantile(0.25)
Q3 = df_filtro['preco_unitario'].quantile(0.75)
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

df_sem_outlier = df_filtro[
    (df_filtro['preco_unitario'] >= limite_inferior) &
    (df_filtro['preco_unitario'] <= limite_superior)
]

np.mean(df_sem_outlier['preco_unitario'])
preco = df_filtro['preco_unitario']

preco_norm = (preco - preco.min()) / (preco.max() - preco.min())

df_filtro['preco_normalizado'] = preco_norm
media = np.mean(preco)
desvio = np.std(preco)

z_score = (preco - media) / desvio

df_filtro['preco_zscore'] = z_score
df_filtro['preco_log'] = np.log1p(df_filtro['preco_unitario'])
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

receita = df_filtro['receita'].values
volume = df_filtro['volume'].values
precos = df_filtro['preco_unitario'].values

kpi_receita = np.sum(receita)
kpi_volume = np.sum(volume)
kpi_preco_medio = np.mean(precos)
kpi_preco_min = np.min(precos)
kpi_preco_max = np.max(precos)

col1, col2, col3 = st.columns(3)

col1.metric("💰 Receita Total", f"{kpi_receita:,.2f}")
col2.metric("📦 Volume Total", f"{kpi_volume:,.0f}")
col3.metric("💲 Preço Médio", f"{kpi_preco_medio:,.2f}")

ticket_medio = kpi_receita / kpi_volume
st.metric("🧾 Ticket Médio", f"{ticket_medio:,.2f}")

df_comp = df_filtro.groupby('empresa')['receita'].sum().reset_index()

df_empresa = df_filtro.groupby('empresa')['receita'].sum()
st.bar_chart(df_empresa)
#Por região ###
df_regiao = df_filtro.groupby('regiao')['receita'].sum()
st.bar_chart(df_regiao)

st.subheader("🏆 Comparação de Receita")
st.bar_chart(df_comp.set_index('empresa'))

variacao = ((kpi_preco_max - kpi_preco_min) / kpi_preco_min) * 100
st.metric("📊 Variação de Preço (%)", f"{variacao:.2f}%")

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
