import pandas as pd


def listar_sheets(caminho_arquivo, prefixo=None, coluna_obrigatoria=None):
    sheets_validas = []

    # abre o arquivo uma vez e lê só o cabeçalho (0 linhas) de cada sheet
    with pd.ExcelFile(caminho_arquivo) as arquivo:
        for nome_sheet in arquivo.sheet_names:
            if prefixo and not nome_sheet.startswith(prefixo):
                continue

            if coluna_obrigatoria:
                cabecalho = arquivo.parse(nome_sheet, nrows=0)
                if coluna_obrigatoria not in cabecalho.columns:
                    continue

            sheets_validas.append(nome_sheet)

    return sheets_validas


def processar_sheets(caminho_arquivo, sheets_selecionadas, coluna="CONTRATO"):
    if not sheets_selecionadas:
        raise ValueError("Nenhuma sheet válida selecionada")

    # lê só as sheets marcadas e só a coluna necessária
    sheets = pd.read_excel(
        caminho_arquivo, sheet_name=list(sheets_selecionadas), usecols=[coluna]
    )
    df_final = pd.concat(sheets.values(), ignore_index=True)

    return df_final.dropna()