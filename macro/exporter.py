import pandas as pd
from datetime import datetime


def export_csv_for_creditor(
    conn,
    cursor,
    sql,
    creditor,
    titulo_ocor,
    complemento,
    base_filename
):
    """
    Executa o SQL para um credor e gera o CSV
    """
    creditor_file = creditor.replace(" ", "_")

    cursor.execute(sql, [titulo_ocor, complemento, creditor])
    conn.commit()

    df = pd.read_sql(
        "SELECT * FROM tempdb.dbo.##Esp",
        conn
    )

    csv_name = (
        f"{base_filename}_"
        f"{creditor_file}_"
        f"{datetime.now().strftime('%d.%m.%Y')}.csv"
    )

    df.to_csv(
        csv_name,
        index=False,
        sep=";",
        encoding="utf-8-sig"
    )

    print(f"✅ CSV gerado para: {creditor}")