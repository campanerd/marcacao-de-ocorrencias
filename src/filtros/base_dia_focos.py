from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import os

# carregar variáveis de ambiente
load_dotenv()
def filtre_base_dia_focos():
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

    # ler todas as sheets
    sheets = pd.read_excel(caminho_origem, sheet_name=None)

    # extrair a coluna CONTRATO apenas das sheets que possuem essa coluna
    dfs = []

    #debugar quais sheets ta lendo
    sheets_lidas = []


    for nome_sheet, df in sheets.items():
        if nome_sheet.startswith("NU"):
            if "CONTRATO" in df.columns:
                sheets_lidas.append(nome_sheet)
                dfs.append(df[["CONTRATO"]])


    if not dfs:
        raise ValueError("Nenhuma sheet contém a coluna 'CONTRATO'")

    #juntar todas as colunas em uma só
    df_final = pd.concat(dfs, ignore_index=True)

    # remover valores vazios
    df_final = df_final.dropna()

    return df_final, sheets_lidas


