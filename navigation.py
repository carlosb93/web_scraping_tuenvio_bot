from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import  types
from config import ADMIN_ID
from aiogram.utils.callback_data import CallbackData
from db_handler import is_admin

class Navigation(StatesGroup):
    main = State()  # Will be represented in storage as 'Navigation:main'
    settings = State()  # Will be represented in storage as 'Navigation:settings'



def load_main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("🔊 Elegir Productos 📦", "🔊 Elegir Tiendas 🛒")
    markup.add("⚙️ Settings")
    if is_admin(message['from']['id']):
        markup.add("🔰 Admin")
    return markup  

def load_settings(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("🔙 Atras")
    return markup   



async def go_to(view, message, text):            
    if view == 'main':
        await Navigation.main.set()
        markup = load_main(message)
        await message.answer(text, reply_markup=markup, parse_mode=types.ParseMode.HTML)  
    elif view == 'settings':
        await Navigation.settings.set()
        markup = load_settings(message)
        await message.answer(text, reply_markup=markup, parse_mode=types.ParseMode.HTML) 