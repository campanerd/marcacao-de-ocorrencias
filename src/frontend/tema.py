"""Paleta de cores, fontes e utilitários de cor da interface.

Cores no formato (claro, escuro): o customtkinter escolhe sozinho conforme o tema.
"""
import customtkinter as ctk

# ---------- superfícies ----------
FUNDO = ("#F1F3F9", "#0C0E13")
LATERAL = ("#FFFFFF", "#12151C")
CARTAO = ("#FFFFFF", "#171B24")
CARTAO_ALT = ("#F1F3F9", "#1E2330")
BORDA = ("#E1E5EF", "#272D3B")
CONSOLE = ("#F3F5FA", "#0A0C10")
DESABILITADO = ("#D6DAE6", "#2A3040")
BOTAO_SEC = ("#E6E9F2", "#1E2330")
BOTAO_SEC_HOVER = ("#D7DBE8", "#2A3142")

# ---------- texto ----------
TEXTO = ("#141824", "#F1F3F8")
TEXTO_SUAVE = ("#69708A", "#8B93A8")

# ---------- cores de destaque ----------
PRIMARIA = "#5B6CFF"
WHATSAPP = "#25D366"
RCS = "#8B5CF6"
SUCESSO = "#22C55E"
ERRO = "#EF4444"
AVISO = "#F59E0B"

FAMILIA = "Segoe UI"


def fonte(tamanho=13, negrito=False):
    return (FAMILIA, tamanho, "bold" if negrito else "normal")


# ---------- utilitários de cor ----------

def _rgb(cor_hex):
    cor_hex = cor_hex.lstrip("#")
    return tuple(int(cor_hex[i:i + 2], 16) for i in (0, 2, 4))


def mesclar(a, b, t):
    """Cor intermediária entre `a` e `b` (t = 0 devolve a, t = 1 devolve b)."""
    ra, rb = _rgb(a), _rgb(b)
    return "#%02x%02x%02x" % tuple(round(x + (y - x) * t) for x, y in zip(ra, rb))


def clarear(cor, t):
    return mesclar(cor, "#FFFFFF", t)


def tingir(base, acento, forca):
    """Mistura um pouco da cor de destaque na cor base (aceita tupla claro/escuro)."""
    if isinstance(base, (tuple, list)):
        return tuple(mesclar(c, acento, forca) for c in base)
    return mesclar(base, acento, forca)


def cor_atual(cor):
    """Resolve uma cor (claro, escuro) para o tema que está ativo agora."""
    if isinstance(cor, (tuple, list)):
        return cor[1] if ctk.get_appearance_mode() == "Dark" else cor[0]
    return cor
