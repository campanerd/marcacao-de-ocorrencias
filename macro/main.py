from tkinter import Tk, filedialog
import os

from excel_reader import read_contracts_from_excel
from db import get_sql_connection
from temp_tables import create_temp_contract_table
from exporter import export_csv_for_creditor



#escolhendo arq excel
Tk().withdraw()

excel_path = filedialog.askopenfilename(
    title="Escolha o arquivo Excel",
    filetypes=[("Arquivos Excel", "*.xlsx")]
)

if not excel_path:
    raise Exception("Nenhum arquivo selecionado")

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



#lendo contratos
contracts = read_contracts_from_excel(excel_path)



# conectando sql

conn = get_sql_connection()
cursor = conn.cursor()



#tabela temporária
create_temp_contract_table(cursor, contracts)
conn.commit()


# sql principal
sql = """
IF OBJECT_ID('tempdb..##Esp') IS NOT NULL DROP TABLE ##Esp;

SELECT DISTINCT
    CAST(A.cod_cred AS VARCHAR) AS [Código do Credor],
    '11' AS Operação,
    RTRIM(A.cpfcgc_pes) AS [CPF/CNPJ],
    RTRIM(A.CONTRATO_TIT) AS Contrato,
    ? AS [Título da Ocorrência],
    ? AS Complemento,
    '' AS [Data de Promessa],
    FORMAT(GETDATE(),'dd/MM/yyyy HH:mm') AS [Data/Hora da Ocorrência],
    '' AS [Código do Usuário],
    '' AS [Nome do Usuário],
    '' AS [Número da parcela?]
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
     = T.Contrato COLLATE SQL_Latin1_General_CP1_CI_AS
WHERE A.nome_cred = ?
  AND C.ddd_tel IS NOT NULL
  AND C.ddd_tel <> ''
  AND LEFT(C.Nr_tel,1) = '9'
  AND LEN(C.Nr_tel) = 9
  AND C.STATUS_TEL IN (1,3)
"""



#gerando csv para credor

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