from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db


async def all_teachers_default_keyboard():
    teachers = await db.select_users(role="teacher")
    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    for teacher in teachers:
        text_button = f"{teacher['full_name']}"
        markup.insert(KeyboardButton(text_button))

    markup.insert(KeyboardButton(text="🔙 Orqaga"))

    return markup


async def all_teachers_and_next_default_keyboard():
    teachers = await db.select_users(role="teacher")
    markup = ReplyKeyboardMarkup()
    markup.resize_keyboard = True
    markup.row_width = 2
    for teacher in teachers:
        text_button = f"{teacher['full_name']}"
        markup.insert(KeyboardButton(text_button))

    markup.insert(KeyboardButton(text="Keyingi 🔜"))

    return markup
