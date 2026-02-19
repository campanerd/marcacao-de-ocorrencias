from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

pasta = os.getenv("CAMINHO_BASE")

if not pasta:
    raise ValueError("CAMINHO_BASE não encontrado no .env")

# data no formato DD.MM
data_hoje = datetime.now().strftime("%d.%m")

arquivo = f"BASE DIA FOCOS {data_hoje}.xlsx"
caminho_arquivo = os.path.join(pasta, arquivo)

print("Tentando abrir:", caminho_arquivo)

df = pd.read_excel(caminho_arquivo)
