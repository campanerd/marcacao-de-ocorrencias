from src.excel.generate_contracts_excel import generate_contracts_excel
from src.macro.excel_reader import read_contracts_from_excel
from src.macro.db import get_sql_connection
from src.macro.temp_tables import create_temp_contract_table
from src.exporters.csv_exporter import export_csv_for_creditor
import os


def run_pipeline():
    # gera o excel automaticamente
    excel_path = generate_contracts_excel()

    base_filename = os.path.splitext(
        os.path.basename(excel_path)
    )[0]

    # credores
    credores = [
        "Daycoval Veiculos",
        "Daycoval Juridico",
        "Daycoval Focos",
        "Daycoval Daycred"
    ]

    titulo_ocor = "SMS Enviado"
    complemento = "Ação Massiva"

    # lê contratos
    contracts = read_contracts_from_excel(excel_path)

    # conecta no banco
    conn = get_sql_connection()
    cursor = conn.cursor()

    #tabela temporária
    create_temp_contract_table(cursor, contracts)
    conn.commit()

    # sql
    sql = """
IF OBJECT_ID('tempdb..##Esp') IS NOT NULL DROP TABLE ##Esp;

SELECT DISTINCT
    CAST(A.cod_cred AS VARCHAR)                  AS [Código do Credor],
    '11'                                         AS Operação,
    RTRIM(A.cpfcgc_pes)                          AS [CPF/CNPJ],
    RTRIM(A.CONTRATO_TIT)                        AS Contrato,
    ?                                            AS [Título da Ocorrência],
    ?                                            AS Complemento,
    ' '                                           AS [Data de Promessa],
    FORMAT(GETDATE(),'dd/MM/yyyy HH:mm')         AS [Data/Hora da Ocorrência],
    ' '                                           AS [Código do Usuário],
    ' '                                           AS [Nome do Usuário],
    ' '                                           AS [Número da parcela?]
INTO ##Esp
FROM [192.168.0.143].cobreports.dbo.POSICAO_CARTEIRA A WITH(NOLOCK)

INNER JOIN [192.168.0.143].cobsystems3.dbo.V_DEVEDORES B WITH(NOLOCK)
    ON A.CPFCGC_PES = B.CPFCGC_PES COLLATE Latin1_General_CI_AI

INNER JOIN [192.168.0.143].cobsystems3.dbo.PESSOAS_TELEFONES C WITH(NOLOCK)
    ON B.COD_PES = C.COD_PES

INNER JOIN [192.168.0.143].cobsystems3.dbo.TELEFONES_STATUS D WITH(NOLOCK)
    ON C.STATUS_TEL = D.COD_STAT

INNER JOIN [192.168.0.143].cobsystems3.dbo.OCORRENCIAS_CLIENTES E WITH(NOLOCK)
    ON A.COD_OCOR = E.COD_OCOR

INNER JOIN #Contratos T
    ON RTRIM(A.CONTRATO_TIT) COLLATE SQL_Latin1_General_CP1_CI_AS
     = T.Contrato        COLLATE SQL_Latin1_General_CP1_CI_AS

WHERE A.nome_cred = ?
  AND C.ddd_tel IS NOT NULL
  AND C.ddd_tel <> ' '
  AND LEFT(C.Nr_tel,1) = '9'
  AND LEN(C.Nr_tel) = 9
  AND C.STATUS_TEL IN (1,3)
"""

    #gera CSV por credor
    for creditor in credores:
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

    downloads = os.path.join("src", "downloads")

    if os.path.exists(downloads):
        for arquivo in os.listdir(downloads):
            caminho_arquivo = os.path.join(downloads, arquivo)

            if arquivo == "contratos_COMPLETO.xlsx":
                try:
                    os.remove(caminho_arquivo)
                    print(f"Removido: {arquivo}")
                except Exception as e:
                    print(f"Erro ao remover {arquivo}: {e}")


if __name__ == "__main__":
    run_pipeline()