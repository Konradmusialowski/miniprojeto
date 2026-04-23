import streamlit as st
import pandas as pd
import numpy as np
from google.cloud import bigquery

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Farmacêutico",
    layout="wide"
)

st.title("📊 Dashboard de Vendas Farmacêuticas")

# =========================
# CLIENTE BIGQUERY (com secrets)
# =========================
@st.cache_resource
def get_client():
    return bigquery.Client.from_service_account_info(
        st.secrets["gcp_service_account"]
    )

# =========================
# CONEXÃO BIGQUERY
# =========================
@st.cache_data(ttl=600)
def load_data():
    client = get_client()

    query = """
    SELECT 
        f.data,
        f.produto_id,
        f.filial_id,
        f.empresa,
        f.volume,
        f.preco_unitario,
        f.receita,
        p.categoria,
        fi.regiao,
        fi.cluster
    FROM `lab365clamed-491112.miniprojeto.fato_vendas` f
    LEFT JOIN `lab365clamed-491112.miniprojeto.dim_produto` p
        ON f.produto_id = p.produto_id
    LEFT JOIN `lab365clamed-491112.miniprojeto.dim_filial` fi
        ON f.filial_id = fi.filial_id
    """

    df = client.query(query).to_dataframe()
    df['data'] = pd.to_datetime(df['data'])

    return df

df = load_data()

# =========================
# SIDEBAR FILTROS
# =========================
st.sidebar.header("🔎 Filtros")

empresa = st.sidebar.multiselect(
    "Empresa",
    options=df['empresa'].unique(),
    default=df['empresa'].unique()
)

regiao = st.sidebar.multiselect(
    "Região",
    options=df['regiao'].dropna().unique(),
    default=df['regiao'].dropna().unique()
)

categoria = st.sidebar.multiselect(
    "Categoria",
    options=df['categoria'].dropna().unique(),
    default=df['categoria'].dropna().unique()
)

data_range = st.sidebar.date_input(
    "Período",
    [df['data'].min(), df['data'].max()]
)

# =========================
# FILTRAR DADOS
# =========================
df_filtro = df[
    (df['empresa'].isin(empresa)) &
    (df['regiao'].isin(regiao)) &
    (df['categoria'].isin(categoria)) &
    (df['data'] >= pd.to_datetime(data_range[0])) &
    (df['data'] <= pd.to_datetime(data_range[1]))
]

# =========================
# KPIs (NumPy)
# =========================
precos = df_filtro['preco_unitario'].values
receita = df_filtro['receita'].values
volume = df_filtro['volume'].values

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Receita Total", f"{np.sum(receita):,.2f}")
col2.metric("📦 Volume Total", f"{np.sum(volume):,.0f}")
col3.metric("💲 Preço Médio", f"{np.mean(precos):,.2f}")
col4.metric("📊 Desvio Padrão", f"{np.std(precos):,.2f}")

# =========================
# GRÁFICO 1 - EVOLUÇÃO
# =========================
st.subheader("📈 Evolução do Preço Médio")

df_time = df_filtro.groupby('data')['preco_unitario'].mean()

st.line_chart(df_time)

# =========================
# GRÁFICO 2 - RECEITA POR PRODUTO
# =========================
st.subheader("📊 Receita por Produto")

df_prod = df_filtro.groupby('produto_id')['receita'].sum().sort_values(ascending=False)

st.bar_chart(df_prod)

# =========================
# GRÁFICO 3 - RECEITA POR REGIÃO
# =========================
st.subheader("🌎 Receita por Região")

df_regiao = df_filtro.groupby('regiao')['receita'].sum()

st.bar_chart(df_regiao)

# =========================
# ANÁLISE NUMPY
# =========================
st.subheader("📉 Análise Estatística")

col1, col2 = st.columns(2)

with col1:
    st.write("**Percentis de Preço**")
    st.write("P25:", np.percentile(precos, 25))
    st.write("P50 (Mediana):", np.percentile(precos, 50))
    st.write("P90:", np.percentile(precos, 90))

with col2:
    st.write("**Correlação**")
    corr = np.corrcoef(df_filtro['volume'], df_filtro['preco_unitario'])
    st.write("Volume vs Preço:", round(corr[0,1], 4))

# =========================
# OUTLIERS
# =========================
st.subheader("🚨 Detecção de Outliers")

media = np.mean(precos)
desvio = np.std(precos)

outliers = df_filtro[np.abs(precos - media) > 3 * desvio]

st.write(f"Quantidade de outliers: {len(outliers)}")

if len(outliers) > 0:
    st.dataframe(outliers)

# =========================
# TABELA FINAL
# =========================
st.subheader("📋 Dados Detalhados")

st.dataframe(df_filtro)
