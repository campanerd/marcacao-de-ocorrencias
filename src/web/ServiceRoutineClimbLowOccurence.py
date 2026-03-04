import os
import sys 
from dotenv import load_dotenv

from fastapi import HTTPException

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
from datetime import datetime
import pandas as pd


if getattr(sys, 'frozen', False):
    # Se for um executável, o caminho base é o diretório do próprio executável
    base_path = os.path.dirname(sys.executable) 
else:
    # Se for um script Python normal, o caminho base é o diretório do script
    base_path = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(base_path, '.env')
load_dotenv(dotenv_path=dotenv_path)


class ServiceRoutineClimbLowOccurence:
    
    
    
    def __init__(self) -> None:
     
        
        chrome_binary_path = "/usr/bin/google-chrome"
        self.options = Options()
        #self.options.binary_location = chrome_binary_path
        #self.options.add_argument("--headless")#type:ignore
        self.options.add_argument("--no-sandbox")#type:ignore
        self.options.add_argument("--disable-dev-shm-usage")#type:ignore
        self.options.add_argument("--disable-gpu")#type:ignore
        self.options.add_argument("--remote-debugging-port=9222")#type:ignore
        
        #prefs = {"download.default_directory": self.path_folder}
        #self.options.add_experimental_option("prefs",prefs)#type:ignore
        #self.driver_service= 
        self.credor_buffers:dict[str,str] = {}
        self.service = ChromeService(executable_path=ChromeDriverManager().install())#type:ignore
        
        self._login_vcom = os.getenv("LOGIN_VCOM")
        self._password_up = os.getenv("PASSWORD_VCOM")


    def login_vcom(self):
        
            self._driver = webdriver.Chrome(service=self.service,options=self.options)
            self._wait = WebDriverWait(self._driver,40)
            self._driver.maximize_window()
            self._driver.get("http://192.168.0.144:8081/VcomCob/Login")

            email = self._wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-login"]')))
            email = self._driver.find_element(By.XPATH,'//*[@id="input-login"]')
            email = email.send_keys(self._login_vcom)#type:ignore

            password = self._wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-senha"]')))
            password = self._driver.find_element(By.XPATH,'//*[@id="input-senha"]')
            password = password.send_keys(self._password_up)#type:ignore

            login = self._wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="botao-login"]')))
            login = self._driver.find_element(By.XPATH,'//*[@id="botao-login"]')
            login = login.click()
            sleep(5)
            if self._driver.current_url != 'http://192.168.0.144:8081/VcomCob':
                raise HTTPException(
                    status_code=403,detail="Credenciais Invalidas"
                )

            return self._driver




    def import_carga_vcom(self,credor:str, caminho_arquivo:str):

            self._driver.get("http://192.168.0.144:8081/VcomCob/ImportacaoCredores/Index")

            select_element = self._wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selTipoImportacao"]')))
            select_element = self._driver.find_element(By.XPATH,'//*[@id="selTipoImportacao"]')
            select = Select(select_element)
            select.select_by_index(1)

            next = self._wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="btn-prosseguir"]')))
            next = self._driver.find_element(By.XPATH,'//*[@id="btn-prosseguir"]')
            next = next.click()

            import_layout= self._wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="chkImportarUsandoLayoutCobsystems"]')))
            import_layout = self._driver.find_element(By.XPATH,'//*[@id="chkImportarUsandoLayoutCobsystems"]')
            import_layout = import_layout.click()

            select_provedor = self._wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selProvedorImportacao"]')))
            select_provedor = self._driver.find_element(By.XPATH,'//*[@id="selProvedorImportacao"]')
            provedor = Select(select_provedor)

            provedor.select_by_visible_text(str(credor).replace("_"," "))

            next = self._wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="btn-prosseguir"]')))
            next = self._driver.find_element(By.XPATH,'//*[@id="btn-prosseguir"]')
            next = next.click()

            input_file = self._wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="files"]')))
            input_file = self._driver.find_element(By.XPATH,'//*[@id="files"]')
            
            
            incluir_arq = self._wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="btn-arquivo"]')))
            incluir_arq = self._driver.find_element(By.XPATH,'//*[@id="btn-arquivo"]')
            incluir_arq = incluir_arq.click()

            
                
            # Faz o upload do arquivo temporário
            input_file.send_keys(caminho_arquivo)#type:ignore
            

            sleep(3)
            # # Descomentar para importar
            import_carga = self._wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="btn-importar"]')))
            import_carga = self._driver.find_element(By.XPATH,'//*[@id="btn-importar"]')
            import_carga = import_carga.click()

            sleep(60)

if __name__ == "__main__":
    bot = ServiceRoutineClimbLowOccurence()
    bot.login_vcom()
    bot.import_carga_vcom("Daycoval Daycred", r"C:\Users\davi.fernandes\Documents\vcom\Whatsapp_geral_04_03_Daycoval_Daycred_04.03.2026_teste.csv")