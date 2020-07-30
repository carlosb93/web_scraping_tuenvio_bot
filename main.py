import time
import logging
import asyncio
import requests
import threading
import pandas as pd

import tasks
import db_handler as db
import bot_message as bm

from os import system
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from navigation import Navigation, go_to
from config import TOKEN, REQUEST_KWARGS

scheduler = AsyncIOScheduler()
bgscheduler = BackgroundScheduler()

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.types.message import ContentType
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions


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

        elif message.text == "⚙️ Configuración":
            rply = bm.get_settings_menu(message)
            await message.answer(text=rply, parse_mode=types.ParseMode.HTML)

        elif message.text == "🔰 Admin" and db.is_admin(message['from']['id']):
            await go_to('admin', message, bm.get_static_message('WelcomeAdmin'))    
    else:
        db.create_user(name=message['from']['first_name'],lang=message['from']['language_code'],arroba=message['from']['username'],tgid=message['from']['id'])
        await message.reply(bm.get_static_message('UserNotRegister'))
        
async def process_settings(message: types.Message):
    if db.is_registered(message['from']['id']):
            
        if message.text == "🔙Atrás":
            broadcast_target[message['from']['id']] = []
            await go_to('main', message, '..')

        # elif message.text == "👥Users" and db.is_admin(message['from']['id']):
        #     await message.answer(text=bm.get_all_users_admin(), parse_mode=types.ParseMode.HTML)     
    else:
        await message.reply(bm.get_static_message('NoPriviledges'))
        
async def process_admin(message: types.Message):
    if db.is_admin(message['from']['id']):
            
        if message.text == "🔙Atrás":
            broadcast_target[message['from']['id']] = []
            await go_to('main', message, '..')

        elif message.text == "👥Usuarios" and db.is_admin(message['from']['id']):
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
            await message.answer(bm.get_static_message('RemovePhone',ulang='Spanish'), parse_mode=types.ParseMode.HTML)
        if db.is_admin(message['from']['id']):
            
            if message.text.startswith('/enable_'):
                command = message.text
                if '@' in command:
                    command = command.split('@')[0]
                    tgid = command[8:].strip()
                else:
                    tgid = command[8:].strip()
                
                db.enable_user_subscription(tgid=tgid)
                await message.answer(bm.get_static_message('Done',ulang='Spanish'), parse_mode=types.ParseMode.HTML)
            
            if message.text.startswith('/disable_'):
                command = message.text
                if '@' in command:
                    command = command.split('@')[0]
                    tgid = command[9:].strip()
                else:
                    tgid = command[9:].strip()
                    
                db.disable_user_subscription(tgid=tgid)
                await message.answer(bm.get_static_message('Done',ulang='Spanish'), parse_mode=types.ParseMode.HTML)
            
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
                    await go_to('main', message, bm.get_static_message('WrongNumber',ulang='Spanish'))
                else:
                    if '@' in command:
                        command = command.split('@')[0]
                    phone = command[10:].strip()
                    db.update_user_phone(phone=phone,tgid=message['from']['id'])            
                    await message.answer(bm.get_static_message('Subscribed',ulang='Spanish'),parse_mode=types.ParseMode.HTML)
 

async def check_db_alert(bot):
    modulos = db.get_module_all()
    if modulos:
        for modulo in modulos:
            min = datetime.fromtimestamp(modulo.created_at/1000)
            max = datetime.fromtimestamp(time.time()/1000)
            created = (max-min).total_seconds() / 60
            if created > 10:
                db.unset_modulo(page_url=modulo.url,title=modulo.name,price=modulo.price)
                await alerta_tu_envio(page_url=modulo.url,title=modulo.name,price=modulo.price,prod_list=modulo.listado)
                
            else:
                db.unset_modulo(page_url=modulo.url,title=modulo.name,price=modulo.price)
                await alerta_tu_envio(page_url=modulo.url,title=modulo.name,price=modulo.price,prod_list=modulo.listado)
            
           
    
