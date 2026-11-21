import customtkinter as ctk

from src.frontend import tema
from src.frontend.componentes import CartaoCanal


class TelaCanal(ctk.CTkFrame):
    """Primeira tela: o usuário escolhe o canal (Whatsapp ou RCS)."""

    TITULO = "Início"
    SUBTITULO = "Escolha o canal de envio para marcar as ocorrências no VCOM."

    def __init__(self, master, janela):
        super().__init__(master, fg_color="transparent")
        self.janela = janela

        self.grid_columnconfigure((0, 1), weight=1, uniform="cartao")

        CartaoCanal(
            self,
            icone="💬",
            titulo="Whatsapp",
            descricao="Marca as ocorrências dos Whatsapp enviados, a partir das "
            "bases Focos, Dia e Novos.",
            cor=tema.WHATSAPP,
            comando=lambda: janela.mostrar_tela("whatsapp"),
        ).grid(row=0, column=0, sticky="new", padx=(0, 10), pady=(6, 0))

        CartaoCanal(
            self,
            icone="✉",
            titulo="RCS",
            descricao="Marca as ocorrências dos RCS enviados, a partir dos "
            "arquivos que chegam na pasta, filtrando por dia.",
            cor=tema.RCS,
            comando=lambda: janela.mostrar_tela("rcs"),
        ).grid(row=0, column=1, sticky="new", padx=(10, 0), pady=(6, 0))

        ctk.CTkLabel(
            self,
            text="O andamento e os erros da automação aparecem no painel Atividade, logo abaixo.",
            font=tema.fonte(12),
            text_color=tema.TEXTO_SUAVE,
            anchor="w",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(16, 0))
