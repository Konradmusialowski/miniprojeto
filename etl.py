import pandas as pd
import numpy as np
import os

# =========================
# CAMINHOS
# =========================
RAW_PATH = "data/"
SILVER_PATH = "data/processed/"
GOLD_PATH = "data/gold/"

os.makedirs(SILVER_PATH, exist_ok=True)
os.makedirs(GOLD_PATH, exist_ok=True)




# =========================
# EXTRAÇÃO (BRONZE)
# =========================
fato = pd.read_csv(RAW_PATH + "fato_vendas.csv")
produto = pd.read_csv(RAW_PATH + "dim_produto.csv")
filial = pd.read_csv(RAW_PATH + "dim_filial.csv")

# =========================
# TRANSFORMAÇÃO (SILVER)
# =========================
fato['data'] = pd.to_datetime(fato['data'])

# Limpeza com NumPy
fato['preco_unitario'] = np.where(
    fato['preco_unitario'] <= 0,
    np.nan,
    fato['preco_unitario']
)

fato['preco_unitario'] = np.nan_to_num(
    fato['preco_unitario'],
    nan=np.mean(fato['preco_unitario'])
)

fato=fato.drop.duplicates()

# Join
df = fato.merge(produto, on="produto_id", how="left") \
         .merge(filial, on="filial_id", how="left")

# Salvar SILVER
df.to_csv(SILVER_PATH + "silver.csv", index=False)

# =========================
# SCD TIPO 2 (GOLD)
# =========================
gold = pd.DataFrame(columns=[
    'sk_produto',
    'id_produto_original',
    'valor_produto',
    'data_inicio_validade',
    'data_fim_validade',
    'flag_ativo'
])

sk = 1

for _, row in df.sort_values('data').iterrows():
    prod = row['produto_id']
    valor = row['preco_unitario']
    data = row['data']

    ativo = gold[
        (gold['id_produto_original'] == prod) &
        (gold['flag_ativo'] == True)
    ]

    if ativo.empty:
        gold.loc[len(gold)] = [sk, prod, valor, data, None, True]
        sk += 1
    else:
        valor_atual = ativo.iloc[0]['valor_produto']

        if not np.isclose(valor, valor_atual):
            idx = ativo.index[0]
            gold.at[idx, 'data_fim_validade'] = data
            gold.at[idx, 'flag_ativo'] = False

            gold.loc[len(gold)] = [sk, prod, valor, data, None, True]
            sk += 1

# Salvar GOLD
gold.to_csv(GOLD_PATH + "gold_produto.csv", index=False)

print("ETL finalizado com sucesso!")
import pandas as pd

df_test = pd.DataFrame({
    "produto_id": ["P001", "P001"],
    "preco_unitario": [10.0, 15.0],
    "data": ["2025-01-01", "2025-02-01"]
})

df_test['data'] = pd.to_datetime(df_test['data'])
