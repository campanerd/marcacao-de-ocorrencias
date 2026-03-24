import pandas as pd


def listar_sheets(caminho_arquivo, prefixo=None, coluna_obrigatoria=None):
    sheets = pd.read_excel(caminho_arquivo, sheet_name=None)

    sheets_validas = []

    for nome_sheet, df in sheets.items():
        if prefixo and not nome_sheet.startswith(prefixo):
            continue

        if coluna_obrigatoria and coluna_obrigatoria not in df.columns:
            continue

        sheets_validas.append(nome_sheet)

    return sheets_validas


def processar_sheets(caminho_arquivo, sheets_selecionadas, coluna="CONTRATO"):
    sheets = pd.read_excel(caminho_arquivo, sheet_name=None)

    dfs = []

    for nome in sheets_selecionadas:
        df = sheets[nome]
        dfs.append(df[[coluna]])

    if not dfs:
        raise ValueError("Nenhuma sheet válida selecionada")

    df_final = pd.concat(dfs, ignore_index=True)

    return df_final.dropna()