"""Componentes visuais reutilizados pelas telas (botões, cartões e chip de estado)."""
import customtkinter as ctk
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass

from src.frontend import tema
from src.frontend.animacoes import animar_cor


class Botao(ctk.CTkButton):
    """Botão com transição de cor ao passar o mouse.

    estilo: "primario" (cor cheia), "secundario" (cinza) ou "menu" (item da lateral).
    """

    def __init__(self, master, estilo="primario", cor=tema.PRIMARIA, **kwargs):
        self._b_cor = cor

        if estilo == "primario":
            self._b_base = cor
            self._b_hover = tema.clarear(cor, 0.18)
            self._b_txt = "#FFFFFF"
        elif estilo == "secundario":
            self._b_base = tema.BOTAO_SEC
            self._b_hover = tema.BOTAO_SEC_HOVER
            self._b_txt = tema.TEXTO
        else:  # menu
            self._b_base = tema.LATERAL
            self._b_hover = tema.CARTAO_ALT
            self._b_txt = tema.TEXTO_SUAVE

        kwargs.setdefault("corner_radius", 12)
        kwargs.setdefault("height", 40)
        kwargs.setdefault("font", tema.fonte(13, True))

        super().__init__(
            master,
            fg_color=self._b_base,
            hover=False,  # o hover é feito por nós, com animação
            text_color=self._b_txt,
            text_color_disabled=tema.TEXTO_SUAVE,
            **kwargs,
        )

        self.bind("<Enter>", self._entrar)
        self.bind("<Leave>", self._sair)

    def _entrar(self, _evento=None):
        if self.cget("state") != "disabled":
            animar_cor(self, "fg_color", self._b_hover, 140)

    def _sair(self, _evento=None):
        if self.cget("state") != "disabled":
            animar_cor(self, "fg_color", self._b_base, 220)

    def configure(self, require_redraw=False, **kwargs):
        # botão desabilitado fica com cara de desabilitado (cinza)
        if "state" in kwargs:
            desabilitado = kwargs["state"] == "disabled"
            kwargs["fg_color"] = tema.DESABILITADO if desabilitado else self._b_base
        super().configure(require_redraw=require_redraw, **kwargs)

    def definir_ativo(self, ativo):
        """Marca o item do menu lateral como selecionado."""
        self._b_base = tema.tingir(tema.LATERAL, self._b_cor, 0.16) if ativo else tema.LATERAL
        self._b_txt = self._b_cor if ativo else tema.TEXTO_SUAVE
        super().configure(text_color=self._b_txt)
        animar_cor(self, "fg_color", self._b_base, 220)


class ChipEstado(ctk.CTkLabel):
    """Etiqueta que mostra o estado da automação (pronto, executando, concluído, erro)."""

    ESTADOS = {
        "pronto": ("●  Pronto", tema.CARTAO_ALT, tema.TEXTO_SUAVE),
        "executando": (
            "Executando",
            tema.tingir(tema.CARTAO_ALT, tema.PRIMARIA, 0.25),
            tema.PRIMARIA,
        ),
        "sucesso": (
            "✓  Concluído",
            tema.tingir(tema.CARTAO_ALT, tema.SUCESSO, 0.22),
            tema.SUCESSO,
        ),
        "erro": (
            "✕  Com erro",
            tema.tingir(tema.CARTAO_ALT, tema.ERRO, 0.22),
            tema.ERRO,
        ),
    }

    def __init__(self, master):
        texto, fundo, cor = self.ESTADOS["pronto"]
        super().__init__(
            master,
            text=texto,
            fg_color=fundo,
            text_color=cor,
            corner_radius=14,
            width=140,
            height=28,
            font=tema.fonte(12, True),
        )
        self._estado = "pronto"

    def definir(self, estado, texto=None):
        padrao, fundo, cor = self.ESTADOS[estado]
        self.configure(text=texto or padrao, text_color=cor)
        if estado != self._estado:
            self._estado = estado
            animar_cor(self, "fg_color", fundo, 240)


