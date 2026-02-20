from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

pasta_base = os.getenv("CAMINHO_BASE")

if not pasta_base:
    raise ValueError("CAMINHO_BASE não encontrado no .env")

# data no formato DD.MM
data_hoje = datetime.now().strftime("%d.%m")

# arquivo de origem
arquivo_origem = f"BASE DIA FOCOS {data_hoje}.xlsx"
caminho_origem = os.path.join(pasta_base, arquivo_origem)

if not os.path.exists(caminho_origem):
    raise FileNotFoundError(f"Arquivo não encontrado: {caminho_origem}")

# ler apenas a sheet desejada
df = pd.read_excel(
    caminho_origem,
    sheet_name="NU-B123",
    usecols=["CONTRATO"]
)

# pasta de destino
pasta_destino = os.path.join("src", "downloads")
os.makedirs(pasta_destino, exist_ok=True)

# nome do novo arquivo
arquivo_saida = "contratos_BASE_DIA_FOCOS.xlsx"
caminho_saida = os.path.join(pasta_destino, arquivo_saida)

# salvar novo Excel
df.to_excel(caminho_saida, index=False)

print("Arquivo criado com sucesso em:", caminho_saida)