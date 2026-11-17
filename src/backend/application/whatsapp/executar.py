from src.backend.application.whatsapp.pipeline import run_pipeline
from src.backend.infrastructure.vcom.vcom_bot import ServiceRoutineClimbLowOccurence
from src.backend.infrastructure.files.paths import DOWNLOADS_DIR
import os

def executar(modo: str, sheets_selecionadas=None):

    def limpar_downloads():
        pasta = DOWNLOADS_DIR

        if not os.path.exists(pasta):
            return

        for arquivo in os.listdir(pasta):
            caminho = os.path.join(pasta, arquivo)

            if os.path.isfile(caminho):
                os.remove(caminho)

        print("Pasta downloads limpa.")

    print(f"Iniciando pipeline selecionada: {modo}")
    generated_files = run_pipeline(modo, sheets_selecionadas=sheets_selecionadas)

    print("Arquivos gerados:")
    for item in generated_files:
        print(item)

    print("Iniciando automação VCOM...")

    bot = ServiceRoutineClimbLowOccurence()
    bot.login_vcom()

    for item in generated_files:

        credor = item["credor"]
        file_path = item["path"]

        print(f"Importando {credor} -> {file_path}")

        bot.import_carga_vcom(credor, file_path)

    print("Processo finalizado com sucesso!")
    limpar_downloads()
