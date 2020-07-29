import time
import logging
import asyncio
import requests
import threading
import pandas as pd
import aioschedule as schedule

import db_handler as db
import bot_message as bm

from os import system
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

from navigation import Navigation, go_to
from config import TOKEN, REQUEST_KWARGS

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.types.message import ContentType
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions


schedstop = threading.Event()
def schedule_run_pending():
    while not schedstop.is_set():
        schedule.run_pending()
        time.sleep(3)
        
schedthread = threading.Thread(target=schedule_run_pending)
schedthread.start()


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
proxies = { 'http': 'http://proxy.server:3128',
            'https': 'http://proxy.server:3128'
                  }

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


if REQUEST_KWARGS == '':
    bot = Bot(token=TOKEN)
else:
    bot = Bot(token=TOKEN, proxy=REQUEST_KWARGS)
    
    
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

broadcast_target = {}

async def process_main(message: types.Message):
    if db.is_registered(message['from']['id']):
        
        if message.text == "🔊 Elegir Productos 📦":
            u = db.get_user(uid=message['from']['id'])
            rply = bm.get_user_alert_status_prod(u.tgid)
            rply_inline_btn = bm.get_alert_options_btn_prod(u.tgid)
            await message.answer(text=rply, disable_notification=False,reply_markup=rply_inline_btn, parse_mode=types.ParseMode.HTML)
            
        elif message.text == "🔊 Elegir Tiendas 🛒":
            u = db.get_user(uid=message['from']['id'])
            rply = bm.get_user_alert_status_url(u.tgid)
            rply_inline_btn = bm.get_alert_options_btn_url(u.tgid)
            await message.answer(text=rply, disable_notification=False,reply_markup=rply_inline_btn, parse_mode=types.ParseMode.HTML)

        elif message.text == "⚙️ Settings":
            rply = bm.get_settings_menu(message)
            await message.answer(text=rply, parse_mode=types.ParseMode.HTML)

        elif message.text == "🔰 Admin" and db.is_admin(message['from']['id']):
            await go_to('admin', message, bm.get_static_message('WelcomeAdmin'))    
    else:
        db.create_user(name=message['from']['first_name'],lang=message['from']['language_code'],arroba=message['from']['username'],tgid=message['from']['id'])
        await message.reply(bm.get_static_message('UserNotRegister'))
        
async def process_settings(message: types.Message):
    if db.is_registered(message['from']['id']):
            
        if message.text == "🔙Go Back":
            broadcast_target[message['from']['id']] = []
            await go_to('main', message, '..')

        # elif message.text == "👥Users" and db.is_admin(message['from']['id']):
        #     await message.answer(text=bm.get_all_users_admin(), parse_mode=types.ParseMode.HTML)     
    else:
        await message.reply(bm.get_static_message('NoPriviledges'))
        
async def process_admin(message: types.Message):
    if db.is_admin(message['from']['id']):
            
        if message.text == "🔙Go Back":
            broadcast_target[message['from']['id']] = []
            await go_to('main', message, '..')

        elif message.text == "👥Users" and db.is_admin(message['from']['id']):
            await message.answer(text=bm.get_all_users_admin(), parse_mode=types.ParseMode.HTML)     
    else:
        await message.reply(bm.get_static_message('NoPriviledges'))
        
#commands
async def general_commands(message: types.Message):
    if db.is_registered(message['from']['id']):

        if message.text.startswith('/help'):
            await message.answer(bm.get_help(), parse_mode=types.ParseMode.HTML)
            
        if message.text.startswith('/removeme'):
            db.del_user_phone(tgid=message['from']['id'])
            await message.answer(bm.get_static_message('RemovePhone'), parse_mode=types.ParseMode.HTML)
        if db.is_admin(message['from']['id']):
            
            if message.text.startswith('/enable_'):
                command = message.text
                if '@' in command:
                    command = command.split('@')[0]
                    tgid = command[8:].strip()
                else:
                    tgid = command[8:].strip()
                
                db.enable_user_subscription(tgid=tgid)
                await message.answer(bm.get_static_message('Done'), parse_mode=types.ParseMode.HTML)
            
            if message.text.startswith('/disable_'):
                command = message.text
                if '@' in command:
                    command = command.split('@')[0]
                    tgid = command[9:].strip()
                else:
                    tgid = command[9:].strip()
                    
                db.disable_user_subscription(tgid=tgid)
                await message.answer(bm.get_static_message('Done'), parse_mode=types.ParseMode.HTML)
            
            if message.text.startswith('/ban_'):
                command = message.text
                if '@' in command:
                    command = command.split('@')[0]
                    tgid = command[5:].strip()
                else:
                    tgid = command[5:].strip()
                    
            if message.text.startswith('/back'):
                await go_to('main', message, '..')
                 
            if message.text.startswith('/users'):
                rply = bm.get_all_users_admin()
                await message.answer(text=rply, parse_mode=types.ParseMode.HTML)  
            
        elif message.text.startswith('/subscribe'):    
                command = message.text
                if '#' in command:
                    await go_to('main', message, bm.get_static_message('WrongNumber'))
                else:
                    if '@' in command:
                        command = command.split('@')[0]
                    phone = command[10:].strip()
                    db.update_user_phone(phone=phone,tgid=message['from']['id'])            
                    await message.answer(bm.get_static_message('Subscribed'),parse_mode=types.ParseMode.HTML)
                    
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
            
            


                   
                
       

@dp.callback_query_handler(state='*')
async def process_callback_button(callback_query: types.CallbackQuery):
    data = callback_query.data
    settings = db.get_setting_alert(kind='all')
  
    if settings:
        
        alerta_activa = db.get_alerta_activa(uid=callback_query.from_user.id,setting_id=data)
        if alerta_activa:            
            
            db.disable_conf_user(tgid=callback_query.from_user.id, name=data)# ❌ 
                    
            await bot.answer_callback_query(callback_query.id, bm.get_static_message('RemoveAlert'))
            await bot.send_message(callback_query.from_user.id, bm.get_static_message('RemoveAlert'))
        else:
            
            db.enable_conf_user(tgid=callback_query.from_user.id, name=data) # ✅
                
            await bot.answer_callback_query(callback_query.id, bm.get_static_message('AddedAlert'))
            await bot.send_message(callback_query.from_user.id, bm.get_static_message('AddedAlert'))
    else:
        
        db.enable_conf_user(tgid=callback_query.from_user.id, name=data) # ✅
                        
        await bot.send_message(callback_query.from_user.id, bm.get_static_message('AddedAlert'))
        await bot.answer_callback_query(callback_query.id, bm.get_static_message('AddedAlert'))

    
@dp.message_handler(state='*')
async def router(message: types.Message, state: FSMContext):
    # if message.forward_from or message.forward_from_chat:
    #     # await forwards(message)
    if message.is_command():
        await general_commands(message)
    if message['chat']['type'] == 'private':
        current_state = await state.get_state()
        if current_state is None:
            await go_to('main', message, bm.get_static_message('Welcome'))
            await process_main(message)
        elif current_state == Navigation.main.state:
            await process_main(message)
        elif current_state == Navigation.settings.state:
            await process_settings(message)
        elif current_state == Navigation.admin.state:
            await process_admin(message)






    
async def start_scratching():
    await alerta_start_scraping()
    
    page_url = db.get_url()
    # system("ping " + page_url)
    print(system("ping " + page_url))
    for uri in page_url:
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
        

async def schedule_all_taskts():
    schedule.every(1).minutes.do(start_scratching)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(2)
    

if __name__ == '__main__':
    dp.loop.create_task(schedule_all_taskts())
    executor.start_polling(dp)
