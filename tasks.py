import time
import logging
import asyncio
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse
import db_handler as db
import bot_message as bm 
from aiogram import types
from main import bot


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
proxies = { 'http': 'http://proxy.server:3128',
            'https': 'http://proxy.server:3128'
                  }
async def alerta_start_scraping():
    users = db.get_all_users()
    for u in users:
        if db.is_admin(u.tgid):
            await bot.send_message(u.tgid, bm.get_static_message('start_scrap'), disable_notification=True, parse_mode=types.ParseMode.HTML)
    
            
async def alerta_basica():
    page_url = 'https://5tay42.enzona.net/nuevos-productos'
    title = '5ta'
    module = db.get_modulo(title=title)
    if module:
        min = datetime.datetime.fromtimestamp(module.created_at/1000)
        max = datetime.datetime.fromtimestamp(time.time()/1000)
        created = (max-min).total_seconds() / 60
        if created > 10:
    
            db.set_modulo(page_url=page_url,title=title)
            users = db.get_all_users()
            for u in users:
                await bot.send_message(u.tgid, bm.get_static_message('5ta'), disable_notification=True, parse_mode=types.ParseMode.HTML)
            
        # await broadcaster(bm.get_static_message('5ta'), broadcast_target[u.tgid], log, bot)
    else:
        db.set_modulo(page_url=page_url,title=title)
        users = db.get_all_users()
        for u in users:
            await bot.send_message(u.tgid, bm.get_static_message('5ta'), disable_notification=True, parse_mode=types.ParseMode.HTML)
    return 'fin'
        
        
async def alerta_basica_prevent(url=None,price=None,title=None):
    users = db.get_all_users()
    formated = '⚠️⚠️ Modulo Unknown⚠️⚠️!!!\n'
    formated += '\n{}'.format(title)
    formated += '\nPrecio: {}'.format(price)
    formated += '\n<a href="{}">Ver modulo...</a>'.format(url)
    
    page_url = url
    title = title
    
    module = db.get_modulo(title=title)
    if module:
        min = datetime.datetime.fromtimestamp(module.created_at/1000)
        max = datetime.datetime.fromtimestamp(time.time()/1000)
        created = (max-min).total_seconds() / 60
        if created > 10:
            db.set_modulo(page_url=page_url,title=title)
            for u in users:
                await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
            
                # await broadcaster(bm.get_static_message('5ta'), broadcast_target[u.tgid], log, bot)
    else:
        db.add_modulo(page_url=page_url,title=title)
        users = db.get_all_users()
        for u in users:
            await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
        
        
    
async def alerta_tu_envio(page_url=None,title=None,price=None,prod_list=None):
    module = db.get_modulo(title=title)
    if module:
        min = datetime.datetime.fromtimestamp(module.created_at/1000)
        max = datetime.datetime.fromtimestamp(time.time()/1000)
        created = (max-min).total_seconds() / 60
        if created > 10:
            # update alert y notifico
            db.set_modulo(page_url=page_url,title=title)
            users = db.get_all_users()
            formated = '⚠️⚠️⚠️ Alerta Tu envio ⚠️⚠️⚠️\n'
            for u in users:
                formated += '{}\n'.format(title)
                formated += '<b>Precio: {}</b>\n\n'.format(price)
                formated += '{}'.format(prod_list)
                formated += '\n<a href="{}">Ver modulo...</a>'.format(page_url)

                settings_user = db.get_user_alerts(uid=u.tgid)
                if settings_user:
                    for a in settings_user:
                        settings = db.get_setting_alert(settings_user=a,kind='url')
                        if settings:
                            for i in settings:
                                settings_prod = db.get_setting_alert(settings_user=a,kind='alert')
                                if settings_prod:
                                    for j in settings:
                                        url = page_url.split('/')[3]
                                        if i.code in prod_list and url in j.code:
                                            await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
                                        elif i.code in prod_list:
                                            await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
                                        elif url in j.code:
                                            await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
                else:
                    await bot.send_message(u.tgid, bm.get_static_message('Conf_alerts'), disable_notification=True, parse_mode=types.ParseMode.HTML)
              
    else:
        #notifico
        db.add_modulo(page_url=page_url,title=title)
        users = db.get_all_users()
        formated = '⚠️⚠️⚠️ Alerta Tu envio ⚠️⚠️⚠️\n'
        for u in users:
            formated += '{}\n'.format(title)
            formated += '<b>Precio: {}</b>\n\n'.format(price)
            formated += '{}'.format(prod_list)
            formated += '\n<a href="{}">Ver modulo...</a>'.format(page_url)

            settings_user = db.get_user_alerts(uid=u.tgid)
            if settings_user:
                for a in settings_user:
                    settings = db.get_setting_alert(settings_user=a,kind='url')
                    if settings:
                        for i in settings:
                            settings_prod = db.get_setting_alert(settings_user=a,kind='alert')
                            if settings_prod:
                                for j in settings:
                                    url = page_url.split('/')[3]
                                    if i.code in prod_list and url in j.code:
                                        await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
                                    elif i.code in prod_list:
                                        await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
                                    elif url in j.code:
                                        await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
            else:
                await bot.send_message(u.tgid, bm.get_static_message('Conf_alerts'), disable_notification=True, parse_mode=types.ParseMode.HTML)
        
        return True
    
    
    
    

async def start_scratching(bot):
    await alerta_start_scraping()
    
    page_url = db.get_url()
    # system("ping " + page_url)
    for uri in page_url:
        uri.code = 'https://www.tuenvio.cu/carlos3/Products?depPid=0'
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
                                time.sleep(4)
                            else:
                                print('5ta alerta')
                                await alerta_basica()
            
                    # get_modulos_href_5ta(soup=soup,page_url=uri.code)
                    # sleep(5)
                else:
                    a = soup.find_all('a', href=True,attrs={'class':'invarseColor'})
                    if a:
                        for href in a:
                            if 'MÓDULOS' in href.text or 'Modulos' in href.text or 'Combos de productos' in href.text:
                                href = href.get('href')
                                url = uri.code.split('Products')[0]
                                url+= href
                                print('----------Accediendo a modulo en tu envio con ruta---------')
                                print(url)
                                await get_modulos_href(page_url=url)
                            else:
                                pass
                    
        pass


async def get_modulos_href(page_url=None):
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
                        await get_modulos_content(url)
                
                        
async def get_modulos_content(page_url=None):
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
            print(title)
            if title:
                title = title.find('h4')
                print(title)
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
                        await alerta_tu_envio(page_url,title,price,prod_list)
            else:
                print('alerta temprana')
                title = soup.find('td',attrs={'class':'DescriptionValue'})
                if title:
                    title = title.find('span').text
                    price = soup.find('td',attrs={'class':'PrecioProdList'})
                    if price:
                        price = price.text
                        print('excecute alerta temprana')
                        await alerta_basica_prevent(url=page_url,price=price,title=title)
                
                        

async def get_modulos_href_5ta(soup=None, page_url=None):
    # modulo parser
    div = soup.find('div', attrs={'class':'center_column col-xs-12 col-sm-9'})
    if div:
        tag_warning = div.find('p', attrs={'class':'alert alert-warning'})
        if tag_warning:
            print('5ta vacio')
            await alerta_basica()
            time.sleep(4)
        else:
            await alerta_basica()