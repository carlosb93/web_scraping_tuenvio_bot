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
        
        response = requests.get(uri.code, proxies=proxies) # go to the url and get it
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
                    get_modulos_href_5ta(soup=soup,page_url=uri.code)
                    sleep(5)
                else:
                    print(uri.code)
                    # get_modulos_href(soup,uri)
        break


def get_modulos_href(soup=None, page_url=None):
    # modulo parser
    div = soup.find('div', attrs={'class':'center_column col-xs-12 col-sm-9'})
    if div:
        tag_warning = div.find('p', attrs={'class':'alert alert-warning'})
        if tag_warning:
            print('tu envio vacio')
            sleep(4)
            
        else:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(botfrom.alerta_basica())
            # tag_ahrefs = div.find('a' ,href=True, attrs={'class':'invarseColor'})
            # tag_a = tag_ahrefs.get('href')
            # urlconcat = str(page_url)+'/'+str(tag_a)
            # get_to_module(urlconcat)

def get_modulos_href_5ta(soup=None, page_url=None):
    # modulo parser
    div = soup.find('div', attrs={'class':'center_column col-xs-12 col-sm-9'})
    if div:
        tag_warning = div.find('p', attrs={'class':'alert alert-warning'})
        if tag_warning:
            print('5ta vacio')
            
            sleep(4)
            main()
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

def schedule_all_taskts():
    schedule.every(1).minutes.do(asyncio.run_coroutine_threadsafe,main())
    
schedule.run_pending()
sleep(1)
    
if __name__ == '__main__':
    schedule_all_taskts()
