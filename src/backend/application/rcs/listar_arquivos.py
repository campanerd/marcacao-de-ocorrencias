from src.backend.domain.rcs.arquivo_rcs import (
    ArquivoRCS,
    dias_com_arquivos,
    filtrar_por_dia,
    interpretar_nome,
)
from src.backend.infrastructure.files.listar_arquivos import listar_nomes_arquivos
from src.backend.infrastructure.files.paths import pasta_rcs

__all__ = ["ArquivoRCS", "listar_arquivos_rcs", "dias_com_arquivos", "filtrar_por_dia"]


def listar_arquivos_rcs() -> list[ArquivoRCS]:
    """Arquivos reconhecidos na pasta do RCS, do mais recente para o mais antigo."""
    arquivos = (interpretar_nome(nome) for nome in listar_nomes_arquivos(pasta_rcs()))
    reconhecidos = [a for a in arquivos if a is not None]
    return sorted(reconhecidos, key=lambda a: a.data_hora, reverse=True)
