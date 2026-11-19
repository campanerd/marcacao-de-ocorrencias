import os
import pandas as pd

COLUNA_CONTRATO = "Número Contrato"
COLUNA_TELEFONE = "DDD+Telefone"


def _ler_csv(caminho):
    try:
        return pd.read_csv(caminho, sep=";", dtype=str, encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(caminho, sep=";", dtype=str, encoding="cp1252")


def ler_contratos_e_telefones(caminho):
    df = _ler_csv(caminho)

    for coluna in (COLUNA_CONTRATO, COLUNA_TELEFONE):
        if coluna not in df.columns:
            raise ValueError(
                f"Coluna '{coluna}' não encontrada em {os.path.basename(caminho)}"
            )

    df = df[[COLUNA_CONTRATO, COLUNA_TELEFONE]].dropna().copy()
    df[COLUNA_CONTRATO] = df[COLUNA_CONTRATO].str.strip()
    df[COLUNA_TELEFONE] = df[COLUNA_TELEFONE].str.replace(r"\D", "", regex=True)

    df = df[(df[COLUNA_CONTRATO] != "") & (df[COLUNA_TELEFONE] != "")]
    df = df.drop_duplicates()

    return list(df.itertuples(index=False, name=None))
