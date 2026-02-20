from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import os

# carregar variáveis de ambiente
load_dotenv()

# caminho base vindo do .env
pasta_base = os.getenv("CAMINHO_BASE")

if not pasta_base:
    raise ValueError("CAMINHO_BASE não encontrado no .env")

# data no formato DD.MM
data_hoje = datetime.now().strftime("%d.%m")

# arquivo de origem
arquivo_origem = f"NOVOS {data_hoje}.xlsx"
caminho_origem = os.path.join(pasta_base, arquivo_origem)

if not os.path.exists(caminho_origem):
    raise FileNotFoundError(f"Arquivo não encontrado: {caminho_origem}")

# ler todas as sheets
sheets = pd.read_excel(caminho_origem, sheet_name=None)

# extrair a coluna CONTRATO apenas das sheets que possuem essa coluna
dfs = []
for nome_sheet, df in sheets.items():
    if "CONTRATO" in df.columns:
        dfs.append(df[["CONTRATO"]])

if not dfs:
    raise ValueError("Nenhuma sheet contém a coluna 'CONTRATO'")

#juntar todas as colunas em uma só
df_final = pd.concat(dfs, ignore_index=True)

# remover valores vazios
df_final = df_final.dropna()

# pasta de destino
pasta_destino = os.path.join("src", "downloads")
os.makedirs(pasta_destino, exist_ok=True)

# nome do arquivo de saída
arquivo_saida = "contratos_NOVOS.xlsx"
caminho_saida = os.path.join(pasta_destino, arquivo_saida)

# salvar o novo Excel
df_final.to_excel(caminho_saida, index=False)

print("Arquivo criado com sucesso em:", caminho_saida)
print("Total de contratos extraídos:", len(df_final))
