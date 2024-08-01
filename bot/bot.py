import sys
import time
import json
sys.path.append('.')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service as ChromeService
from anticaptchaofficial.recaptchav2enterpriseproxyless import *

J = {}
class bt_challenge():
    def __init__(self):
        self.setup_browser()

    def setup_browser(self):
        options_browser = Options()
        options_browser.add_argument("--disable-notifications")
        options_browser.add_argument("--disable-dev-shm-usage")
        servico_chrome = ChromeService(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=servico_chrome, options=options_browser)
        self.browser.maximize_window()

    def scrap(self):
        n = 0
        while n == 0:
            try:
                pass
            except Exception as error:
                print(f'Erro ao acessar o Banco de dados: {error}')
            time.sleep(2)