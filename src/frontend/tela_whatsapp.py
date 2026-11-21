import traceback
from tkinter import messagebox

import customtkinter as ctk

from src.backend.application.whatsapp.executar import executar
from src.backend.application.whatsapp.obter_sheets import obter_sheets
from src.frontend import tema
from src.frontend.componentes import Botao, CartaoOpcao

NOMES_MODO = {
    "Focos": "Base Focos",
    "Dia": "Base Dia",
    "Novos": "Base Novos",
}

# (modo, número exibido, título, descrição)
OPCOES = (
    ("Focos", 1, "Focos", "Base Focos"),
    ("Dia", 2, "Dia", "Base Dia"),
    ("Novos", 3, "Novos", "Base Novos"),
)


class TelaWhatsapp(ctk.CTkFrame):
    """Tela do Whatsapp: escolha da base (Focos/Dia/Novos) e das sheets."""

    TITULO = "Whatsapp"
    SUBTITULO = "Escolha a base e as sheets que serão marcadas no VCOM."

    def __init__(self, master, janela):
        super().__init__(master, fg_color="transparent")
        self.janela = janela

        self.modo_execucao = None
        self.checkboxes = []
        self._geracao = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ---------- bases ----------
        bases = ctk.CTkFrame(self, fg_color="transparent")
        bases.grid(row=0, column=0, sticky="ew", pady=(4, 12))
        bases.grid_columnconfigure((0, 1, 2), weight=1, uniform="base")

        self.cartoes = {}
        for coluna, (modo, numero, titulo, descricao) in enumerate(OPCOES):
            cartao = CartaoOpcao(
                bases,
                numero=numero,
                titulo=titulo,
                descricao=descricao,
                cor=tema.WHATSAPP,
                comando=lambda m=modo: self.selecionar_opcao(m),
            )
            cartao.grid(row=0, column=coluna, sticky="ew", padx=(0 if coluna == 0 else 6, 0 if coluna == 2 else 6))
            self.cartoes[modo] = cartao

        # ---------- sheets ----------
        painel = ctk.CTkFrame(
            self,
            fg_color=tema.CARTAO,
            corner_radius=16,
            border_width=1,
            border_color=tema.BORDA,
        )
        painel.grid(row=1, column=0, sticky="nsew")
        painel.grid_columnconfigure(0, weight=1)
        painel.grid_rowconfigure(1, weight=1)

        topo = ctk.CTkFrame(painel, fg_color="transparent")
        topo.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            topo, text="Sheets da base", font=tema.fonte(14, True), text_color=tema.TEXTO
        ).pack(side="left")

        self.contador = ctk.CTkLabel(
            topo, text="", font=tema.fonte(12), text_color=tema.TEXTO_SUAVE
        )
        self.contador.pack(side="left", padx=12)

        self.botao_todas = Botao(
            topo,
            estilo="secundario",
            text="Selecionar todas",
            height=30,
            width=130,
            corner_radius=9,
            font=tema.fonte(12, True),
            command=self.alternar_todas,
        )
        self.botao_todas.pack(side="right")

        self.lista = ctk.CTkScrollableFrame(painel, fg_color="transparent")
        self.lista.grid(row=1, column=0, sticky="nsew", padx=(8, 4), pady=(0, 8))

        # ---------- rodapé ----------
        rodape = ctk.CTkFrame(self, fg_color="transparent")
        rodape.grid(row=2, column=0, sticky="ew", pady=(12, 0))

        self.botao = Botao(
            rodape,
            cor=tema.WHATSAPP,
            text="▶   Executar automação",
            width=230,
            height=46,
            corner_radius=14,
            font=tema.fonte(14, True),
            command=self.iniciar,
        )
        self.botao.pack(side="right")

        self._mostrar_aviso("Selecione uma base acima para ver as sheets.")

    # ---------- lista de sheets ----------

    def _limpar_lista(self):
        self._geracao += 1
        for widget in self.lista.winfo_children():
            widget.destroy()
        self.checkboxes = []

    def _mostrar_aviso(self, texto):
        self._limpar_lista()
        self.contador.configure(text="")
        ctk.CTkLabel(
            self.lista, text=texto, font=tema.fonte(13), text_color=tema.TEXTO_SUAVE
        ).pack(pady=30)

    def selecionar_opcao(self, modo):
        if self.janela.em_execucao:
            return

        self.modo_execucao = modo
        for chave, cartao in self.cartoes.items():
            cartao.definir_selecionado(chave == modo)

        try:
            sheets = obter_sheets(modo)
        except Exception as erro:
            print(f"Erro ao ler as sheets da {NOMES_MODO[modo]}: {erro}")
            self._mostrar_aviso("Não foi possível ler as sheets desta base.")
            return

        self._limpar_lista()

        if not sheets:
            self._mostrar_aviso("Esta base não tem sheets disponíveis.")
            return

        linhas = []
        for sheet in sheets:
            linha = ctk.CTkFrame(self.lista, fg_color=tema.CARTAO_ALT, corner_radius=10)
            cb = ctk.CTkCheckBox(
                linha,
                text=sheet,
                font=tema.fonte(13),
                text_color=tema.TEXTO,
                fg_color=tema.WHATSAPP,
                hover_color=tema.WHATSAPP,
                command=self._atualizar_contador,
            )
            cb.pack(anchor="w", padx=14, pady=9)
            linha.bind("<Button-1>", lambda _e, c=cb: self._alternar(c))
            self.checkboxes.append(cb)
            linhas.append(linha)

        self._atualizar_contador()
        self.janela.status.configure(text=f"Modo selecionado: {NOMES_MODO[modo]}")
        self._aparecer_em_sequencia(linhas, self._geracao)

    def _aparecer_em_sequencia(self, linhas, geracao, i=0):
        """Mostra as linhas uma a uma, para a lista 'entrar' com animação."""
        if geracao != self._geracao or i >= len(linhas):
            return
        linhas[i].pack(fill="x", padx=6, pady=3)
        self.after(35, lambda: self._aparecer_em_sequencia(linhas, geracao, i + 1))

    def _alternar(self, checkbox):
        checkbox.toggle()

    def _atualizar_contador(self):
        marcadas = sum(1 for cb in self.checkboxes if cb.get() == 1)
        self.contador.configure(text=f"{marcadas} de {len(self.checkboxes)} selecionada(s)")
        todas = bool(self.checkboxes) and marcadas == len(self.checkboxes)
        self.botao_todas.configure(text="Limpar seleção" if todas else "Selecionar todas")

    def alternar_todas(self):
        if not self.checkboxes:
            return
        marcar = any(cb.get() == 0 for cb in self.checkboxes)
        for cb in self.checkboxes:
            cb.select() if marcar else cb.deselect()
        self._atualizar_contador()

    # ---------- execução ----------

    def iniciar(self):
        if not self.modo_execucao:
            messagebox.showwarning("Aviso", "Selecione uma opção")
            return

        sheets_selecionadas = [
            cb.cget("text") for cb in self.checkboxes if cb.get() == 1
        ]

        if not sheets_selecionadas:
            messagebox.showwarning("Aviso", "Selecione ao menos uma sheet")
            return

        self.janela.executar_em_thread(
            lambda: self.executar_modo(sheets_selecionadas), self.botao
        )

    def executar_modo(self, sheets_selecionadas):
        sucesso = True
        try:
            executar(self.modo_execucao, sheets_selecionadas)
        except Exception as erro:
            sucesso = False
            print(f"Erro na execução do Whatsapp: {erro}")
            print(traceback.format_exc())
        finally:
            self.janela.finalizar_execucao(sucesso)
