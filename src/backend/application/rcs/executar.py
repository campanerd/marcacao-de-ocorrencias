import os
from src.backend.infrastructure.files.historico_rcs import registrar_envio
from src.backend.application.rcs.pipeline import run_pipeline
from src.backend.infrastructure.files.paths import DOWNLOADS_DIR
from src.backend.infrastructure.vcom.vcom_bot import ServiceRoutineClimbLowOccurence


def _limpar_downloads():
    if not os.path.exists(DOWNLOADS_DIR):
        return

    for nome in os.listdir(DOWNLOADS_DIR):
        caminho = os.path.join(DOWNLOADS_DIR, nome)
        if os.path.isfile(caminho):
            os.remove(caminho)

    print("Pasta downloads limpa.")


def executar(arquivos):
    print(f"Iniciando pipeline RCS: {len(arquivos)} arquivo(s)")
    arquivos_gerados = run_pipeline(arquivos)

    if not arquivos_gerados:
        print("Nenhum arquivo gerado, nada para importar no VCOM.")
        return

    print("Iniciando automação VCOM...")
    bot = ServiceRoutineClimbLowOccurence()
    bot.login_vcom()

    for item in arquivos_gerados:
        print(f"Importando {item['credor']} -> {item['path']}")
        bot.import_carga_vcom(item["credor"], item["path"])

    registrar_envio({item["arquivo"] for item in arquivos_gerados})
    print("Histórico de envios atualizado.")

    print("Processo finalizado com sucesso!")
    _limpar_downloads()
