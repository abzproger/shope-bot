from aiogram import Router
from aiogram import F
from aiogram.filters import Command, CommandStart,Filter
from aiogram.types import Message


from keyboard.keyboard import kb_generator, ikb_generator
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from dataclasses import dataclass
from lexicon.lexicon_RU import LEXICON



router: Router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Приветствуем вас в нашем магазине.\nВведите /help для справки по командам',reply_markup=kb_generator([LEXICON['start_buy'], LEXICON['cart'], LEXICON['cancel']]))

@router.message(Command('help'))
async def help(message:Message):
    await message.answer(f'<i>/start - Запуск бота.\n/description - описание бота.\n/help - справка по командам.\n/location - местположение.</i>')

@router.message(Command('location'))
async def location (message:Message):
    await message.answer('Вот где находится наш магазин.👇🏻')
    await message.answer_location(latitude=42.73303393290414,longitude= 47.134653774337586)


