from tkinter import messagebox
from src.backend.application.rcs.executar import executar

from datetime import date

import customtkinter as ctk

from src.backend.application.rcs.listar_arquivos import (
    dias_com_arquivos,
    filtrar_por_dia,
    listar_arquivos_rcs,
)

FORMATO_DIA = "%d/%m/%Y"


class TelaRCS(ctk.CTkFrame):
    """Tela do RCS: filtro por dia e lista dos arquivos que chegaram na pasta."""

    def __init__(self, master, janela):
        super().__init__(master, fg_color="transparent")
        self.janela = janela

        self.arquivos = []
        self.itens = []  # (checkbox, ArquivoRCS)
        self.dias = {}   # "17/11/2026" -> date

        ctk.CTkButton(
            self,
            text="← Voltar",
            width=90,
            height=30,
            corner_radius=10,
            command=lambda: janela.mostrar_tela("canal"),
        ).pack(anchor="w", padx=10, pady=(10, 0))

        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.pack(pady=10)

        ctk.CTkLabel(barra, text="Dia:", font=("Arial", 14, "bold")).pack(
            side="left", padx=(0, 8)
        )

        self.menu_dia = ctk.CTkOptionMenu(
            barra, values=[""], width=140, command=lambda _: self.mostrar_arquivos()
        )
        self.menu_dia.pack(side="left")

        ctk.CTkButton(
            barra, text="Atualizar", width=90, command=self.carregar
        ).pack(side="left", padx=8)

        self.lista = ctk.CTkScrollableFrame(
            self, fg_color="transparent", width=400, height=170
        )
        self.lista.pack(pady=5)

        self.botao = ctk.CTkButton(
            self,
            text="Executar Automação",
            width=200,
            height=45,
            corner_radius=12,
            font=("Arial", 15, "bold"),
            command=self.iniciar,
        )
        self.botao.pack(pady=10)

        self.carregar()

    def carregar(self):
        """Lê a pasta do RCS e atualiza os dias disponíveis."""
        erro = None
        try:
            self.arquivos = listar_arquivos_rcs()
        except Exception as e:
            self.arquivos = []
            erro = e

        hoje = date.today()
        dias = sorted(set(dias_com_arquivos(self.arquivos)) | {hoje}, reverse=True)
        self.dias = {d.strftime(FORMATO_DIA): d for d in dias}

        selecionado = self.menu_dia.get()
        if selecionado not in self.dias:
            selecionado = hoje.strftime(FORMATO_DIA)

        self.menu_dia.configure(values=list(self.dias))
        self.menu_dia.set(selecionado)

        self.mostrar_arquivos()

        if erro is not None:
            self.janela.status.configure(text=f"Erro ao ler a pasta do RCS: {erro}")

    def mostrar_arquivos(self):
        for widget in self.lista.winfo_children():
            widget.destroy()
        self.itens = []

        dia = self.dias[self.menu_dia.get()]
        arquivos_do_dia = filtrar_por_dia(self.arquivos, dia)

        for arquivo in arquivos_do_dia:
            cb = ctk.CTkCheckBox(self.lista, text=arquivo.rotulo)
            cb.pack(anchor="w", padx=20, pady=2)
            self.itens.append((cb, arquivo))

        if not arquivos_do_dia:
            ctk.CTkLabel(
                self.lista,
                text="Nenhum arquivo para este dia",
                font=("Arial", 14),
                text_color="gray",
            ).pack(pady=10)

        self.janela.status.configure(
            text=f"{len(arquivos_do_dia)} arquivo(s) em {self.menu_dia.get()}"
        )

    def iniciar(self):
        selecionados = [arquivo for cb, arquivo in self.itens if cb.get() == 1]

        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione ao menos um arquivo")
            return

        self.janela.executar_em_thread(
            lambda: self.executar_selecionados(selecionados), self.botao
        )

    def executar_selecionados(self, arquivos):
        try:
            executar(arquivos)
        except Exception as erro:
            print(f"Erro na execução do RCS: {erro}")
        finally:
            self.janela.finalizar_execucao()
