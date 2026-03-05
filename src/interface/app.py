import tkinter as tk
from tkinter import messagebox
import threading

nomes_modo = {
    "Focos": "Focos",
    "Base Novos": "Base Novos",
    "Novos": "Novos"
}

modo_execucao = None
botao = None

def focos():
    print("Focos")

def selecionar_opcao(modo):
    global modo_execucao, botao
    modo_execucao = modo

    limpar_frame_inferior()

    botao = tk.Button(frame_inferior, text="Executar", command=iniciar)
    botao.pack(pady=10)

    status.config(text=f"Modo selecionado: {nomes_modo[modo]}")

def limpar_frame_inferior():
    for widget in frame_inferior.winfo_children():
        widget.destroy()

def iniciar():

    if not modo_execucao:
        messagebox.showwarning("Aviso", "Selecione uma opção")
        return

    status.config(text="Processando...")
    botao.config(state="disabled")

    if modo_execucao == "Focos":
        thread = threading.Thread(
            target=focos,
            daemon=True
        )
    
    elif modo_execucao == "Base Novos":
        thread = threading.Thread(
            target=base_novos,
            daemon=True
        )
    
    elif modo_execucao == "Novos":
        thread = threading.Thread(
            target=novos,
            daemon=True
        )

    thread.start()

def execute():
    print("teste")

def base_novos():
    print("Base Novos")

def novos():
    print("Novos")

#janela
root = tk.Tk()
root.title("Marcação de Ocorrências")
root.geometry("450x280")

#frame superior

frame_button = tk.Frame(root)
frame_button.pack(pady=10)

botao1 = tk.Button(frame_button, text="1 - BASE FOCOS", width=15, command=lambda: selecionar_opcao("Focos"))
botao1.pack(side="left", padx=5)

botao2 = tk.Button(frame_button, text="2 - BASE NOVOS", width=15, command=lambda: selecionar_opcao("Base Novos"))
botao2.pack(side="left", padx=5)

botao3 = tk.Button(frame_button, text="3 - NOVOS", width=15, command=lambda: selecionar_opcao("Novos"))
botao3.pack(side="left", padx=5)

#frame inferior

frame_inferior = tk.Frame(root)
frame_inferior.pack(expand=True)

tk.Label(
    frame_inferior,
    text="Selecione uma opção acima",
    fg="gray"
).pack(pady=5)

status = tk.Label(
    root,
    text="",
    wraplength=420,
    justify="left"
)
status.pack(pady=5)

tk.Label(
    root,
    text="Desenvolvido por Davi Campaner"
).pack(side="bottom", pady=5)

root.mainloop()