async def alerta_tu_envio(page_url=None,title=None,price=None,prod_list=None):
    users = db.get_all_users()
    formated = '⚠️⚠️⚠️ Alerta Nuevo Módulo ⚠️⚠️⚠️\n'
    for u in users:
        formated += '{}\n'.format(title)
        formated += '<b>Precio: {}</b>\n\n'.format(price)
        formated += '{}'.format(prod_list)
        formated += '\n<a href="{}">Ver Módulo...</a>'.format(page_url)

        settings_user = db.get_user_alerts(uid=u.tgid)
        if settings_user:
            for a in settings_user:
                settings = db.get_setting_alert(settings_user=a,kind='url')
                if settings:
                    for j in settings:
                        url = page_url.split('/')[3]
                        if url in j.code:
                            settings_prod = db.get_setting_alert(settings_user=a,kind='alert')
                            if settings_prod:
                                for i in settings_prod:
                                    if i.code in prod_list:
                                        await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
                            else:
                                await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
                else:
                    settings_prod = db.get_setting_alert(settings_user=a,kind='alert')
                    if settings_prod:
                        for i in settings_prod:
                            if i.code in prod_list:
                                await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
                                    
                                    
                
        else:
            await bot.send_message(u.tgid, bm.get_static_message('Conf_alerts',ulang='Spanish'), disable_notification=True, parse_mode=types.ParseMode.HTML)
        
        return True                   

            
            


                   
                
       

@dp.callback_query_handler(state='*')
async def process_callback_button(callback_query: types.CallbackQuery):
    data = callback_query.data
    settings = db.get_setting_alert(kind='all')
  
    if settings:
        
        alerta_activa = db.get_alerta_activa(uid=callback_query.from_user.id,setting_id=data)
        if alerta_activa:            
            
            db.disable_conf_user(tgid=callback_query.from_user.id, name=data)# ❌ 
            
            if db.is_kind_prod(data):
                rply = bm.get_user_alert_status_prod(callback_query.from_user.id)
                rply_inline_btn = bm.get_alert_options_btn_prod(callback_query.from_user.id)
            else:
                rply = bm.get_user_alert_status_url(callback_query.from_user.id)
                rply_inline_btn = bm.get_alert_options_btn_url(callback_query.from_user.id)
            
            await bot.answer_callback_query(callback_query.id, bm.get_static_message('RemoveAlert',ulang='Spanish'))
            await bot.edit_message_text(text=rply,chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,reply_markup=rply_inline_btn, parse_mode=types.ParseMode.HTML)        
        else:
            
            db.enable_conf_user(tgid=callback_query.from_user.id, name=data) # ✅
            
            if db.is_kind_prod(data):
                rply = bm.get_user_alert_status_prod(callback_query.from_user.id)
                rply_inline_btn = bm.get_alert_options_btn_prod(callback_query.from_user.id)
            else:
                rply = bm.get_user_alert_status_url(callback_query.from_user.id)
                rply_inline_btn = bm.get_alert_options_btn_url(callback_query.from_user.id)
                
            await bot.answer_callback_query(callback_query.id, bm.get_static_message('AddedAlert',ulang='Spanish'))            
            await bot.edit_message_text(text=rply,chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,reply_markup=rply_inline_btn, parse_mode=types.ParseMode.HTML)
    else:
        
        db.enable_conf_user(tgid=callback_query.from_user.id, name=data) # ✅
        
        if db.is_kind_prod(data):
            rply = bm.get_user_alert_status_prod(callback_query.from_user.id)
            rply_inline_btn = bm.get_alert_options_btn_prod(callback_query.from_user.id)
        else:
            rply = bm.get_user_alert_status_url(callback_query.from_user.id)
            rply_inline_btn = bm.get_alert_options_btn_url(callback_query.from_user.id)
            
        await bot.send_message(callback_query.from_user.id, bm.get_static_message('AddedAlert',ulang='Spanish'))
        await bot.edit_message_text(text=rply,chat_id=callback_query.message.chat.id,message_id=callback_query.message.message_id,reply_markup=rply_inline_btn, parse_mode=types.ParseMode.HTML)

    
@dp.message_handler(state='*')
async def router(message: types.Message, state: FSMContext):
    # if message.forward_from or message.forward_from_chat:
    #     # await forwards(message)
    if message.is_command():
        await general_commands(message)
    if message['chat']['type'] == 'private':
        current_state = await state.get_state()
        if current_state is None:
            await go_to('main', message, bm.get_static_message('Welcome',ulang='Spanish'))
            await process_main(message)
        elif current_state == Navigation.main.state:
            await process_main(message)
        elif current_state == Navigation.settings.state:
            await process_settings(message)
        elif current_state == Navigation.admin.state:
            await process_admin(message)

        

def schedule_all_taskts():
    bgscheduler.add_job(tasks.start_scratching, 'interval', minutes=2)
    bgscheduler.start()
    
    scheduler.add_job(check_db_alert, 'cron', hour='*', minute='*', second=40, kwargs={'bot': bot})    
    scheduler.start()
    

if __name__ == '__main__':
    schedule_all_taskts()
    executor.start_polling(dp, skip_updates=True)
