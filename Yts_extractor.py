from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
from urllib.error import HTTPError, URLError
cont = 0
movies_dict = {}
num_pages = 3
while cont < num_pages:

    cont += 1
    try:
        req = Request(
        f'https://yts./browse-movies?page={cont}',
        headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()


    except HTTPError as e:
        print(e)
    except URLError:
        print('The server could not be found!')

    else:

        soup = BeautifulSoup(html,'html.parser')
        movies = soup.find_all(class_="browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4")
        '''listas temporarias que serão geradas a cada pagina:
        (Não estamos usando .append() em uma lista existente) Porque queremos ir salvando no excel
        durante o LOOP, sem ocupar muita memoria... se formos adicionando a uma list,a acumulando dados,
        e gerar o excel apenas depois do loop, vamos ter muita info na memoria e se travar durante o processo,
        nao teremos nenhum dado consolidado...
        Do jeito que está pelo menos se por exemplo travar na pagin a 10, ja tera 10 paginas no arquivo..'''
        movie_title = [movie.find(class_="browse-movie-title").get_text() for movie in movies]
        movie_year = [movie.find(class_="browse-movie-year").get_text() for movie in movies]
        movie_link = [movie.find(class_="browse-movie-link").get('href') for movie in movies]
        movie_db = pd.DataFrame({'Titulo' : movie_title,'Ano' : movie_year,'link de download' : movie_link,})

        movie_db.to_csv('extração_yts2.csv', mode='a', header=False)
        print(cont)

