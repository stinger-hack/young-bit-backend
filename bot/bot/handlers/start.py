from aiogram import Router
import bot.keyboards as kb
from bot.requests.common import get_random_user, get_user_by_fullname

router = Router()

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from bot.app import bot, storage


class Form(StatesGroup):
    menu = State()
    sos = State()
    goal = State()
    faq = State()
    sticker_gift = State()
    random_lunch = State()
    important = State()
    testing = State()


class Sos(StatesGroup):
    situation = State()


class NetworkLunch(StatesGroup):
    start = State()
    choose = State()


class StickerGift(StatesGroup):
    search_user = State()
    select_sticker = State()


class Important(StatesGroup):
    news_list = State()
    card = State()


class FormState(StatesGroup):
    fill = State()


class QuestionState(StatesGroup):
    start = State()
    card = State()
    theme = State()


@router.message(commands=["start"])
async def start_handler(msg: Message):
    await bot.send_message(msg.chat.id, f"Привет, {msg.from_user.first_name}", reply_markup=kb.menu_kb)


@router.message(Important.news_list)
@router.message(F.text == "Важное")
async def process_name(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Важное:",
        reply_markup=kb.important_kb,
    )


@router.message(F.text == "Изменение процедуры назначения собраний")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Important.news_list)
    await message.answer(
        "Собрание назначается только при согласии всех руководителей управления, минимум за 3 рабочих дня.",
        reply_markup=kb.done_kb,
    )


@router.message(F.text == "Назад")
async def back_button(message: Message) -> None:
    await message.answer(
        "Меню:",
        reply_markup=kb.menu_kb,
    )


@router.message(F.text == "Нетворкинг ланч")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(NetworkLunch.start)
    await message.answer(
        "Нетворкинг ланч - это обед со случайным сотрудником. Хотели бы вы принять участие?",
        reply_markup=kb.yes_no_kb,
    )


@router.message(NetworkLunch.start)
async def start_lunch(message: Message, state: FSMContext):
    if message.text.lower() == "нет":
        await state.set_state(Form.menu)
        await message.answer(
            "Очень жаль :(",
            reply_markup=kb.menu_kb,
        )
    else:
        await state.set_state(NetworkLunch.choose)
        result = await get_random_user()
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=result["img_link"],
            caption=f"Ваш собеседник на сегодня: {result['fullname']}.\nСоветую поговорить на тему: {result['theme']}.",
            reply_markup=kb.menu_kb,
        )


@router.message(F.text == "Подарить стикер")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(StickerGift.search_user)
    await message.answer(
        "Кому вы хотите подарить стикер? Напишите ФИ (Иванов Иван)",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(StickerGift.search_user)
async def sticker_gift(message: Message, state: FSMContext) -> None:
    split_str = message.text.split(" ")
    if len(split_str) != 2:
        await state.set_state(Form.menu)
        return await message.answer(
            "Человек не найден",
            reply_markup=kb.menu_kb,
        )
    last_name, first_name = split_str
    result = await get_user_by_fullname(first_name=first_name, last_name=last_name)
    if not result:
        await state.set_state(Form.menu)
        await message.answer(
            "Человек не найден",
            reply_markup=kb.menu_kb,
        )
    await state.set_state(StickerGift.select_sticker)
    await message.answer(
        "Выберите стикер",
        reply_markup=kb.sticker_kb,
    )


@router.message(StickerGift.select_sticker)
async def select_sticker(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.menu)

    if message.text == 'Лидер':
        await bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEHzXFj8a43Lap1bbiPinwW6Ka3oviz9wACEyQAAthHkEvCBXLs_w8mey4E')
    elif message.text == 'Инициативный':
        await bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEHzXNj8a45njOJuIWwotkG43ZU5u7UNgACWSIAAsyqkUuEkcDmp6QYIy4E')
    else:
        await bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEHzXVj8a47BC6ZlcA602mnDcWv8pVcRQACRSUAAnMYkUuOjaI4d5wSfy4E')

    await message.answer(
        "Стикер успешно отправлен",
        reply_markup=kb.menu_kb,
    )


@router.message(F.text == "Тестирование")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Sos.situation)
    is_filled = await storage.get_data(bot, f"form/{message.chat.id}")
    if is_filled:
        await message.answer(
            "Вы уже заполнили форму",
            reply_markup=kb.menu_kb,
        )
    else:
        await state.set_state(FormState.fill)
        link = "https://docs.google.com/forms/d/1KbUMssWyaAL6_lfAiFVqNTIro3EtL0f5SspHkrxUsAo/viewform"
        await message.answer(
            f"Заполните форму:\n{link}",
            reply_markup=kb.fill_kb,
        )


@router.message(FormState.fill)
async def fill_form(message: Message, state: FSMContext) -> None:
    if message.text == "Готово":
        await state.set_state(Form.menu)
        await storage.set_data(bot=bot, key=f"form/{message.chat.id}", data=["test"])
        await message.answer(
            "Форма заполнена. Спасибо!",
            reply_markup=kb.menu_kb,
        )
    else:
        await state.set_state(Form.menu)
        await message.answer(
            "Меню:",
            reply_markup=kb.menu_kb,
        )


@router.message(F.text == "Важное")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Sos.situation)
    await message.answer(
        "Опишите ситуацию",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(F.text == "F.A.Q.")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(QuestionState.start)
    await message.answer(
        "Выберите раздел",
        reply_markup=kb.questions_kb,
    )


@router.message(QuestionState.start)
async def choose_category(message: Message, state: FSMContext) -> None:
    if message.text == "Назад":
        await state.set_state(Form.menu)
        await message.answer(
            "Меню:",
            reply_markup=kb.menu_kb,
        )
    if message.text == "Цифровые технологии":
        await state.set_state(QuestionState.card)
        await message.answer(
            "Выберите тему",
            reply_markup=kb.theme_kb,
        )


@router.message(QuestionState.card)
async def choose_category(message: Message, state: FSMContext) -> None:
    if message.text == "Назад":
        await state.set_state(Form.menu)
        await message.answer(
            "Меню:",
            reply_markup=kb.questions_kb,
        )

    if message.text == "Настройка iOS":
        await state.set_state(Form.menu)
        await bot.send_document(
            message.chat.id, "https://storage.yandexcloud.net/onboarding/f60baaa5e9804bd29c43f8931c3f10f7.pdf", caption="Памятка по настройке", reply_markup=kb.menu_kb
        )


@router.message(F.text == "Цель на неделю")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.goal)
    prev_goal = await storage.get_data(bot, "goal")
    if prev_goal:
        await message.answer(
            "Вы хотите изменить цель?",
            reply_markup=kb.yes_no_kb,
        )
    else:
        await message.answer(
            "Напишите цель на неделю",
            reply_markup=ReplyKeyboardRemove(),
        )


@router.message(Form.goal)
async def fill_goal(message: Message, state: FSMContext):
    await message.answer(
        "Цель сохранена",
        reply_markup=kb.menu_kb,
    )


@router.message(F.text == "S.O.S.")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Sos.situation)
    await message.answer(
        "Опишите ситуацию",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Sos.situation)
async def process_situation(message: Message, state: FSMContext) -> None:
    # TODO: send to HR
    await state.set_state(Form.menu)
    await message.answer(
        'Вопрос отправлен, ждите ответа и проверяйте раздел "Важноe"',
        reply_markup=kb.menu_kb,
    )
