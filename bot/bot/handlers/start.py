from aiogram import types, Router


router = Router()

@router.message(commands=['start'])
async def start_handler(msg: types.Message):
    await msg.reply("Группа создана")

