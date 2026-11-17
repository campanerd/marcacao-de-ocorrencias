import customtkinter as ctk


class TelaCanal(ctk.CTkFrame):
    """Primeira tela: o usuário escolhe o canal (Whatsapp ou RCS)."""

    def __init__(self, master, janela):
        super().__init__(master, fg_color="transparent")
        self.janela = janela

        centro = ctk.CTkFrame(self, fg_color="transparent")
        centro.pack(expand=True)

        ctk.CTkLabel(
            centro,
            text="Qual canal deseja utilizar?",
            font=("Arial", 18, "bold"),
        ).pack(pady=(0, 20))

        ctk.CTkButton(
            centro,
            text="WHATSAPP",
            width=220,
            height=50,
            corner_radius=10,
            font=("Arial", 15, "bold"),
            command=lambda: janela.mostrar_tela("whatsapp"),
        ).pack(pady=8)

        ctk.CTkButton(
            centro,
            text="RCS",
            width=220,
            height=50,
            corner_radius=10,
            font=("Arial", 15, "bold"),
            command=lambda: janela.mostrar_tela("rcs"),
        ).pack(pady=8)
