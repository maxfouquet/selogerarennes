import pandas as pd
import time
import bs4
import random
import requests
# !pip install fake-useragent
from fake_useragent import UserAgent
import itertools as it
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from requests_html import HTMLSession

def index(request):
    template = 'articles.html'
    
    return render(request, template, {})

def api(request):
    template = 'articles.html'
    token = 'https://www.seloger.com/immobilier/locations/immo-rennes-35/bien-appartement/?LISTING-LISTpg='

    def get_pages(token, nb):
        pages = []
        for i in range(1,nb+1):
            j = token + str(i)
            pages.append(j)
        return pages

    pages = get_pages(token,3)

    # https://www.proxy-list.download/HTTPS
    proxies = pd.read_csv('proxy_list.txt', header = None)
    proxies = proxies.values.tolist()
    proxies = list(it.chain.from_iterable(proxies))

    def get_data(pages):
        df = pd.DataFrame()
        parameters = ['data-prix','data-codepostal','data-idagence','data-idannonce','data-nb_chambres','data-nb_pieces','data-surface','data-typebien']
        ua = UserAgent()
        proxy_pool = it.cycle(proxies)
        
        while len(pages) > 0:
            for i in pages:
            # on lit les pages une par une et on initialise une table vide pour ranger les données d'une page     
                df_f = pd.DataFrame()
            # itération dans un liste de proxies    
                proxy = next(proxy_pool)
            # essai d'ouverture d'une page   
                try:
                    response = requests.get(i,proxies={"http": proxy, "https": proxy}, headers={'User-Agent': ua.random},timeout=5)
                    time.sleep(random.randrange(1,5))
            # lecture du code html et la recherche des balises <em>
                    soup = bs4.BeautifulSoup(response.text, 'html.parser')
                    print(soup)
                    # print(em_box)
            # extraction des données        
                    # for par in parameters:
                    #     l = []
                    #     for el in em_box:
                    #         j = el[par]
                    #         l.append(j)
                    #     l = pd.DataFrame(l, columns = [par])
                    #     df_f = pd.concat([df_f,l], axis = 1)
                    # df = df.append(df_f, ignore_index=True)
                    # pages.remove(i)
                    # print(df.shape)
                except:
                    print("Skipping. Connnection error")
                    
        return df

    data = get_data(pages)
    print(data)

    return render(request, template, {})