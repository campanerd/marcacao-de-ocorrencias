from src.backend.application.whatsapp.filtros.base_dia_focos import obter_sheets_focos
from src.backend.application.whatsapp.filtros.base_dia import obter_sheets_dia
from src.backend.application.whatsapp.filtros.novos import obter_sheets_novos


def obter_sheets(modo: str) -> list:
    """Lista as sheets disponíveis para a base escolhida (Focos, Dia ou Novos)."""
    if modo == "Focos":
        return obter_sheets_focos()

    if modo == "Dia":
        return obter_sheets_dia()

    if modo == "Novos":
        return obter_sheets_novos()

    raise ValueError(f"Modo inválido: {modo}")
