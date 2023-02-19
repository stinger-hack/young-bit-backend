from aiogram import Router
import bot.keyboards as kb

router = Router()

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)
from aiogram import F, Router
from aiogram.fsm.context import FSMContext


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

@router.message(commands=["start"])
async def start_handler(msg: Message):
    await msg.reply(f"Привет, {msg.from_user.first_name}", reply_markup=kb.menu_kb)


@router.message(F.text == "Нетворкинг ланч")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(NetworkLunch.start)
    await message.answer(
        "Нетворкинг ланч - это обед со случайным сотрудником. Хотели бы вы принять участие?",
        reply_markup=kb.yes_no_kb,
    )



@router.message(NetworkLunch.start)
async def start_lunch(message: Message, state: FSMContext):
    await state.set_state(Form.menu)
    if message.text.lower() == "нет":
        await message.answer(
            "Очень жаль :(",
            reply_markup=kb.menu_kb,
        )
    else:
        ...

@router.message(NetworkLunch.choose)
async def choose_network(message: Message, state: FSMContext):
    aw


@router.message(F.text == "Тестирование")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Sos.situation)
    await message.answer(
        "Опишите ситуацию",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(F.text == "Важное")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Sos.situation)
    await message.answer(
        "Опишите ситуацию",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(F.text == "Задать вопрос")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Sos.situation)
    await message.answer(
        "Опишите ситуацию",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(F.text == "Цель на неделю")
async def process_name(message: Message, state: FSMContext) -> None:
    await state.set_state(Sos.situation)
    await message.answer(
        "Опишите ситуацию",
        reply_markup=ReplyKeyboardRemove(),
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
