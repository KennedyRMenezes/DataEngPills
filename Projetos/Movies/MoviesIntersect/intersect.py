from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-extensions')
options.add_argument('--disable-software-rasterizer')

class Usuario:

    def __init__ (self, url: str):
        self.url = url
        self.soup = self.getSoup(self.url)

        self.now = ''
        self.movies_watchlist = []
        self.num_pages = self.get_num_pages()
        self.name = self.get_name()


        self.get_all_movies_in_watchlist()


    def getSoup(self, url):
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


    def get_num_pages(self):
        pages_div = self.soup.find('div', {'class': 'paginate-pages'})
        
        if pages_div:
            ul_element = pages_div.find('ul')
            
            if ul_element:
                return len(ul_element.find_all('li'))
            else:
                print("Elemento <ul> não encontrado.")
        else:
            print("Elemento <div class='paginate-pages'> não encontrado.")


    def get_movies(self, url):
        html_movies = self.getSoup(url)

        list_movies = html_movies.find('ul', {'class': 'poster-list -p125 -grid -scaled128'})
        
        if not list_movies:
            print("Lista de filmes não encontrada.")
            return []

        movie_data = []
        for movie in list_movies.find_all('li', {'class': 'poster-container'}):
            div = movie.find('div')
            if div:
                film_name = div.get('data-film-name', '')
                film_release_year = div.get('data-film-release-year', '')
                movie_data.append({'name': film_name, 'year': film_release_year})

        return movie_data


    def get_name(self):

        url_splited = self.url.split("/")
        return url_splited[3]

    
    def get_movies_for_page(self, url):
        return self.get_movies(url)


    def get_all_movies_in_watchlist(self):
        print(f"Searching movies from {self.name}")
        urls = self._generate_urls()
        self.movies_watchlist = self._fetch_movies(urls)


    def _generate_urls(self):
        return [self.url + f"/page/{page + 1}/" for page in range(self.num_pages)]


    def _fetch_movies(self, urls):
        with ThreadPoolExecutor() as executor:
            return [movie for movies in executor.map(self.get_movies_for_page, urls) for movie in movies]


    def match_movies(self, other):

        print(f"\nMovies in common from {self.name} and {other.name}\n")

        common = [dicionario for dicionario in self.movies_watchlist if dicionario in other.movies_watchlist]
        print(f"{'Movie'.ljust(20)} | {'Year'.ljust(20)}")
        for movie in common:
            if movie["name"] == '':
                pass
            else:
                print(f"{str(movie['name']).ljust(20)} | {str(movie['year']).ljust(20)}")
        print()
    
def buscar_filmes_usuario(url):
    return Usuario(url)


if __name__ == "__main__":

    start_time = time.time()

    

    print()

    urls = [
        "https://letterboxd.com/dorettto/watchlist/",
        "https://letterboxd.com/kennedyrmenezes/watchlist/"
    ]

    # Usando ThreadPoolExecutor para buscar os filmes dos usuários em paralelo
    with ThreadPoolExecutor() as executor:
        usuarios = list(executor.map(buscar_filmes_usuario, urls))

    user1, user2 = usuarios
    user1.match_movies(user2)

    end_time = time.time()

    print("Execution time: ", end_time-start_time)