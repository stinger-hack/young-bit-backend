from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup


important_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Изменение в грантовой отчетности")],
        [KeyboardButton(text="Новые должностные инструкции")],
        [KeyboardButton(text="Изменение процедуры назначения собраний")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)

fill_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Готово")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)

done_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Принято")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)

yes_no_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет")],
    ],
    resize_keyboard=True,
)

sticker_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Лидер")],
        [KeyboardButton(text="Инициативный")],
        [KeyboardButton(text="Лучший советник")],
    ],
    resize_keyboard=True,
)

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="S.O.S.")],
        [KeyboardButton(text="Подарить стикер"), KeyboardButton(text="Цель на неделю")],
        [KeyboardButton(text="Нетворкинг ланч"), KeyboardButton(text="F.A.Q.")],
        [KeyboardButton(text="Важное"), KeyboardButton(text="Тестирование")],
    ]
)


questions_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Цифровые технологии")],
        [KeyboardButton(text="Отчетность")],
        [KeyboardButton(text="Медиа")],
        [KeyboardButton(text="Корпоративная культура")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)


theme_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Инструменты для сбора обратной связи ")],
        [KeyboardButton(text="Инструменты для анализа SEO")],
        [KeyboardButton(text="Настройка iOS")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)
