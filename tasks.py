import time
import sys
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse
import db_handler as db



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
proxies = { 'http': '190.107.5.51:3128',
            'https': '190.107.5.51:3128'
                  }
      
    

def start_scratching():
    
    
    page_url = db.get_url()
    # system("ping " + page_url)
    for uri in page_url:
        try:
            print("Start request to:", uri.code)
            response = requests.get(uri.code,headers=headers,proxies=proxies) # go to the url and get it
        
        
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
                                    pass
                                else:
                                    module = db.get_modulo(title='5ta y 42')
                                    if module:
                                        min = datetime.fromtimestamp(module.created_at/1000)
                                        max = datetime.fromtimestamp(time.time()/1000)
                                        created = (max-min).total_seconds() / 60
                                        if created > 10:
                                            db.set_modulo(page_url=uri.code,title='5ta y 42',price=None,listado=None)
                                    else:
                                        db.add_modulo(page_url=uri.code,title='5ta y 42',price='',listado='')
                                                           
                                    
                
                        # get_modulos_href_5ta(soup=soup,page_url=uri.code)
                        # sleep(5)
                    else:
                        a = soup.find_all('a', href=True,attrs={'class':'invarseColor'})
                        if a:
                            for href in a:
                                if 'MÓDULOS' in href.text or 'Modulos' in href.text or 'Combos de productos' in href.text or 'Combos' in href.text or 'Miscelaneas' in href.text:  
                                    href = href.get('href')
                                    url = uri.code.split('Products')[0]
                                    url+= href
                                    print('----------Accediendo a modulo en tu envio con ruta---------')
                                    print(url)
                                    get_modulos_href(page_url=url)
                                else:
                                    pass
                        
        except Exception:
            print(sys.exc_info()[0])
            continue


def get_modulos_href(page_url=None):
    # modulo parser
    try:
        print("Start request to:", page_url)
        response = requests.get(page_url,headers=headers,proxies=proxies) # go to the url and get it
    
     # go to the url and get it
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
    except Exception:
        print(sys.exc_info()[0])
                
                        
def get_modulos_content(page_url=None):
    # modulo parser
    try:
        print("Start request to:", page_url) 
        response = requests.get(page_url,headers=headers,proxies=proxies) # go to the url and get it
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
                if title:
                    title = title.find('h4')
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
                            
                            module = db.get_modulo(title=title)
                            if module:
                                min = datetime.fromtimestamp(module.created_at/1000)
                                max = datetime.fromtimestamp(time.time()/1000)
                                created = (max-min).total_seconds() / 60
                                if created > 10:
                                    db.set_modulo(page_url=page_url,title=title,price=price,listado=prod_list)
                                elif module.prod_list == '':
                                    db.set_modulo(page_url=page_url,title=title,price=price,listado=prod_list)
                            else:
                                db.add_modulo(page_url=page_url,title=title,price=price,listado=prod_list)
                else:
                    title = soup.find('td',attrs={'class':'DescriptionValue'})
                    if title:
                        title = title.find('span').text
                        price = soup.find('td',attrs={'class':'PrecioProdList'})
                        if price:
                            price = price.text
                            module = db.get_modulo(title=title)
                            if module:
                                min = datetime.fromtimestamp(module.created_at/1000)
                                max = datetime.fromtimestamp(time.time()/1000)
                                created = (max-min).total_seconds() / 60
                                if created > 10:
                                    db.set_modulo(page_url=page_url,title=title,price=price,listado='')
                            else:
                                db.add_modulo(page_url=page_url,title=title,price=price,listado='')
    except Exception:
        print(sys.exc_info()[0])                      
                
                        

