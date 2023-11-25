from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from config_data.config import load_config
from aiogram.filters import BaseFilter
from database.database import db
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram import F
from keyboard.keyboard import kb_generator, ikb_generator
from lexicon.lexicon_RU import ADMIN_PANEL, LEXICON, LEXICON_ADMIN

router: Router = Router()

admin_ids = load_config().tg_bot.admin_ids


class FSMProduct(StatesGroup):
    name = State()
    category = State()
    description = State()
    price = State()
    quantity = State()
    photo = State()


class FsmCategory(StatesGroup):
    category = State()


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


# Отмена
@router.message(F.text == ADMIN_PANEL[5], ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADMIN['cancel_fsm'], reply_markup=ReplyKeyboardRemove())
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()
@router.message(F.text == ADMIN_PANEL[5], StateFilter(default_state))
async def cancel(message:Message):  # Отмена в дефолтном состоянии
    pass


# /admin
@router.message(Command(commands='admin'), IsAdmin(admin_ids))
async def admin(message: Message):
    await message.answer(text=LEXICON_ADMIN['admin'], reply_markup=kb_generator(ADMIN_PANEL))


@router.message(F.text == ADMIN_PANEL[1], IsAdmin(admin_ids), StateFilter(default_state))
async def category(message: Message, state: FSMContext):
    await message.answer('Введите новую категорию',reply_markup=ReplyKeyboardRemove())
    await state.set_state(state=FsmCategory.category)


@router.message(FsmCategory.category)
async def add_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text.capitalize())
    a = await state.get_data()
    db.insert_data(table_name='Categories', data=(None, a['category']))
    await message.answer(f'Категория "{message.text.capitalize()}" добавлена')
    await state.clear()


@router.message(F.text == ADMIN_PANEL[0], IsAdmin(admin_ids), StateFilter(default_state))
async def append_product(message: Message, state: FSMContext):
    global cats
    categories_data = db.select_data('Categories')
    cats = {category[1]: category[0] for category in categories_data}
    if not categories_data:
        await state.clear()
        await message.answer(text='Для начала добавьте категории')
    else:
        await message.answer(text='1/6 Введите название продукта:',
                             reply_markup=kb_generator([ADMIN_PANEL[5]]))
        await state.set_state(state=FSMProduct.name)


@router.message(FSMProduct.name, F.text != ADMIN_PANEL[5])
async def fsm_name(message: Message, state: FSMContext):
    await message.answer(text='2/6 Выберите категорию продукта:', reply_markup=kb_generator(list(cats.keys())))
    await state.update_data(name=message.text.capitalize())
    await state.set_state(state=FSMProduct.category)
