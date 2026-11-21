import queue
import sys
import threading
import time
from datetime import datetime

import customtkinter as ctk

from src.frontend import tema
from src.frontend.animacoes import animar
from src.frontend.componentes import Botao, ChipEstado
from src.frontend.tela_canal import TelaCanal
from src.frontend.tela_rcs import TelaRCS
from src.frontend.tela_whatsapp import TelaWhatsapp

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

QUADROS_SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"


class RedirectOutput:
    """Redireciona os print() do backend para o painel de atividade da janela.

    Os prints acontecem em outra thread, então só enfileiramos o texto; quem
    escreve na tela é a thread principal (ver `_drenar_fila`).
    """

    def __init__(self, enfileirar):
        self._enfileirar = enfileirar

    def write(self, texto):
        if texto.strip():
            self._enfileirar(("log", texto.rstrip()))

    def flush(self):
        pass

    def isatty(self):
        return False


class JanelaPrincipal(ctk.CTk):
    TELAS = {
        "canal": TelaCanal,
        "whatsapp": TelaWhatsapp,
        "rcs": TelaRCS,
    }

    # (tela, ícone, texto, cor de destaque)
    MENU = [
        ("canal", "⌂", "Início", tema.PRIMARIA),
        ("whatsapp", "💬", "Whatsapp", tema.WHATSAPP),
        ("rcs", "📨", "RCS", tema.RCS),
    ]

    def __init__(self):
        super().__init__(fg_color=tema.FUNDO)
        self.title("Marcação de Ocorrências")
        self.minsize(980, 700)
        self._centralizar(1080, 760)

        self.modo_tema = "dark"
        self.spinner_running = False
        self.em_execucao = False
        self._botao_execucao = None
        self._tela_atual = None
        self._nome_atual = None
        self._inicio_execucao = 0.0
        self._quadro = 0
        self._fila = queue.Queue()

        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._construir_lateral()
        self._construir_principal()

        sys.stdout = RedirectOutput(self._fila.put)
        self.after(80, self._drenar_fila)

        self.mostrar_tela("canal")
        self._aparecer()

    # ---------- construção da interface ----------

    def _centralizar(self, largura, altura):
        try:
            escala = self._get_window_scaling()
        except Exception:
            escala = 1.0
        x = max(0, int((self.winfo_screenwidth() - largura * escala) / 2))
        y = max(0, int((self.winfo_screenheight() - altura * escala) / 2) - 20)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def _construir_lateral(self):
        lateral = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=tema.LATERAL)
        lateral.grid(row=0, column=0, sticky="ns")
        lateral.pack_propagate(False)

        # linha fina separando a lateral do conteúdo
        ctk.CTkFrame(self, width=1, corner_radius=0, fg_color=tema.BORDA).grid(
            row=0, column=1, sticky="ns"
        )

        marca = ctk.CTkFrame(lateral, fg_color="transparent")
        marca.pack(fill="x", padx=20, pady=(28, 24))

        ctk.CTkLabel(
            marca,
            text="M",
            width=42,
            height=42,
            corner_radius=13,
            fg_color=tema.PRIMARIA,
            text_color="#FFFFFF",
            font=tema.fonte(20, True),
        ).pack(side="left")

        nomes = ctk.CTkFrame(marca, fg_color="transparent")
        nomes.pack(side="left", padx=(12, 0))
        ctk.CTkLabel(
            nomes,
            text="Marcação de\nOcorrências",
            font=tema.fonte(14, True),
            text_color=tema.TEXTO,
            justify="left",
            anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            nomes,
            text="Automação VCOM",
            font=tema.fonte(11),
            text_color=tema.TEXTO_SUAVE,
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            lateral,
            text="MENU",
            font=tema.fonte(11, True),
            text_color=tema.TEXTO_SUAVE,
            anchor="w",
        ).pack(fill="x", padx=24, pady=(0, 6))

        self._botoes_menu = {}
        for nome, icone, texto, cor in self.MENU:
            botao = Botao(
                lateral,
                estilo="menu",
                cor=cor,
                text=f"{icone}   {texto}",
                anchor="w",
                height=44,
                command=lambda n=nome: self.mostrar_tela(n),
            )
            botao.pack(fill="x", padx=14, pady=3)
            self._botoes_menu[nome] = botao

        rodape = ctk.CTkFrame(lateral, fg_color="transparent")
        rodape.pack(side="bottom", fill="x", padx=14, pady=(0, 18))

        self.botao_tema = Botao(
            rodape,
            estilo="secundario",
            text="☀   Tema claro",
            height=38,
            command=self.alternar_tema,
        )
        self.botao_tema.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            rodape,
            text="Desenvolvido por Davi Campaner · 2026",
            font=tema.fonte(11),
            text_color=tema.TEXTO_SUAVE,
            wraplength=190,
            justify="center",
        ).pack()

    def _construir_principal(self):
        principal = ctk.CTkFrame(self, fg_color="transparent")
        principal.grid(row=0, column=2, sticky="nsew")
        principal.grid_columnconfigure(0, weight=1)
        principal.grid_rowconfigure(1, weight=1)

        # cabeçalho (título e subtítulo mudam conforme a tela)
        cabecalho = ctk.CTkFrame(principal, fg_color="transparent")
        cabecalho.grid(row=0, column=0, sticky="ew", padx=32, pady=(26, 8))

        self.titulo = ctk.CTkLabel(
            cabecalho, text="", font=tema.fonte(26, True), text_color=tema.TEXTO, anchor="w"
        )
        self.titulo.pack(fill="x")
        self.subtitulo = ctk.CTkLabel(
            cabecalho, text="", font=tema.fonte(13), text_color=tema.TEXTO_SUAVE, anchor="w"
        )
        self.subtitulo.pack(fill="x")

        # área onde as telas são exibidas
        self.conteudo = ctk.CTkFrame(principal, fg_color="transparent")
        self.conteudo.grid(row=1, column=0, sticky="nsew", padx=32, pady=(8, 0))

        # painel de atividade (status, progresso e log)
        painel = ctk.CTkFrame(
            principal,
            fg_color=tema.CARTAO,
            corner_radius=16,
            border_width=1,
            border_color=tema.BORDA,
        )
        painel.grid(row=2, column=0, sticky="ew", padx=32, pady=(14, 26))

        topo = ctk.CTkFrame(painel, fg_color="transparent")
        topo.pack(fill="x", padx=18, pady=(14, 10))

        ctk.CTkLabel(
            topo, text="Atividade", font=tema.fonte(14, True), text_color=tema.TEXTO
        ).pack(side="left")

        self.status = ctk.CTkLabel(
            topo, text="", font=tema.fonte(12), text_color=tema.TEXTO_SUAVE, anchor="w"
        )
        self.status.pack(side="left", padx=14)

        self.chip = ChipEstado(topo)
        self.chip.pack(side="right")

        self.progress = ctk.CTkProgressBar(
            painel,
            height=6,
            corner_radius=3,
            fg_color=tema.CARTAO_ALT,
            progress_color=tema.CARTAO_ALT,  # invisível em repouso
            indeterminate_speed=1.2,
        )
        self.progress.set(0)
        self.progress.pack(fill="x", padx=18)

        self.log_box = ctk.CTkTextbox(
            painel,
            height=150,
            corner_radius=10,
            border_width=0,
            fg_color=tema.CONSOLE,
            text_color=tema.TEXTO,
            font=("Consolas", 12),
            wrap="word",
        )
        self.log_box.pack(fill="x", padx=18, pady=(12, 16))
        self.log_box.tag_config("hora", foreground="#6B7390")
        self.log_box.tag_config("erro", foreground="#F87171")
        self.log_box.tag_config("ok", foreground="#34D399")
        self.log_box.tag_config("aviso", foreground="#FBBF24")
        self.log_box.configure(state="disabled")

    def _aparecer(self):
        """Efeito de fade-in ao abrir a janela."""
        try:
            self.attributes("-alpha", 0.0)
            animar(self, 380, lambda t: self.attributes("-alpha", t), chave="alpha")
        except Exception:
            pass

    # ---------- navegação ----------

    def mostrar_tela(self, nome):
        if nome == self._nome_atual:
            return

        if self.em_execucao:
            self.status.configure(text="Aguarde a automação terminar para trocar de tela.")
            return

        if self._tela_atual is not None:
            self._tela_atual.destroy()

        classe = self.TELAS[nome]
        self.status.configure(text="")
        self.titulo.configure(text=classe.TITULO)
        self.subtitulo.configure(text=classe.SUBTITULO)

        for chave, botao in self._botoes_menu.items():
            botao.definir_ativo(chave == nome)

        tela = classe(self.conteudo, self)
        self._tela_atual = tela
        self._nome_atual = nome

        # a tela "sobe" suavemente ao entrar
        deslocamento = 26
        tela.place(x=0, y=deslocamento, relwidth=1, relheight=1)
        animar(
            tela,
            260,
            lambda t: tela.place_configure(y=int(deslocamento * (1 - t))),
            chave="entrada",
        )

    # ---------- execução em segundo plano ----------

    def executar_em_thread(self, alvo, botao):
        """Inicia `alvo` em uma thread e controla spinner/progresso/botão."""
        self.em_execucao = True
        self._botao_execucao = botao
        self._inicio_execucao = time.time()

        self.progress.configure(mode="indeterminate", progress_color=tema.PRIMARIA)
        self.progress.start()
        self._iniciar_spinner()

        self.log("Iniciando automação...")
        self.status.configure(text="Processando...")
        botao.configure(state="disabled")

        threading.Thread(target=alvo, daemon=True).start()

    def finalizar_execucao(self, sucesso=True):
        """Pode ser chamado da thread de execução; a tela é atualizada na principal."""
        self._fila.put(("fim", sucesso))

    def _concluir(self, sucesso):
        self.spinner_running = False
        self.em_execucao = False

        segundos = int(time.time() - self._inicio_execucao)
        duracao = f"{segundos // 60}min {segundos % 60:02d}s" if segundos >= 60 else f"{segundos}s"

        self.progress.stop()
        self.progress.configure(
            mode="determinate", progress_color=tema.SUCESSO if sucesso else tema.ERRO
        )
        self.progress.set(1)

        if sucesso:
            mensagem = f"Processo finalizado com sucesso! ({duracao})"
            self.chip.definir("sucesso")
        else:
            mensagem = f"Processo finalizado com erro. ({duracao})"
            self.chip.definir("erro")

        self.log(mensagem)
        self.status.configure(text=mensagem)

        if self._botao_execucao is not None:
            self._botao_execucao.configure(state="normal")

        self.after(5000, self._voltar_ao_repouso)

    def _voltar_ao_repouso(self):
        if self.em_execucao:
            return
        self.chip.definir("pronto")
        self.progress.set(0)
        self.progress.configure(progress_color=tema.CARTAO_ALT)

    def _iniciar_spinner(self):
        self.spinner_running = True
        self._quadro = 0

        def loop():
            if not self.spinner_running:
                return
            self._quadro = (self._quadro + 1) % len(QUADROS_SPINNER)
            self.chip.definir("executando", f"{QUADROS_SPINNER[self._quadro]}  Executando")
            self.after(90, loop)

        loop()

    # ---------- log ----------

    def _drenar_fila(self):
        try:
            while True:
                tipo, valor = self._fila.get_nowait()
                if tipo == "log":
                    self.log(valor)
                elif tipo == "fim":
                    self._concluir(valor)
        except queue.Empty:
            pass
        self.after(80, self._drenar_fila)

    @staticmethod
    def _classificar(mensagem):
        baixo = mensagem.lower()
        if baixo.startswith("erro") or "traceback" in baixo or "exception" in baixo:
            return "erro"
        if "sucesso" in baixo or "limpa" in baixo:
            return "ok"
        if "nenhum" in baixo or "aviso" in baixo:
            return "aviso"
        return None

    def log(self, mensagem):
        """Escreve uma linha no painel de atividade (apenas na thread principal)."""
        etiqueta = self._classificar(mensagem)
        self.log_box.configure(state="normal")
        for i, linha in enumerate(mensagem.splitlines() or [""]):
            hora = datetime.now().strftime("%H:%M:%S") if i == 0 else "        "
            self.log_box.insert("end", f"{hora}  ", "hora")
            self.log_box.insert("end", linha + "\n", etiqueta)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    # ---------- tema ----------

    def alternar_tema(self):
        if self.modo_tema == "dark":
            ctk.set_appearance_mode("light")
            self.modo_tema = "light"
            self.botao_tema.configure(text="🌙   Tema escuro")
        else:
            ctk.set_appearance_mode("dark")
            self.modo_tema = "dark"
            self.botao_tema.configure(text="☀   Tema claro")
