import customtkinter as ctk
from tkinter import messagebox
import threading
from src.font.runner import main

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

nomes_modo = {
    "Focos": "Base Focos",
    "Base Novos": "Base Dia",
    "Novos": "Base Novos"
}

modo_execucao = None
botao = None

def selecionar_opcao(modo):
    global modo_execucao, botao
    modo_execucao = modo

    limpar_frame_inferior()

    botao = ctk.CTkButton(frame_inferior, text="Executar Automação", width=200, height=45, corner_radius=12, font=("Arial", 15, "bold"), command=iniciar)
    botao.pack(pady=10)

    status.configure(text=f"Modo selecionado: {nomes_modo[modo]}")

def limpar_frame_inferior():
    for widget in frame_inferior.winfo_children():
        widget.destroy()

def iniciar():

    if not modo_execucao:
        messagebox.showwarning("Aviso", "Selecione uma opção")
        return

    status.configure(text="Processando...")
    botao.configure(state="disabled")

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

def finalizar_execucao():
    def atualizar():
        status.configure(text="Processo finalizado com sucesso!")
        botao.configure(state="normal")
    root.after(0, atualizar)

def focos():
    main("Focos")
    finalizar_execucao()

def execute():
    print("teste")
    finalizar_execucao()

def base_novos():
    main("Base Novos")
    finalizar_execucao()

def novos():
    main("Novos")
    finalizar_execucao()

#janela
root = ctk.CTk()
root.title("Marcação de Ocorrências")
root.geometry("520x260")

#frame superior

frame_button = ctk.CTkFrame(root, fg_color="transparent")
frame_button.pack(pady=10)

botao1 = ctk.CTkButton(frame_button, text="1 - BASE FOCOS", width=140, height=40, corner_radius=10, font=("Arial", 14, "bold"), command=lambda: selecionar_opcao("Focos"))
botao1.pack(side="left", padx=5)

botao2 = ctk.CTkButton(frame_button, text="2 - BASE DIA", width=140, height=40, corner_radius=10, font=("Arial", 14, "bold"), command=lambda: selecionar_opcao("Base Novos"))
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
    font=("Arial", 13),
    wraplength=480,
    justify="center"
)
status.pack(pady=5)

ctk.CTkLabel(
    root,
    fg_color="transparent",
    text="Desenvolvido por Davi Campaner",
    font=("Arial", 13, "bold"),
).pack(side="bottom", pady=8)

root.mainloop()