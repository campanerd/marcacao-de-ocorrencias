import os
import traceback
from datetime import date
from tkinter import messagebox

import customtkinter as ctk

from src.backend.application.rcs.executar import executar
from src.backend.application.rcs.listar_arquivos import (
    dias_com_arquivos,
    filtrar_por_dia,
    listar_arquivos_rcs,
)
from src.frontend import tema
from src.frontend.componentes import Botao

FORMATO_DIA = "%d/%m/%Y"


class TelaRCS(ctk.CTkFrame):
    """Tela do RCS: filtro por dia e lista dos arquivos que chegaram na pasta."""

    TITULO = "RCS"
    SUBTITULO = "Escolha o dia e os arquivos que serão marcados no VCOM."

    def __init__(self, master, janela):
        super().__init__(master, fg_color="transparent")
        self.janela = janela

        self.arquivos = []
        self.itens = []  # (checkbox, ArquivoRCS)
        self.dias = {}   # "17/11/2026" -> date
        self._geracao = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ---------- barra: dia, atualizar, selecionar todos ----------
        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.grid(row=0, column=0, sticky="ew", pady=(4, 12))

        ctk.CTkLabel(
            barra, text="Dia", font=tema.fonte(13, True), text_color=tema.TEXTO_SUAVE
        ).pack(side="left", padx=(0, 10))

        self.menu_dia = ctk.CTkOptionMenu(
            barra,
            values=[""],
            width=160,
            height=38,
            corner_radius=10,
            fg_color=tema.CARTAO,
            button_color=tema.BORDA,
            button_hover_color=tema.RCS,
            text_color=tema.TEXTO,
            dropdown_fg_color=tema.CARTAO,
            dropdown_hover_color=tema.CARTAO_ALT,
            dropdown_text_color=tema.TEXTO,
            font=tema.fonte(13, True),
            dropdown_font=tema.fonte(13),
            command=lambda _: self.mostrar_arquivos(),
        )
        self.menu_dia.pack(side="left")

        Botao(
            barra,
            estilo="secundario",
            text="⟳   Atualizar",
            width=120,
            height=38,
            corner_radius=10,
            command=self.carregar,
        ).pack(side="left", padx=10)

        self.botao_todos = Botao(
            barra,
            estilo="secundario",
            text="Selecionar todos",
            width=140,
            height=38,
            corner_radius=10,
            command=self.alternar_todos,
        )
        self.botao_todos.pack(side="right")

        # ---------- lista de arquivos ----------
        painel = ctk.CTkFrame(
            self,
            fg_color=tema.CARTAO,
            corner_radius=16,
            border_width=1,
            border_color=tema.BORDA,
        )
        painel.grid(row=1, column=0, sticky="nsew")
        painel.grid_columnconfigure(0, weight=1)
        painel.grid_rowconfigure(0, weight=1)

        self.lista = ctk.CTkScrollableFrame(painel, fg_color="transparent")
        self.lista.grid(row=0, column=0, sticky="nsew", padx=(8, 4), pady=8)

        # ---------- rodapé ----------
        rodape = ctk.CTkFrame(self, fg_color="transparent")
        rodape.grid(row=2, column=0, sticky="ew", pady=(12, 0))

        self.contador = ctk.CTkLabel(
            rodape, text="", font=tema.fonte(13), text_color=tema.TEXTO_SUAVE
        )
        self.contador.pack(side="left")

        self.botao = Botao(
            rodape,
            cor=tema.RCS,
            text="▶   Executar RCS",
            width=230,
            height=46,
            corner_radius=14,
            font=tema.fonte(14, True),
            command=self.iniciar,
        )
        self.botao.pack(side="right")

        self.carregar()

    # ---------- dados ----------

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
        self._geracao += 1
        for widget in self.lista.winfo_children():
            widget.destroy()
        self.itens = []

        dia = self.dias[self.menu_dia.get()]
        arquivos_do_dia = filtrar_por_dia(self.arquivos, dia)

        linhas = []
        for arquivo in arquivos_do_dia:
            linhas.append(self._criar_linha(arquivo))

        if arquivos_do_dia:
            self._aparecer_em_sequencia(linhas, self._geracao)
        else:
            ctk.CTkLabel(
                self.lista,
                text="📂\nNenhum arquivo para este dia",
                font=tema.fonte(14),
                text_color=tema.TEXTO_SUAVE,
                justify="center",
            ).pack(pady=40)

        self._atualizar_contador()
        self.janela.status.configure(
            text=f"{len(arquivos_do_dia)} arquivo(s) em {self.menu_dia.get()}"
        )

    def _criar_linha(self, arquivo):
        """Cria (sem exibir ainda) a linha de um arquivo."""
        linha = ctk.CTkFrame(self.lista, fg_color=tema.CARTAO_ALT, corner_radius=12)
        linha.grid_columnconfigure(1, weight=1)

        cb = ctk.CTkCheckBox(
            linha,
            text="",
            width=24,
            checkbox_width=22,
            checkbox_height=22,
            corner_radius=7,
            fg_color=tema.RCS,
            hover_color=tema.RCS,
            command=self._atualizar_contador,
        )
        cb.grid(row=0, column=0, rowspan=2, padx=(14, 4), pady=12)

        extensao = os.path.splitext(arquivo.nome)[1].lstrip(".").upper() or "ARQ"

        textos = (
            ctk.CTkLabel(
                linha,
                text=arquivo.categoria,
                font=tema.fonte(14, True),
                text_color=tema.TEXTO,
                anchor="w",
            ),
            ctk.CTkLabel(
                linha,
                text=f"{arquivo.data_hora:%d/%m/%Y}  ·  {arquivo.data_hora:%H:%M}",
                font=tema.fonte(12),
                text_color=tema.TEXTO_SUAVE,
                anchor="w",
            ),
        )
        textos[0].grid(row=0, column=1, sticky="sw", pady=(10, 0))
        textos[1].grid(row=1, column=1, sticky="nw", pady=(0, 10))

        selo = ctk.CTkLabel(
            linha,
            text=extensao,
            width=48,
            height=24,
            corner_radius=8,
            fg_color=tema.tingir(tema.CARTAO_ALT, tema.RCS, 0.22),
            text_color=tema.RCS,
            font=tema.fonte(11, True),
        )
        selo.grid(row=0, column=2, rowspan=2, padx=16)

        # clicar em qualquer parte da linha marca/desmarca o arquivo
        for alvo in (linha, selo, *textos):
            alvo.bind("<Button-1>", lambda _e, c=cb: c.toggle(), add="+")

        self.itens.append((cb, arquivo))
        return linha

    def _aparecer_em_sequencia(self, linhas, geracao, i=0):
        """Mostra as linhas uma a uma, para a lista 'entrar' com animação."""
        if geracao != self._geracao or i >= len(linhas):
            return
        linhas[i].pack(fill="x", padx=6, pady=3)
        self.after(35, lambda: self._aparecer_em_sequencia(linhas, geracao, i + 1))

    def _atualizar_contador(self):
        total = len(self.itens)
        marcados = sum(1 for cb, _ in self.itens if cb.get() == 1)
        self.contador.configure(
            text=f"{marcados} de {total} arquivo(s) selecionado(s)" if total else ""
        )
        todos = total > 0 and marcados == total
        self.botao_todos.configure(text="Limpar seleção" if todos else "Selecionar todos")

    def alternar_todos(self):
        if not self.itens:
            return
        marcar = any(cb.get() == 0 for cb, _ in self.itens)
        for cb, _ in self.itens:
            cb.select() if marcar else cb.deselect()
        self._atualizar_contador()

    # ---------- execução ----------

    def iniciar(self):
        selecionados = [arquivo for cb, arquivo in self.itens if cb.get() == 1]

        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione ao menos um arquivo")
            return

        self.janela.executar_em_thread(
            lambda: self.executar_selecionados(selecionados), self.botao
        )

    def executar_selecionados(self, arquivos):
        sucesso = True
        try:
            executar(arquivos)
        except Exception as erro:
            sucesso = False
            print(f"Erro na execução do RCS: {erro}")
            print(traceback.format_exc())
        finally:
            self.janela.finalizar_execucao(sucesso)
