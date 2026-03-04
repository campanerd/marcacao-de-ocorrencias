import pandas as pd
import os
from src.filtros.base_dia import filtre_base_dia
from src.filtros.novos import filtre_novos
from src.filtros.base_dia_focos import filtre_base_dia_focos


def generate_contracts_excel():
    df_base, sheets_base = filtre_base_dia()
    df_novos = filtre_novos()
    df_focos, sheets_base_focos = filtre_base_dia_focos()

    print("Sheets processadas:", sheets_base)
    print("Sheets processadas (Focos):", sheets_base_focos)

    df_final = (
        pd.concat([df_base, df_novos, df_focos], ignore_index=True)
        .dropna()
        .drop_duplicates()
    )

    pasta_destino = os.path.join("src", "downloads")
    os.makedirs(pasta_destino, exist_ok=True)

    caminho_saida = os.path.join(
        pasta_destino,
        "contratos_COMPLETO.xlsx"
    )

    df_final.to_excel(caminho_saida, index=False)

    print("Excel de contratos gerado")
    print("Total de contratos:", len(df_final))

    return caminho_saida