def create_temp_contract_table(cursor, contracts):
    """
    Cria a tabela temporária #Contratos e insere os contratos
    """
    cursor.execute("""
        IF OBJECT_ID('tempdb..#Contratos') IS NOT NULL
            DROP TABLE #Contratos;

        CREATE TABLE #Contratos (
            Contrato VARCHAR(50)
        );
    """)

    cursor.fast_executemany = True
    cursor.executemany(
        "INSERT INTO #Contratos (Contrato) VALUES (?)",
        [(c,) for c in contracts]
    )