"""Animações simples baseadas em `after` (sem dependências extras)."""
import time
import tkinter as tk

from src.frontend.tema import cor_atual, mesclar

QUADRO_MS = 16  # ~60 fps


def suavizar(t):
    """Curva ease-out: começa rápido e desacelera no final."""
    return 1 - (1 - t) ** 3


def animar(widget, duracao_ms, passo, fim=None, chave="anim"):
    """Chama `passo(t)` com t de 0 a 1 durante `duracao_ms`.

    Iniciar outra animação com a mesma `chave` no mesmo widget cancela a anterior.
    """
    tokens = widget.__dict__.setdefault("_tokens_anim", {})
    token = object()
    tokens[chave] = token
    inicio = time.perf_counter()

    def tick():
        if tokens.get(chave) is not token:
            return
        try:
            if not widget.winfo_exists():
                return
            t = min(1.0, (time.perf_counter() - inicio) * 1000 / duracao_ms)
            passo(suavizar(t))
            if t < 1.0:
                widget.after(QUADRO_MS, tick)
            elif fim:
                fim()
        except tk.TclError:
            return  # widget destruído no meio da animação

    tick()


def animar_cor(widget, opcao, destino, duracao_ms=160):
    """Faz a transição suave de uma opção de cor (fg_color, border_color...)."""
    try:
        origem = cor_atual(widget.cget(opcao))
        alvo = cor_atual(destino)
        pode_animar = origem.startswith("#") and alvo.startswith("#")
    except Exception:
        pode_animar = False

    if not pode_animar:
        widget.configure(**{opcao: destino})
        return

    animar(
        widget,
        duracao_ms,
        lambda t: widget.configure(**{opcao: mesclar(origem, alvo, t)}),
        # no final volta para a cor original (tupla), para o tema claro/escuro continuar valendo
        fim=lambda: widget.configure(**{opcao: destino}),
        chave=f"cor_{opcao}",
    )
