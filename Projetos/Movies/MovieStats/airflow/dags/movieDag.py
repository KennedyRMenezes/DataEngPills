from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import timedelta


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


def get_num_views(movie):
    movie.getNumViwes()

def get_title_movie(movie):
    movie.getTitleMovie()

def save_data(movie):
    movie.saveData()

def create_movie_tasks(dag, url):

    movie = MovieData(url)

    task_get_num_views = PythonOperator(
        task_id=f"get_num_views_{url.split('/')[-2]}",
        python_callable=get_num_views,
        op_args=[movie],
        dag=dag
    )

    task_get_title_movie = PythonOperator(
        task_id=f'get_title_movie_{movie_url.split("/")[-2]}',
        python_callable=get_title_movie,
        op_args=[movie],
        dag=dag
    )

    task_save_data = PythonOperator(
        task_id=f'save_data_{movie_url.split("/")[-2]}',
        python_callable=save_data,
        op_args=[movie],
        dag=dag
    )

    # Define a ordem de execução das tasks para cada filme
    task_get_num_views >> task_get_title_movie >> task_save_data

movie_urls = [
    'https://letterboxd.com/film/la-la-land/',
    'https://letterboxd.com/film/past-lives/',
    'https://letterboxd.com/film/interstellar/'
]

with DAG ("movie_data_dag",
          description="script to get data from movies",
          schedule_interval=timedelta(hours=5),
          catchup=False) as dag:

    for movie_url in movie_urls:
        create_movie_tasks(dag, movie_url)

