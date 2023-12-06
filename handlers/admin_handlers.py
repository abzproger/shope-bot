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


@router.message(F.text, FSMProduct.category)
async def fsm_category(message: Message, state: FSMContext):
   if list(cats.keys()).count(f"{message.text}"):
       await state.update_data(category=cats[f"{message.text}"])
       await message.answer(text='3/6 Введите описание товара:', reply_markup=kb_generator([ADMIN_PANEL[5]]))

       await state.set_state(state=FSMProduct.description)
   else:
        await message.answer('Нажмите на кнопку!')



@router.message(FSMProduct.description)
async def fsm_description(message: Message, state: FSMContext):
    await message.answer(text='4/6 Введите стоимость товара (руб.)', reply_markup=kb_generator([ADMIN_PANEL[5]]))
    await state.update_data(description=message.text.capitalize())
    await state.set_state(state=FSMProduct.price)


@router.message(F.text.isdigit(), FSMProduct.price)
async def fsm_price(message: Message, state: FSMContext):
    await message.answer(text='5/6 Введите число товаров в наличии:', reply_markup=kb_generator([ADMIN_PANEL[5]]))
    await state.update_data(price=int(message.text))
    await state.set_state(state=FSMProduct.quantity)


@router.message(F.text.isdigit(), FSMProduct.quantity)
async def fsm_quantity(message: Message, state: FSMContext):
    await message.answer(text='6/6 Почти готово.Отправьте фото товара:', reply_markup=kb_generator([ADMIN_PANEL[4]]))
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

    await message.answer(text='Товар успешно добавлен!',
                         reply_markup=ReplyKeyboardRemove())  # Сообщаем об успешной операции
    await state.clear()


@router.message(F.text == ADMIN_PANEL[2], IsAdmin(admin_ids))
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


@router.message(F.text == ADMIN_PANEL[4], IsAdmin(admin_ids))
async def delete_all_products(message: Message):
    if db.select_data('Products'):
        db.delete_data('Products', condition='ProductID > 0')
        await message.answer(LEXICON_ADMIN['successfuly_delete'])
    else:
        await message.answer(LEXICON_ADMIN['database_is_empty'])

@router.message(F.text == ADMIN_PANEL[3],IsAdmin(admin_ids))
async def get_all_cats (message:Message):
    if db.select_data('Categories'):
        await message.answer('<b><u>Категории:</u></b>')
        for i in db.select_data('Categories'):
            await message.answer(text=f'{i[1]}',reply_markup=ikb_generator(1,LEXICON['delete']))
    else:
        await message.answer('Создайте для начала категории.')


@router.callback_query(F.data == LEXICON['delete'], IsAdmin(admin_ids))
async def del_cat(callback: CallbackQuery):
    category_id = [i for i in db.select_data(table_name='Categories',condition=f"CategoryName = '{callback.message.text}'",data='CategoryID')[0]][0]
    if category_id:
            # Удаляем продукты, связанные с этим CategoryID из таблицы Products
        db.delete_data(table_name='Products', condition=f"CategoryID = {category_id}")
            # Удаляем записи из таблицы Cart, связанные с этим CategoryID
        db.delete_data(table_name='Cart', condition=f"CategoryID = {category_id}")
            # Удаляем саму категорию из таблицы Categories
        db.delete_data(table_name='Categories', condition=f"CategoryID = {category_id}")
        await callback.answer(show_alert=True,text=f'Категория - {callback.message.text} удалена из базы данных.\n.')
        await callback.message.delete()




