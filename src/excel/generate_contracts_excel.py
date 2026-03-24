import pandas as pd
import os
from src.filtros.base_dia import filtre_base_dia
from src.filtros.novos import filtre_novos
from src.filtros.base_dia_focos import filtre_base_dia_focos
from datetime import datetime


def generate_contracts_excel(modo: str, sheets_selecionadas=None):

    if modo == "Focos":
        df_final = filtre_base_dia_focos(sheets_selecionadas)

    elif modo == "Dia":
        df_final = filtre_base_dia(sheets_selecionadas)

    elif modo == "Novos":
        df_final = filtre_novos(sheets_selecionadas)

    else:
        raise ValueError("Modo inválido")

    pasta_destino = os.getenv("CAMINHO_BASE")
    os.makedirs(pasta_destino, exist_ok=True)

    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    nome_arquivo = f"contratos_{modo}_{agora}.xlsx"

    caminho_saida = os.path.join(
        pasta_destino,
        nome_arquivo
    )

    df_final.to_excel(caminho_saida, index=False)

    print("Excel de contratos gerado")
    print("Total de contratos:", len(df_final))

    return caminho_saida