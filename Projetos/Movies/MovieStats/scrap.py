from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
from openpyxl import load_workbook
from datetime import datetime
from bs4 import BeautifulSoup
import time
import re

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-extensions')
options.add_argument('--disable-software-rasterizer')


class MovieData:

    def __init__ (self, url: str):
        self.url = url
        self.title = ""
        self.views = ""
        self.now = ""

        self.print_current_time("Class init")

        self.soup = self.getSoup(self.url)
        
        # self.getNumViwes()
        # self.getTitleMovie()
        # self.saveData()

    def __del__(self):
        self.print_current_time("Class end")

    
    def print_current_time(self, event: str):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n####### {event}: {current_time} #######\n")


    def getSoup(self, url):
        print("Scrapping...")
        chrome_service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=chrome_service, options=options)

        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'poster-container'))
            )
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")
            driver.quit()
            return None

        html_pagina = driver.page_source
        soup = BeautifulSoup(html_pagina, 'html.parser')
        driver.quit()

        return soup
    
    def getNumViwes(self):
        print("\nGetting data...")
        views = self.soup.find('a', {'class': 'has-icon icon-watched icon-16 tooltip'})
        views = views.get('data-original-title', '')
        views = re.search(r'\d+', views.replace(',', '')).group()
        self.views = views

    def getTitleMovie(self):
        titulo = self.soup.find('span', {'class': 'frame-title'})
        titulo = titulo.text.strip()
        ##Retira o ano do titulo do filme
        titulo = titulo[:-6].strip()
        self.title = titulo

    def saveData(self):
        print("\nSaving data...")
        now = datetime.now()
        self.now = now.strftime("%Y-%m-%d %H:%M:%S")

        file = './movies_stats.xlsx'
        wb = load_workbook(file)
        ws = wb.active

        ws.append([self.title, self.views, self.now])

        wb.save(file)

        print("\nDone!")

        return self
    

if __name__ == "__main__":

    MovieData("https://letterboxd.com/film/la-la-land/")
    MovieData("https://letterboxd.com/film/past-lives/")