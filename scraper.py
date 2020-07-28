import os
import asyncio
import schedule
import requests
import logging
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import db_handler as db
from urllib.parse import urlparse
from collections import Counter
from stop_words import get_stop_words
import main as botfrom


# http://proxy.server:3128
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
proxies = { 'http': 'http://proxy.server:3128',
            'https': 'http://proxy.server:3128'
                  }
# headers = { 'http': 'http://proxy.server:3128',
#             'https': 'http://proxy.server:3128'
#                   }

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

    
def main():
    page_url = db.get_url()
   
    for uri in page_url:
        # my_url = input(uri.code)
        # print('Grabbing... '+my_url)
        # domain = urlparse(my_url).netloc # domain name
        # print("via domain", domain)
        print(uri.code)
        response = requests.get(uri.code,headers=headers) # go to the url and get it
        print("Status is", response.status_code) # 200, 403, 404, 500, 503

        if response.status_code != 200: # not equal, == equal
            print("You can't scrape this", response.status_code)
        
        else:
            print("Scraping..", uri.code)
                
            content = response.content
            # content = browser.page_source
            soup = BeautifulSoup(content, 'html.parser')
            if soup:
    
                if 'https://5tay42.enzona.net/nuevos-productos' == uri.code:
                        div = soup.find('div', attrs={'class':'center_column col-xs-12 col-sm-9'})
                        if div:
                            tag_warning = div.find('p', attrs={'class':'alert alert-warning'})
                            if tag_warning:
                                print('5ta vacio')
                                sleep(4)
                            else:
                                print('5ta alerta')
                                loop = asyncio.get_event_loop()
                                loop.run_until_complete(botfrom.alerta_basica())
            
                    # get_modulos_href_5ta(soup=soup,page_url=uri.code)
                    # sleep(5)
                else:
                    a = soup.find_all('a', href=True,attrs={'class':'invarseColor'})
                    if a:
                        for href in a:
                            if 'MÓDULOS' in href.text or 'Modulos' in href.text:
                                href = href.get('href')
                                url = uri.code.split('Products')[0]
                                url+= href
                                print('----------Accediendo a modulo en tu envio con ruta---------')
                                print(url)
                                get_modulos_href(page_url=url)
                            else:
                                pass
                    
        pass


def get_modulos_href(page_url=None):
    # modulo parser
    response = requests.get(page_url,headers=headers) # go to the url and get it
    print("Status is", response.status_code) # 200, 403, 404, 500, 503

    if response.status_code != 200: # not equal, == equal
        print("You can't scrape this", response.status_code)  
    else:
        print("Scraping..", page_url)
                
        content = response.content
        # content = browser.page_source
        soup = BeautifulSoup(content, 'html.parser')
        if soup:
            listado = soup.find('ul',attrs={'class':'hProductItems clearfix'})
            if listado:
                items = listado.find_all('li',attrs={'class':'span3 clearfix'})
                if items:
                    for item in items:
                        a = item.find('a',href=True,attrs={'class':'invarseColor'})
                        # title = a.text       # titulo del modulo
                        href = a.get('href')
                        url = page_url.split('Products')[0]
                        url+= href
                        get_modulos_content(url)
                
                        
def get_modulos_content(page_url=None):
    # modulo parser
    response = requests.get(page_url,headers=headers) # go to the url and get it
    print("Status is", response.status_code) # 200, 403, 404, 500, 503

    if response.status_code != 200: # not equal, == equal
        print("You can't scrape this", response.status_code)  
    else:
        print("Scraping..", page_url)
                
        content = response.content
        # content = browser.page_source
        soup = BeautifulSoup(content, 'html.parser')
        if soup:
            title = soup.find('div',attrs={'class':'product-title'})
            title = title.find('h4').text
            
            product_set = soup.find('div',attrs={'class':'product-set'})
            if product_set:
                price = product_set.find('div',attrs={'class':'product-price'})
                price = price.find('span').text
                
            product_desc = soup.find('div',attrs={'id':'ctl00_cphPage_formProduct_ctl00_productDetail_DetailTabs_tabKit_kitItems_pnlKitItems'})
            if product_desc:
                table = soup.find('table',attrs={'id':'ctl00_cphPage_formProduct_ctl00_productDetail_DetailTabs_tabKit_kitItems_gridKitItems'})
                elements = table.find_all('td',attrs={'class':'desc'})
                if elements:
                    prod_list ='Productos:\n'
                    for element in elements:
                        prod = element.find('a',href=True,attrs={'target':'_blank'})
                        prod_list += '- {}\n'.format(prod.text) 
                    print(prod_list)
                    loop = asyncio.get_event_loop()
                    # page_url ='https://www.tuenvio.cu/carlos3/Item?ProdPid=914122&depPid=46095&page=0'
                    # title ='Kit de Alimentos No.24'
                    # price ='10.85 CUC'
                    # prod_list ='1 L-Aceite de soya\n425 g-Sardinas en tomate\n2 kg- Muslo de pollo'
                    
                    loop.run_until_complete(botfrom.alerta_tu_envio(page_url,title,price,prod_list))
                    
        
            
                        
                
                        
                        
    

def get_modulos_href_5ta(soup=None, page_url=None):
    # modulo parser
    div = soup.find('div', attrs={'class':'center_column col-xs-12 col-sm-9'})
    if div:
        tag_warning = div.find('p', attrs={'class':'alert alert-warning'})
        if tag_warning:
            print('5ta vacio')
            loop = asyncio.get_event_loop()
            loop.run_until_complete(botfrom.alerta_basica())
            sleep(4)
        else:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(botfrom.alerta_basica())
            # tag_ahrefs = div.find('a' ,href=True, attrs={'class':'invarseColor'})
            # tag_a = tag_ahrefs.get('href')
            # urlconcat = str(page_url)+'/'+str(tag_a)
            # get_to_module(urlconcat)

      

def get_to_module(modulo_href=None):
    try:
        
        my_url = input(modulo_href) 

        print("Grabbing...", my_url)
        domain = urlparse(my_url).netloc # domain name
        print("via domain", domain)

        

        response = requests.get(my_url, proxies=proxies) # go to the url and get it
        print("Status is", response.status_code) # 200, 403, 404, 500, 503

        if response.status_code != 200: # not equal, == equal
            print("You can't scrape this", response.status_code)
        else:
            print("Scraping..")
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            if soup:
                print('start')
    except requests.exceptions.ConnectionError:
        requests.status_code = "Connection refused"
        sleep(4)




def parse_module_content(modulo_href=None):

    classes={
        'product-price',
        'product-rate',
        'product-info'
    }

    response = requests.get(modulo_href)
    if response.status_code != 200: # not equal, == equal
        print("You can't scrape this", response.status_code)
    else:
        print("Scraping..")
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        if soup:
            for c in classes:
               python_jobs = soup.find_all('div',attrs={'class':c})
               if python_jobs:
                    if 'price' in c:  #price analisis
                        for p_job in python_jobs:
                            precio = p_job.find('dd').get_text()
                            print('precio:'+ precio)
    
                    elif 'rate' in c:  #ratings
                        for p_job in python_jobs:
                            rate = p_job.find('dd').get_text()
                            print('rate:'+rate)
    
                    elif 'info' in c:  #information
                        for p_job in python_jobs:
                            info = p_job.find('dd').get_text()
                            print('info:'+info)
    
                    else:
                        print('fin')

        else:
            pass

schedule.every(1).minutes.do(main)

while True:    
    schedule.run_pending()
    sleep(5)

