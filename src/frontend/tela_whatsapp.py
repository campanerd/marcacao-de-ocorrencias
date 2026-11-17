import customtkinter as ctk
from tkinter import messagebox

from src.backend.application.whatsapp.executar import executar
from src.backend.application.whatsapp.obter_sheets import obter_sheets

NOMES_MODO = {
    "Focos": "Base Focos",
    "Dia": "Base Dia",
    "Novos": "Base Novos",
}


class TelaWhatsapp(ctk.CTkFrame):
    """Tela do Whatsapp: escolha da base (Focos/Dia/Novos) e das sheets."""

    def __init__(self, master, janela):
        super().__init__(master, fg_color="transparent")
        self.janela = janela

        self.modo_execucao = None
        self.botao = None
        self.checkboxes = []

        ctk.CTkButton(
            self,
            text="← Voltar",
            width=90,
            height=30,
            corner_radius=10,
            command=lambda: janela.mostrar_tela("canal"),
        ).pack(anchor="w", padx=10, pady=(10, 0))

        # frame superior
        frame_button = ctk.CTkFrame(self, fg_color="transparent")
        frame_button.pack(pady=10)

        for texto, modo in (
            ("1 - BASE FOCOS", "Focos"),
            ("2 - BASE DIA", "Dia"),
            ("3 - BASE NOVOS", "Novos"),
        ):
            ctk.CTkButton(
                frame_button,
                text=texto,
                width=140,
                height=40,
                corner_radius=10,
                font=("Arial", 14, "bold"),
                command=lambda m=modo: self.selecionar_opcao(m),
            ).pack(side="left", padx=5)

        # frame inferior
        self.frame_inferior = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_inferior.pack(expand=True)

        ctk.CTkLabel(
            self.frame_inferior,
            text="Selecione uma opção acima",
            font=("Arial", 14),
            text_color="gray",
        ).pack(pady=5)

    def limpar_frame_inferior(self):
        for widget in self.frame_inferior.winfo_children():
            widget.destroy()

    def selecionar_opcao(self, modo):
        if self.janela.em_execucao:
            return

        self.modo_execucao = modo

        self.limpar_frame_inferior()
        self.checkboxes = []

        for sheet in obter_sheets(modo):
            cb = ctk.CTkCheckBox(self.frame_inferior, text=sheet)
            cb.pack(anchor="w", padx=20)
            self.checkboxes.append(cb)

        self.botao = ctk.CTkButton(
            self.frame_inferior,
            text="Executar Automação",
            width=200,
            height=45,
            corner_radius=12,
            font=("Arial", 15, "bold"),
            command=self.iniciar,
        )
        self.botao.pack(pady=10)

        self.janela.status.configure(text=f"Modo selecionado: {NOMES_MODO[modo]}")

    def iniciar(self):
        if not self.modo_execucao:
            messagebox.showwarning("Aviso", "Selecione uma opção")
            return

        self.janela.executar_em_thread(self.executar_modo, self.botao)

    def executar_modo(self):
        sheets_selecionadas = [
            cb.cget("text") for cb in self.checkboxes if cb.get() == 1
        ]

        if not sheets_selecionadas:
            messagebox.showwarning("Aviso", "Selecione ao menos uma sheet")
            self.janela.finalizar_execucao()
            return

        executar(self.modo_execucao, sheets_selecionadas)
        self.janela.finalizar_execucao()
