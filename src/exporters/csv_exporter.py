import pandas as pd
import os
from datetime import datetime


def export_csv_for_creditor(
    conn,
    cursor,
    sql,
    creditor,
    titulo_ocor,
    complemento,
    base_filename,
    output_dir="src/downloads"
):
    """
    Executa a query para um credor específico e exporta o resultado em CSV.
    """

    # garante pasta de saída
    os.makedirs(output_dir, exist_ok=True)

    creditor_safe = creditor.replace(" ", "_")

    # executa a query
    cursor.execute(
        sql,
        titulo_ocor,
        complemento,
        creditor
    )
    conn.commit()

    # lê dados da tabela temporária global
    df = pd.read_sql(
        "SELECT * FROM tempdb.dbo.##Esp",
        conn
    )

    if df.empty:
        print(f"Nenhum registro para o credor: {creditor}")
        return None

    nome_csv = (
        f"{base_filename}_"
        f"{creditor_safe}_"
        f"{datetime.now().strftime('%d.%m.%Y')}.csv"
    )

    caminho_saida = os.path.abspath(os.path.join(output_dir, nome_csv))

    df.to_csv(
        caminho_saida,
        index=False,
        sep=";",
        encoding="utf-8-sig"
    )

    print(f"CSV gerado: {caminho_saida}")
    return caminho_saida