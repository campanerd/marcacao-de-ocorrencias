import os

from src.backend.domain.rcs.regras import (
    CREDORES,
    TITULO_OCORRENCIA,
    COMPLEMENTO_PADRAO,
)
from src.backend.infrastructure.database.db import get_sql_connection
from src.backend.infrastructure.database.temp_tables import create_temp_contract_phone_table
from src.backend.infrastructure.files.csv_exporter import export_csv_for_creditor
from src.backend.infrastructure.files.csv_reader import ler_contratos_e_telefones
from src.backend.infrastructure.files.paths import pasta_rcs

SQL_RCS = """
IF OBJECT_ID('tempdb..##Esp') IS NOT NULL DROP TABLE ##Esp;

SELECT DISTINCT
    CAST(A.cod_cred AS VARCHAR)                  AS [Código do Credor],
    '11'                                         AS Operação,
    RTRIM(A.cpfcgc_pes)                          AS [CPF/CNPJ],
    RTRIM(A.CONTRATO_TIT)                        AS Contrato,
    ?                                            AS [Título da Ocorrência],
    LTRIM(CONCAT(?, ' ', T.Telefone))            AS Complemento,
    ' '                                          AS [Data de Promessa],
    FORMAT(GETDATE(),'dd/MM/yyyy HH:mm')         AS [Data/Hora da Ocorrência],
    ' '                                          AS [Código do Usuário],
    ' '                                          AS [Nome do Usuário],
    ' '                                          AS [Número da parcela?]
INTO ##Esp
FROM [192.168.0.143].cobreports.dbo.POSICAO_CARTEIRA A WITH(NOLOCK)

INNER JOIN [192.168.0.143].cobsystems3.dbo.OCORRENCIAS_CLIENTES E WITH(NOLOCK)
    ON A.COD_OCOR = E.COD_OCOR

INNER JOIN #Contratos T
    ON RTRIM(A.CONTRATO_TIT) COLLATE SQL_Latin1_General_CP1_CI_AS
     = T.Contrato            COLLATE SQL_Latin1_General_CP1_CI_AS

WHERE A.nome_cred = ?
"""


def run_pipeline(arquivos):
    conn = get_sql_connection()
    cursor = conn.cursor()

    arquivos_gerados = []

    for arquivo in arquivos:
        caminho = os.path.join(pasta_rcs(), arquivo.nome)
        base_filename = os.path.splitext(arquivo.nome)[0]

        linhas = ler_contratos_e_telefones(caminho)
        print(f"{arquivo.nome}: {len(linhas)} contrato(s)/telefone(s) lido(s)")

        create_temp_contract_phone_table(cursor, linhas)
        conn.commit()

        for creditor in CREDORES:
            caminho_csv = export_csv_for_creditor(
                conn,
                cursor,
                SQL_RCS,
                creditor,
                TITULO_OCORRENCIA,
                COMPLEMENTO_PADRAO,
                base_filename,
            )
            if caminho_csv:
                arquivos_gerados.append({"credor": creditor, "path": caminho_csv})

    cursor.close()
    conn.close()

    print("Pipeline RCS finalizado com sucesso!")
    return arquivos_gerados