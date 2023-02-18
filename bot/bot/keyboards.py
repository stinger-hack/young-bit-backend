from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup

yes_no_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет")],
    ],
    resize_keyboard=True,
)

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="S.O.S.")],
        [KeyboardButton(text="Подарить стикер"), KeyboardButton(text="Цель на неделю")],
        [KeyboardButton(text="Нетворкинг ланч"), KeyboardButton(text="Задать вопрос")],
        [KeyboardButton(text="Важное")],
    ]
)
