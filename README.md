# 📊 Dashboard de Vendas Farmacêuticas com SCD Tipo 2

## 🎯 Objetivo

Este projeto tem como objetivo desenvolver um pipeline de dados completo (ETL) e um dashboard interativo para análise de vendas farmacêuticas, simulando dados do mercado (modelo IQVIA).

O projeto implementa o conceito de **SCD Tipo 2 (Slowly Changing Dimension)**, permitindo o acompanhamento histórico de mudanças nos produtos, como variações de preço.

---

## 🧱 Arquitetura do Projeto

```
data/
 ├── raw/        # Dados brutos (Bronze)
 ├── processed/  # Dados tratados (Silver)
 └── gold/       # Dados modelados com SCD Tipo 2

app.py           # Dashboard em Streamlit
etl.py           # Pipeline de transformação
requirements.txt # Dependências
README.md
```

---

## ⚙️ Tecnologias Utilizadas

* Python
* Pandas
* NumPy
* Streamlit
* Seaborn / Matplotlib
* Git / GitHub

---

## 🔄 Pipeline ETL

### 🟤 Bronze (Raw)

* Ingestão de dados CSV
* Sem tratamento

### ⚪ Silver (Processed)

* Limpeza de dados
* Conversão de tipos
* Remoção de duplicados

### 🟡 Gold (SCD Tipo 2)

* Controle de histórico de produtos
* Criação de colunas:

  * `sk_produto`
  * `data_inicio_validade`
  * `data_fim_validade`
  * `flag_ativo`

---

## 🧠 SCD Tipo 2 (Implementação)

O sistema mantém histórico completo de alterações:

* Novo registro → inserido normalmente
* Alteração de preço →

  * registro antigo é fechado (`data_fim_validade`)
  * novo registro é criado com nova vigência
* Registro atual → `flag_ativo = TRUE`

---

## 📊 Dashboard (Streamlit)

### KPIs Principais

* 📈 Market Share (Clamed vs Concorrência)
* 💲 Gap de Preço Médio
* 🚀 Brick com maior potencial de crescimento

---

### Visualizações

* 🔥 Heatmap de Volume por Brick
* 📈 Evolução temporal de vendas
* 📦 Boxplot (detecção de outliers)
* 🏆 Ranking de vendas por região/produto
* 🚨 Identificação de produtos discrepantes

---

### 🎛️ Filtros Dinâmicos

* Empresa
* Região
* Brick
* Categoria
* Período (mês)

---

## 🧪 Análises Avançadas

* Detecção de outliers (IQR e Z-score)
* Normalização de dados
* Log transform
* Análise de variabilidade de preço
* Identificação de produtos com maior discrepância

---

## 🚀 Como executar o projeto

### 1. Clonar repositório

```
git clone https://https://github.com/Konradmusialowski/miniprojeto
```

### 2. Criar ambiente virtual

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```
pip install -r requirements.txt
```

### 4. Executar dashboard

```
streamlit run app.py
```

---

## ☁️ Deploy

O projeto pode ser executado via:

* Streamlit Cloud
* GitHub

---

## 📌 Insights do Projeto

* Identificação de produtos com preços fora do padrão
* Detecção de oportunidades de crescimento por região (Brick)
* Análise competitiva entre Clamed e concorrentes
* Monitoramento histórico de preços (SCD Tipo 2)

---

## 👨‍💻 Autor

Projeto desenvolvido para fins acadêmicos e de análise de dados.
