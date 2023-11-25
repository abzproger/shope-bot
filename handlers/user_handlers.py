from aiogram import Router
from aiogram import F
from aiogram.filters import Command, CommandStart, Filter
from aiogram.types import Message, URLInputFile, BufferedInputFile, FSInputFile
from keyboard.keyboard import kb_generator, ikb_generator
from lexicon.lexicon_RU import LEXICON, LEXICON_ADMIN
from database.database import db

router: Router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Приветствуем вас в нашем магазине.\nВведите /help для справки по командам',
                         reply_markup=kb_generator([LEXICON['start_buy'], LEXICON['cart'], LEXICON['cancel']]))


@router.message(Command('help'))
async def help(message: Message):
    await message.answer(
        f'<i>/start - Запуск бота.\n/description - описание бота.\n/help - справка по командам.\n/location - местположение.</i>')


@router.message(Command('location'))
async def location(message: Message):
    await message.answer('Вот где находится наш магазин.👇🏻')
    await message.answer_location(latitude=42.73303393290414, longitude=47.134653774337586)


@router.message(F.text == LEXICON['start_buy'])
async def start_buy(message:Message):
    cats = {category[1]: category[0] for category in db.select_data('Categories') }
    if cats:
        await message.answer(text=LEXICON['select_cats'],reply_markup=kb_generator(list(cats.keys())))
    else:

        # Отправка файла из файловой системы
        image_from_pc = FSInputFile("emty.jpg")
        await message.answer_photo(
            image_from_pc,
            caption=LEXICON['empty']
        )


#router.message(F.text)
#sync def select_cats(message: Message):
#   cats = {category[1]: category[0] for category in db.select_data('Categories')}
#   if list(cats.keys()).count(f"{message.text}"):
#       product_data = [i for i in db.select_data(table_name="Products",
#                                                 condition=f"CategoryID = {cats[message.text]}")[0]]
#       await message.answer_photo(photo=product_data[-1],
#                                  caption=f"<b>{product_data[1]}</b>\nКатегория:  {message.text}\nХарактерстики:  {product_data[3]}\nСтоимость:  {product_data[4]}")
