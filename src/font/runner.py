from src.pipelines.pontuais_pipeline import run_pipeline
from src.web.ServiceRoutineClimbLowOccurence import ServiceRoutineClimbLowOccurence


def main(modo: str):

    print(f"Iniciando pipeline selecionada: {modo}")
    generated_files = run_pipeline(modo)

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


if __name__ == "__main__":
    main("Focos")