import os

EXTENSOES_PADRAO = (".csv", ".xlsx")


def listar_nomes_arquivos(pasta: str, extensoes=EXTENSOES_PADRAO) -> list[str]:
    """Nomes dos arquivos da pasta com as extensões indicadas.

    Ignora subpastas e arquivos temporários do Excel ('~$').
    """
    if not os.path.isdir(pasta):
        raise FileNotFoundError(f"Pasta não encontrada: {pasta}")

    return [
        nome
        for nome in os.listdir(pasta)
        if nome.lower().endswith(extensoes)
        and not nome.startswith("~$")
        and os.path.isfile(os.path.join(pasta, nome))
    ]
