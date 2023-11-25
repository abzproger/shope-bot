LEXICON = {
    'new_user': 'Приветствуем вас в нашем магазине,для совершения покупок необходимо зарегестрироваться.\nДля этого нажмите кнопку ниже',
    'old_user': 'Рады видеть вас в нашем магазине электронной техники.\nВыберите интересующий вас пункт.',
    'location': 'Местоположение нашего магазина.',
    'registration': 'Регистрация',
    'start_buy': 'Начать покупки',
    'cancel': 'Отмена',
    'cart': 'Корзина',
    'select_cats': 'Выберите категорию',
    'delete': 'Удалить',
    'edit': 'Изменить',
    'edit_profile': 'Править',
    'error': 'Произошла ошибка',
    'other_answer': 'Я вас не понимаю.\nВведите <i>/help</i> для справки по командам.',
    'empty':'Товары временно отсутсвуют',
    'profile':'Профиль',
    'location':'Вот где находится наш магазин.👇🏻',
    'help':f'<i>/start - Запуск бота.\n/description - описание бота.\n/help - справка по командам.\n/location - местположение.</i>'

}
FSM_LEXICON = {'fsm_name': 'Введите ваше имя и фамилию',
               'fsm_name_fail': 'Введите ваше имя и фамилию через пробел.\nНапример: Али Алиев',
               'fsm_email': 'Введите вашу электронную почту',
               'fsm_phone_number': 'Введите ваш номер телефона',
               'error_value': 'Вы ввели неправильное значение',
               'successfuly_registration': 'Регистрация прошла успешно.Введите /start еще раз.',
               'error_email':'Такого адреса эл.почты не существует.\nУбедитесь в правильности введенных данных.'

               }

ADMIN_PANEL: list = ['Добавить товар','Добавить категорию', 'Получить все товары','Получить все категории','Удалить все', 'Отмена']

product_ikb: list = ['Править', 'Удалить']

LEXICON_ADMIN: dict = {
    'cancel_fsm': 'Вы отменили заполнение формы.',
    'admin': 'Вы вошли в режим администратора.',
    'fsm_product': 'Введите название: ',
    'fsm_category': 'Введите категорию: ',
    'fsm_description': 'Введите описание: ',
    'fsm_price': 'Введите цену: ',
    'fsm_quantity': 'Введите количество: ',
    'fsm_photo': 'Отправьте фото: ',
    'successfuly_added': 'Товар успешно добавлен в базу данных.',
    'successfuly_edit': 'Товар успешно изменен',
    'database_is_empty': 'База данных пуста.',
    'successfuly_delete': 'Удаление выполнено успешно',
    'cancel_out_of_аfms': 'Вы отменили заполнение формы',
    'edit': 'Выберите что вы хотите изменить у этого продукта: '
}

product_params: list = ['Название', 'Категорию', 'Характеристики', 'Цену', 'Фото']
pagination: list = ['Назад', 'Вперед']