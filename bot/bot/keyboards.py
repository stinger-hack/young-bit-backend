from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup

menu_kb = ReplyKeyboardMarkup(keyboard=
    [
        [KeyboardButton(text="S.O.S.")],
        [KeyboardButton(text="Подарить стикер"), KeyboardButton(text="Цель на неделю")],
        [KeyboardButton(text="Нетворкинг ланч"), KeyboardButton(text="Задать вопрос")],
        [KeyboardButton(text="Важное")],
    ]
)
