from excel.generate_contracts_excel import generate_contracts_excel
from macro.excel_reader import read_contracts_from_excel
from macro.db import get_sql_connection
from macro.temp_tables import create_temp_contract_table
from exporters.csv_exporter import export_csv_for_creditor
import os


def run_pipeline():
    # gera o excel automaticamente
    excel_path = generate_contracts_excel()

    base_filename = os.path.splitext(
        os.path.basename(excel_path)
    )[0]

    # credores
    creditors = [
        "Daycoval Veiculos",
        "Daycoval Juridico",
        "Daycoval Focos",
        "Daycoval Daycred"
    ]

    titulo_ocor = "TITULO DA OCORRENCIA"
    complemento = "COMPLEMENTO"

    # lê contratos
    contracts = read_contracts_from_excel(excel_path)

    # conecta no banco
    conn = get_sql_connection()
    cursor = conn.cursor()

    #tabela temporária
    create_temp_contract_table(cursor, contracts)
    conn.commit()

    # sql
    sql = """ SUA QUERY AQUI """

    #gera CSV por credor
    for creditor in creditors:
        export_csv_for_creditor(
            conn,
            cursor,
            sql,
            creditor,
            titulo_ocor,
            complemento,
            base_filename
        )

    cursor.close()
    conn.close()

    print("Pipeline finalizado com sucesso!")


if __name__ == "__main__":
    run_pipeline()