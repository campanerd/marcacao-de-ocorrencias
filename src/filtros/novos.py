from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import os

# carregar variáveis de ambiente
load_dotenv()
def filtre_novos():
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
    df = pd.read_excel(caminho_origem, sheet_name="BASE")

    if "CONTRATO" not in df.columns:
        raise ValueError("A coluna 'CONTRATO' não existe na sheet BASE")

    df_final = df[["CONTRATO"]].dropna()


    # remover valores vazios
    df_final = df_final.dropna()

    return df_final

