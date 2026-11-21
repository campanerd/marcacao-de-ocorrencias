import json
import os
from datetime import datetime

ARQUIVO_HISTORICO = "historico_rcs.json"


def carregar_historico():
    """Devolve {nome_do_arquivo: data_do_envio}. Se não existir, devolve vazio."""
    if not os.path.exists(ARQUIVO_HISTORICO):
        return {}
    try:
        with open(ARQUIVO_HISTORICO, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def registrar_envio(nomes):
    """Marca os arquivos como enviados agora."""
    historico = carregar_historico()
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    for nome in nomes:
        historico[nome] = agora

    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)