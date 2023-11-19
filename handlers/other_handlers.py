from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_RU import  LEXICON



router: Router = Router()

# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON['other_answer'])


