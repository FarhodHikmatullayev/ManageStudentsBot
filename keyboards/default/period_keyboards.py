from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

period_default_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="1 kun"),
            KeyboardButton(text="5 kun")
        ],
        [
            KeyboardButton(text="1 hafta"),
            KeyboardButton(text="10 kun")
        ],
        [
            KeyboardButton(text="15 kun"),
            KeyboardButton(text="20 kun")
        ],
        [
            KeyboardButton(text="1 oy"),
            KeyboardButton(text="2 oy")
        ],
        [
            KeyboardButton(text="3 oy"),
            KeyboardButton(text="6 oy")
        ],
        [
            KeyboardButton(text="1 yil"),
            KeyboardButton(text="Hammasi")
        ],
        [
            KeyboardButton(text="🔙 Bosh Menyu"),
        ]
    ]
)
