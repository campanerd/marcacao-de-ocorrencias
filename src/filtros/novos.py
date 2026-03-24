from src.excel.checkbox import listar_sheets, processar_sheets
from datetime import datetime
from dotenv import load_dotenv

import os

# carregar variáveis de ambiente
load_dotenv()
def filtre_novos(sheets_selecionadas: list):
    # caminho base vindo do .env
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

    #juntar todas as colunas em uma só
    df_final = processar_sheets(caminho_origem, sheets_selecionadas, coluna="CONTRATO")

    return df_final

def obter_sheets_focos():
    pasta_base = os.getenv("CAMINHO_BASE")

    data_hoje = datetime.now().strftime("%d.%m")
    arquivo_origem = f"NOVOS {data_hoje}.xlsx"
    caminho_origem = os.path.join(pasta_base, arquivo_origem)

    return listar_sheets(
        caminho_origem,
        coluna_obrigatoria="CONTRATO"
    )