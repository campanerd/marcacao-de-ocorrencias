import os
from dotenv import load_dotenv

load_dotenv()

# Pasta onde os CSVs gerados ficam antes de serem importados no VCOM.
# Relativa à pasta de onde a aplicação é executada (antes era "src/downloads").
DOWNLOADS_DIR = "downloads"


def pasta_rcs() -> str:
    """Pasta onde chegam os arquivos do RCS (variável CAMINHO_RCS do .env)."""
    pasta = os.getenv("CAMINHO_RCS")
    if not pasta:
        raise ValueError("CAMINHO_RCS não encontrado no .env")
    return pasta
