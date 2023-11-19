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


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message(Command(commands='admin'), IsAdmin(admin_ids))
async def admin(message: Message):
    await message.answer(text=LEXICON_ADMIN['admin'], reply_markup=kb_generator(ADMIN_PANEL))


@router.message(F.text == ADMIN_PANEL[3], StateFilter(default_state))
async def cancel(message: Message):  # Отмена в дефолтном состоянии
    await message.answer(text='Отмена', reply_markup=ReplyKeyboardRemove())


@router.message(F.text == ADMIN_PANEL[3], ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADMIN['cancel_fsm'], reply_markup=ReplyKeyboardRemove())
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@router.message(F.text == ADMIN_PANEL[0], IsAdmin(admin_ids), StateFilter(default_state))
async def append_product(message: Message, state: FSMContext):
    await message.answer(text='1/6 Введите название продукта:', reply_markup=kb_generator([ADMIN_PANEL[3]]))
    await state.set_state(state=FSMProduct.name)


@router.message(FSMProduct.name)
async def fsm_name(message: Message, state: FSMContext):
    global cats
    categories_data = db.select_data('Categories')
    cats = {category[1]: category[0] for category in categories_data}
    await message.answer(text='2/6 Введите категорию продукта:', reply_markup=kb_generator(list(cats.keys())))
    await state.update_data(name=message.text.capitalize())
    await state.set_state(state=FSMProduct.category)


@router.message(F.text, FSMProduct.category)
async def fsm_category(message: Message, state: FSMContext):
    if list(cats.keys()).count(f"{message.text}"):
        await state.update_data(category=cats[f"{message.text}"])
        await message.answer(text='3/6 Введите описание товара:', reply_markup=kb_generator([ADMIN_PANEL[3]]))

        await state.set_state(state=FSMProduct.description)
    else:
        await message.answer('Нажмите на кнопку!')


@router.message(FSMProduct.description)
async def fsm_description(message: Message, state: FSMContext):
    await message.answer(text='4/6 Введите стоимость товара (руб.)', reply_markup=kb_generator([ADMIN_PANEL[3]]))
    await state.update_data(description=message.text.capitalize())
    await state.set_state(state=FSMProduct.price)


@router.message(F.text.isdigit(), FSMProduct.price)
async def fsm_price(message: Message, state: FSMContext):
    await message.answer(text='5/6 Введите число товаров в наличии:', reply_markup=kb_generator([ADMIN_PANEL[3]]))
    await state.update_data(price=int(message.text))
    await state.set_state(state=FSMProduct.quantity)


@router.message(F.text.isdigit(), FSMProduct.quantity)
async def fsm_quantity(message: Message, state: FSMContext):
    await message.answer(text='6/6 Почти готово.Отправьте фото товара:', reply_markup=kb_generator([ADMIN_PANEL[3]]))
    await state.update_data(quantity=int(message.text))
    await state.set_state(state=FSMProduct.photo)


@router.message(F.content_type == 'photo', FSMProduct.photo)  # Вводим фото
async def fsm_photo(message: Message, state: FSMContext):
    URI_INFO = f'https://api.telegram.org/bot{load_config().tg_bot.token}/getFile?file_id='
    URI = f'https://api.telegram.org/file/bot{load_config().tg_bot.token}/'
    for photo in message.photo:
        # Обработка каждой фотографии
        file_id = photo.file_id
        # Остальные операции с фотографией

    await state.update_data(photo=file_id)
    data = await state.get_data()
    db.insert_data(table_name='Products', data=(
        None,
        data['name'],
        data['category'],
        data['description'],
        data['price'],
        data['quantity'],
        data['photo']))

    await message.answer(text='Товар успешно добавлен!',reply_markup=ReplyKeyboardRemove())  # Сообщаем об успешной операции
    await state.clear()



@router.message(F.text == ADMIN_PANEL[1], IsAdmin(admin_ids))
async def get_product(message: Message):
    if db.select_data('Products'):
        product_data = db.select_data('Products')
        product_data = [i for i in product_data[0:]]

        for data in product_data:
            data = [str(a) for a in data]
            cats_name = [x for x in db.select_data('Categories', f'CategoryID = {data[2]} ')[0]]
            await message.answer_photo(photo=data[-1],
                                       caption=f'<b>{data[1]}</b>\nКатегория: {cats_name[1]}\nХарактеристики: {data[3]}\nКол-во на складе: {data[5]}\nЦена: {data[4]}\nid: {data[0]}',
                                       reply_markup=ikb_generator(1, LEXICON['delete']))

    else:
        await message.answer(LEXICON_ADMIN['database_is_empty'])


@router.message(F.text == ADMIN_PANEL[2], IsAdmin(admin_ids))
async def delete_all_products(message: Message):
    if db.select_data('Products'):
        db.delete_data('Products', condition='ProductID > 0')
        await message.answer(LEXICON_ADMIN['successfuly_delete'])
    else:
        await message.answer(LEXICON_ADMIN['database_is_empty'])


@router.callback_query(F.data == LEXICON['delete'])
async def delete_product(callback: CallbackQuery):
    await callback.message.delete()
    id = callback.message.caption.split(' ')[-1]
    db.delete_data(table_name='Products', condition=f'ProductID = {id}')
    await callback.message.answer(text='Товар удалён.', reply_markup=ReplyKeyboardRemove())

