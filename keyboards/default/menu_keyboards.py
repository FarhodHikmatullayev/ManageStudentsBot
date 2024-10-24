from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_to_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔙 Bosh Menyu"),
        ]
    ]
)

use_bot_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🤖 Botdan foydalanish 🤖")
        ]
    ]
)


async def main_menu_default_keyboard(user_role):
    if user_role == "admin":
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="👩‍🏫 O'qituvchilar")  # O'qituvchilar tugmasi
                ],
                [
                    KeyboardButton(text="🔴 Jarima bali qo'yish")  # Guruhlar tugmasi
                ],
                [
                    KeyboardButton(text="📊 Jarima ballarini ko'rish")
                ]
            ]
        )
    elif user_role == "teacher":
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="🔴 Jarima bali qo'yish")  # Guruhlar tugmasi
                ],
            ]
        )
    else:
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="🔙 Bosh Menyu")  # Mening Profilim tugmasi
                ]
            ]
        )

    return markup


go_back_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="🔙 Orqaga")
        ]
    ]
)