class _CartaoBase(ctk.CTkFrame):
    """Cartão clicável que anima a borda e o fundo ao passar o mouse."""

    def __init__(self, master, cor, comando):
        super().__init__(
            master,
            fg_color=tema.CARTAO,
            border_width=1,
            border_color=tema.BORDA,
            corner_radius=18,
        )
        self._c_cor = cor
        self._c_comando = comando
        self._c_hover = False
        self._c_selecionado = False

    def _ativar(self):
        """Chamar no fim do __init__ da subclasse, depois de criar os filhos."""
        self._vincular(self)

    def _vincular(self, widget):
        widget.bind("<Enter>", self._entrar, add="+")
        widget.bind("<Leave>", self._sair, add="+")
        widget.bind("<Button-1>", self._clicar, add="+")
        try:
            widget.configure(cursor="hand2")
        except Exception:
            pass
        for filho in widget.winfo_children():
            if isinstance(filho, CTkBaseClass):
                self._vincular(filho)

    def _ponteiro_dentro(self):
        try:
            x, y = self.winfo_pointerxy()
            atual = self.winfo_containing(x, y)
        except Exception:
            return False
        while atual is not None:
            if atual is self:
                return True
            atual = getattr(atual, "master", None)
        return False

    def _entrar(self, _evento=None):
        if not self._c_hover:
            self._c_hover = True
            self._ao_hover(True)
            self._aplicar()

    def _sair(self, _evento=None):
        if self._c_hover and not self._ponteiro_dentro():
            self._c_hover = False
            self._ao_hover(False)
            self._aplicar()

    def _clicar(self, _evento=None):
        if self._c_comando:
            self._c_comando()

    def _ao_hover(self, ativo):
        """Gancho para as subclasses reagirem ao mouse (opcional)."""

    def _aplicar(self):
        if self._c_selecionado:
            borda = self._c_cor
            fundo = tema.tingir(tema.CARTAO, self._c_cor, 0.12)
        elif self._c_hover:
            borda = self._c_cor
            fundo = tema.CARTAO_ALT
        else:
            borda = tema.BORDA
            fundo = tema.CARTAO
        animar_cor(self, "border_color", borda, 170)
        animar_cor(self, "fg_color", fundo, 170)


class CartaoCanal(_CartaoBase):
    """Cartão grande da tela inicial (Whatsapp / RCS)."""

    def __init__(self, master, icone, titulo, descricao, cor, comando):
        super().__init__(master, cor, comando)

        ctk.CTkLabel(
            self,
            text=icone,
            width=60,
            height=60,
            corner_radius=18,
            fg_color=cor,
            text_color="#FFFFFF",
            font=("Segoe UI Emoji", 26),
        ).pack(anchor="w", padx=26, pady=(26, 14))

        ctk.CTkLabel(
            self,
            text=titulo,
            font=tema.fonte(22, True),
            text_color=tema.TEXTO,
            anchor="w",
        ).pack(fill="x", padx=26)

        ctk.CTkLabel(
            self,
            text=descricao,
            font=tema.fonte(13),
            text_color=tema.TEXTO_SUAVE,
            anchor="w",
            justify="left",
            wraplength=290,
        ).pack(fill="x", padx=26, pady=(6, 14))

        self._cta = ctk.CTkLabel(
            self,
            text="Abrir  →",
            font=tema.fonte(13, True),
            text_color=cor,
            anchor="w",
        )
        self._cta.pack(fill="x", padx=26, pady=(0, 24))

        self._ativar()

    def _ao_hover(self, ativo):
        self._cta.configure(text="Abrir      →" if ativo else "Abrir  →")


class CartaoOpcao(_CartaoBase):
    """Cartão selecionável (ex.: Base Focos / Dia / Novos)."""

    def __init__(self, master, numero, titulo, descricao, cor, comando):
        super().__init__(master, cor, comando)
        self.grid_columnconfigure(1, weight=1)

        self._badge = ctk.CTkLabel(
            self,
            text=str(numero),
            width=40,
            height=40,
            corner_radius=12,
            fg_color=tema.tingir(tema.CARTAO, cor, 0.2),
            text_color=cor,
            font=tema.fonte(16, True),
        )
        self._badge.grid(row=0, column=0, rowspan=2, padx=(16, 12), pady=14)

        ctk.CTkLabel(
            self,
            text=titulo,
            font=tema.fonte(15, True),
            text_color=tema.TEXTO,
            anchor="w",
        ).grid(row=0, column=1, sticky="sw", pady=(14, 0))

        ctk.CTkLabel(
            self,
            text=descricao,
            font=tema.fonte(12),
            text_color=tema.TEXTO_SUAVE,
            anchor="w",
        ).grid(row=1, column=1, sticky="nw", pady=(0, 14), padx=(0, 16))

        self._ativar()

    def definir_selecionado(self, selecionado):
        self._c_selecionado = selecionado
        self._badge.configure(
            fg_color=self._c_cor if selecionado else tema.tingir(tema.CARTAO, self._c_cor, 0.2),
            text_color="#FFFFFF" if selecionado else self._c_cor,
        )
        self._aplicar()
