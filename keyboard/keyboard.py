from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from lexicon.lexicon_RU import LEXICON

def kb_generator(buttons: list):
    keyboard: list[KeyboardButton] = [
        KeyboardButton(text=str(i)) for i in buttons]

    # Инициализируем билдер
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    builder.row(*keyboard, width=3)

    # Создаем объект клавиатуры, добавляя в него кнопки
    return builder.as_markup(resize_keyboard=True,one_time_keyboard=True)



# Функция для формирования инлайн-клавиатуры на лету
def ikb_generator(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()

