import customtkinter as ctk
from tkinter import messagebox
import threading
from src.font.runner import main
from src.filtros.base_dia_focos import obter_sheets_focos
from src.filtros.base_dia import obter_sheets_dia
from src.filtros.novos import obter_sheets_novos
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

modo_tema = "dark"
spinner_running = False

checkboxes = []

nomes_modo = {
    "Focos": "Base Focos",
    "Dia": "Base Dia",
    "Novos": "Base Novos"
}

modo_execucao = None
botao = None

def selecionar_opcao(modo):
    global modo_execucao, botao, checkboxes
    modo_execucao = modo

    limpar_frame_inferior()
    checkboxes = []

    if modo == "Focos":
        sheets = obter_sheets_focos()

    elif modo == "Dia":
        sheets = obter_sheets_dia()

    elif modo == "Novos":
        sheets = obter_sheets_novos()

    for sheet in sheets:
        cb = ctk.CTkCheckBox(frame_inferior, text=sheet)
        cb.pack(anchor="w", padx=20)
        checkboxes.append(cb)

    botao = ctk.CTkButton(
        frame_inferior,
        text="Executar Automação",
        width=200,
        height=45,
        corner_radius=12,
        font=("Arial", 15, "bold"),
        command=iniciar
    )
    botao.pack(pady=10)

    status.configure(text=f"Modo selecionado: {nomes_modo[modo]}")


class RedirectOutput:
    def write(self, text): 
        if text.strip(): 
            log(text.strip()) 

    def flush(self): 
        pass

def limpar_frame_inferior():
    for widget in frame_inferior.winfo_children():
        widget.destroy()

def iniciar():

    global spinner_running
    spinner_running = True
    animar_spinner()

    progress.start()

    log("Iniciando automação...")

    if not modo_execucao:
        messagebox.showwarning("Aviso", "Selecione uma opção")
        return

    status.configure(text="Processando...")
    botao.configure(state="disabled")

    thread = threading.Thread(
        target=executar_modo,
        daemon=True
    )

def finalizar_execucao():
    def atualizar():
        global spinner_running
        spinner_running = False

        progress.stop()
        loading.configure(text="")

        log("Processo finalizado com sucesso!")

        status.configure(text="Processo finalizado com sucesso!")
        botao.configure(state="normal")
    root.after(0, atualizar)

def log(msg):
    log_box.insert("end", msg + "\n")
    log_box.see("end")

def animar_spinner():
    frames = ["⏳", "⌛"]
    i = 0

    def loop():
        nonlocal i
        if spinner_running:
            loading.configure(text=frames[i % 2])
            i += 1
            root.after(500, loop)

    loop()

def executar_modo():
    sheets_selecionadas = []

    for cb in checkboxes:
        if cb.get() == 1:
            sheets_selecionadas.append(cb.cget("text"))

    if not sheets_selecionadas:
        messagebox.showwarning("Aviso", "Selecione ao menos uma sheet")
        finalizar_execucao()
        return

    main(modo_execucao, sheets_selecionadas)
    finalizar_execucao()
    
def alternar_tema():
    global modo_tema

    root.configure(cursor="watch")
    root.update()

    if modo_tema == "dark":
        ctk.set_appearance_mode("light")
        modo_tema = "light"
        botao_tema.configure(text="🌙")
    else:
        ctk.set_appearance_mode("dark")
        modo_tema = "dark"
        botao_tema.configure(text="☀")

    root.configure(cursor="")

#janela
root = ctk.CTk()
root.title("Marcação de Ocorrências")
root.geometry("520x560")

#frame superior

frame_button = ctk.CTkFrame(root, fg_color="transparent")
frame_button.pack(pady=10)

botao1 = ctk.CTkButton(frame_button, text="1 - BASE FOCOS", width=140, height=40, corner_radius=10, font=("Arial", 14, "bold"), command=lambda: selecionar_opcao("Focos"))
botao1.pack(side="left", padx=5)

botao2 = ctk.CTkButton(frame_button, text="2 - BASE DIA", width=140, height=40, corner_radius=10, font=("Arial", 14, "bold"), command=lambda: selecionar_opcao("Dia"))
botao2.pack(side="left", padx=5)

botao3 = ctk.CTkButton(frame_button, text="3 - BASE NOVOS", width=140, height=40, corner_radius=10, font=("Arial", 14, "bold"), command=lambda: selecionar_opcao("Novos"))
botao3.pack(side="left", padx=5)

#frame inferior

frame_inferior = ctk.CTkFrame(root, fg_color="transparent")
frame_inferior.pack(expand=True)

ctk.CTkLabel(
    frame_inferior,
    text="Selecione uma opção acima",
    font=("Arial", 14),
    text_color="gray"
).pack(pady=5)

status = ctk.CTkLabel(
    root, 
    fg_color="transparent",
    text="",
    font=("Arial", 15, "bold"),
    wraplength=480,
    justify="center"
)
status.pack(pady=5)

ctk.CTkLabel(
    root,
    fg_color="transparent",
    text="Desenvolvido por Davi Campaner - 2026",
    font=("Arial", 13, "bold", "italic"),
    text_color="gray",
    justify="center"
).pack(side="bottom", pady=8)

botao_tema = ctk.CTkButton(
    root,
    text="☀",
    width=40,
    height=30,
    corner_radius=50,
    command=alternar_tema
)

botao_tema.place(relx=0.90, rely=0.90, anchor="center")

progress = ctk.CTkProgressBar(root, width=300)
progress.set(0)
progress.pack(pady=5)

log_box = ctk.CTkTextbox(root, width=480, height=80)
log_box.pack(pady=5)

loading = ctk.CTkLabel(root, text="", font=("Arial", 18))
loading.pack()

sys.stdout = RedirectOutput()
root.mainloop()