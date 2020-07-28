import asyncio
import logging
import schedule
# import scraper
import threading
import time
from datetime import datetime

from navigation import Navigation, go_to
from config import TOKEN, REQUEST_KWARGS
import db_handler as db
import bot_message as bm

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions


schedstop = threading.Event()
def schedule_run_pending():
    while not schedstop.is_set():
        schedule.run_pending()
        time.sleep(3)
        
schedthread = threading.Thread(target=schedule_run_pending)
schedthread.start()



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
                    
async def alerta_basica():
    users = db.get_all_users()
    for u in users:
        await bot.send_message(u.tgid, bm.get_static_message('5ta'), disable_notification=True, parse_mode=types.ParseMode.HTML)
        # await broadcaster(bm.get_static_message('5ta'), broadcast_target[u.tgid], log, bot)
    
async def alerta_tu_envio(page_url=None,title=None,price=None,prod_list=None):
    users = db.get_all_users()
    formated = '⚠️⚠️⚠️ Alerta Tu envio ⚠️⚠️⚠️\n'
    for u in users:
        formated += '{}\n'.format(title)
        formated += '<b>Precio: {}</b>\n\n'.format(price)
        formated += '{}'.format(prod_list)
        formated += '\n<a href="{}">Ver modulo...</a>'.format(page_url)
        await bot.send_message(u.tgid, formated, disable_notification=True, parse_mode=types.ParseMode.HTML)
    

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

# exitFlag = 0
 
# class myThread(threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID =threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print("Starting " + self.name)
#         # function
#         scraper.start_gain_url()
#         print("Exiting " + self.name)
        

def schedule_all_taskts():
    pass
    # thread1 = myThread(1,"Thread-1", 1)
    # schedule.every(3).minutes.do(asyncio.run_coroutine_threadsafe, thread1.start(),bot.loop)
    

if __name__ == '__main__':
    executor.start_polling(dp)
