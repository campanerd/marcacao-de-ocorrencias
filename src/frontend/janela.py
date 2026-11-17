import sys
import threading

import customtkinter as ctk

from src.frontend.tela_canal import TelaCanal
from src.frontend.tela_rcs import TelaRCS
from src.frontend.tela_whatsapp import TelaWhatsapp

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class RedirectOutput:
    """Redireciona os print() do backend para a caixa de log da janela."""

    def __init__(self, log):
        self._log = log

    def write(self, text):
        if text.strip():
            self._log(text.strip())

    def flush(self):
        pass


class JanelaPrincipal(ctk.CTk):
    TELAS = {
        "canal": TelaCanal,
        "whatsapp": TelaWhatsapp,
        "rcs": TelaRCS,
    }

    def __init__(self):
        super().__init__()
        self.title("Marcação de Ocorrências")
        self.geometry("520x560")

        self.modo_tema = "dark"
        self.spinner_running = False
        self.em_execucao = False
        self._botao_execucao = None
        self._tela_atual = None

        # área onde as telas (canal / whatsapp / rcs) são exibidas
        self.conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.conteudo.pack(fill="both", expand=True)

        # componentes compartilhados por todas as telas
        self.status = ctk.CTkLabel(
            self,
            fg_color="transparent",
            text="",
            font=("Arial", 15, "bold"),
            wraplength=480,
            justify="center",
        )
        self.status.pack(pady=5)

        ctk.CTkLabel(
            self,
            fg_color="transparent",
            text="Desenvolvido por Davi Campaner - 2026",
            font=("Arial", 13, "bold", "italic"),
            text_color="gray",
            justify="center",
        ).pack(side="bottom", pady=8)

        self.botao_tema = ctk.CTkButton(
            self,
            text="☀",
            width=40,
            height=30,
            corner_radius=50,
            command=self.alternar_tema,
        )
        self.botao_tema.place(relx=0.90, rely=0.90, anchor="center")

        self.progress = ctk.CTkProgressBar(self, width=300)
        self.progress.set(0)
        self.progress.pack(pady=5)

        self.log_box = ctk.CTkTextbox(self, width=480, height=80)
        self.log_box.pack(pady=5)

        self.loading = ctk.CTkLabel(self, text="", font=("Arial", 18))
        self.loading.pack()

        sys.stdout = RedirectOutput(self.log)

        self.mostrar_tela("canal")

    # ---------- navegação ----------

    def mostrar_tela(self, nome):
        if self.em_execucao:
            return

        if self._tela_atual is not None:
            self._tela_atual.destroy()

        self.status.configure(text="")
        self._tela_atual = self.TELAS[nome](self.conteudo, self)
        self._tela_atual.pack(fill="both", expand=True)

    # ---------- execução em segundo plano ----------

    def executar_em_thread(self, alvo, botao):
        """Inicia `alvo` em uma thread e controla spinner/progresso/botão."""
        self.em_execucao = True
        self._botao_execucao = botao

        self.spinner_running = True
        self.animar_spinner()
        self.progress.start()

        self.log("Iniciando automação...")
        self.status.configure(text="Processando...")
        botao.configure(state="disabled")

        threading.Thread(target=alvo, daemon=True).start()

    def finalizar_execucao(self):
        def atualizar():
            self.spinner_running = False
            self.em_execucao = False

            self.progress.stop()
            self.loading.configure(text="")

            self.log("Processo finalizado com sucesso!")

            self.status.configure(text="Processo finalizado com sucesso!")
            if self._botao_execucao is not None:
                self._botao_execucao.configure(state="normal")

        self.after(0, atualizar)

    # ---------- utilitários de interface ----------

    def log(self, msg):
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")

    def animar_spinner(self):
        frames = ["⏳", "⌛"]
        i = 0

        def loop():
            nonlocal i
            if self.spinner_running:
                self.loading.configure(text=frames[i % 2])
                i += 1
                self.after(500, loop)

        loop()

    def alternar_tema(self):
        self.configure(cursor="watch")
        self.update()

        if self.modo_tema == "dark":
            ctk.set_appearance_mode("light")
            self.modo_tema = "light"
            self.botao_tema.configure(text="🌙")
        else:
            ctk.set_appearance_mode("dark")
            self.modo_tema = "dark"
            self.botao_tema.configure(text="☀")

        self.configure(cursor="")
