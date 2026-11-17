"""Regras puras para interpretar os arquivos que chegam na pasta do RCS.

Os nomes seguem o padrão  CATEGORIA_dd-mm-aaaa_hh-mm.csv
(ex.: PROMOTORA_17-11-2026_12-12.csv, DAYCRED-16A360_05-11-2026_11-21.csv).
"""
import re
from dataclasses import dataclass
from datetime import date, datetime

_PADRAO_NOME = re.compile(
    r"^(?P<categoria>.+)_"
    r"(?P<dia>\d{2})-(?P<mes>\d{2})-(?P<ano>\d{4})_"
    r"(?P<hora>\d{2})-(?P<minuto>\d{2})",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ArquivoRCS:
    nome: str
    categoria: str
    data_hora: datetime

    @property
    def dia(self) -> date:
        return self.data_hora.date()

    @property
    def rotulo(self) -> str:
        """Texto exibido na tela, ex.: PROMOTORA_17-11 (12:12)."""
        return f"{self.categoria}_{self.data_hora:%d-%m} ({self.data_hora:%H:%M})"


def interpretar_nome(nome: str) -> ArquivoRCS | None:
    """Extrai categoria e data/hora do nome do arquivo.

    Retorna None se o nome não segue o padrão (esses arquivos são ignorados).
    """
    casamento = _PADRAO_NOME.match(nome)
    if not casamento:
        return None

    try:
        data_hora = datetime(
            int(casamento["ano"]),
            int(casamento["mes"]),
            int(casamento["dia"]),
            int(casamento["hora"]),
            int(casamento["minuto"]),
        )
    except ValueError:
        return None

    return ArquivoRCS(
        nome=nome,
        categoria=casamento["categoria"].strip(),
        data_hora=data_hora,
    )


def dias_com_arquivos(arquivos) -> list[date]:
    return sorted({a.dia for a in arquivos}, reverse=True)


def filtrar_por_dia(arquivos, dia: date) -> list[ArquivoRCS]:
    return sorted((a for a in arquivos if a.dia == dia), key=lambda a: a.data_hora)
