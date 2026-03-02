import pandas as pd


def read_contracts_from_excel(excel_path):
    """
    Lê o Excel e retorna a lista de contratos
    """
    df = pd.read_excel(excel_path)

    if "CONTRATO" not in df.columns:
        raise Exception("Coluna 'CONTRATO' não encontrada no Excel")

    contracts = (
        df["CONTRATO"]
        .astype(str)
        .str.strip()
        .tolist()
    )

    if not contracts:
        raise Exception("Nenhum contrato encontrado no Excel")

    return contracts