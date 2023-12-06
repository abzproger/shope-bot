import sqlite3
from datetime import datetime


class DataBase:
    def __init__(self, db_name):
        self.con = sqlite3.connect(database=db_name)
        self.cur = self.con.cursor()

    def create_table(self, table_name, columns):  # Создаем таблицу
        column = ', '.join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column})"
        self.cur.execute(query)
        self.con.commit()

    def insert_data(self, table_name, data):  # Вставляем в таблицу
        placeholders = ', '.join(['?' for _ in range(len(data))])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cur.execute(query, data)
        self.con.commit()

    def select_data(self,table_name,condition=None,data='*'):
        query = f"SELECT {data} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows


    def update_data(self, table_name, data, condition):  # Обновляем столбец
        set_values = ', '.join([f"{column} = ?" for column in data.keys()])
        query = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
        self.cur.execute(query, list(data.values()))
        self.con.commit()

    def delete_data(self, table_name, condition):  # Удаляем из таблицы
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cur.execute(query)
        self.con.commit()

    def close(self):  # Закрываем базу данных
        self.con.close()


#
# class User:
#    date = datetime.now().date()
#
#    def __init__(self, db):
#        self.db = db
#
#    def user_exists(self, telegram_id):
#        condition = f"telegram_id = {telegram_id}"
#        rows = self.db.select_data("user", condition)
#        return len(rows) > 0
#
#    def add_user(self, username, telegram_id, phone_number, email):
#        # if  self.user_exists(telegram_id):
#        # raise ValueError("Пользователь с таким telegram_id уже существует")
#
#        data = (None, username, telegram_id, phone_number, email, self.date)  # None для автоинкрементного столбца id
#        self.db.insert_data("user", data)
#
#    def update_user(self, data, condition):
#        db.update_data(table_name='user', data=data, condition=condition)
#
#    def get_users(self):
#        rows = self.db.select_data("user")
#        return rows
#
#
# class Products:
#    def __init__(self, db):
#        self.db = db
#
#    def product_exists(self, product_id: int):
#        condition = f"ProductsID = '{product_id}'"  # Исправленное условие
#        rows = self.db.select_data("Products", condition)
#        return len(rows) > 0
#
#    def add_product(self, product, category, description, price, quantity, media: str):
#        if self.product_exists(product):
#            return
#        else:
#            data = (
#                None, product, category, description, price, quantity, media)  # None для автоинкрементного столбца id
#            self.db.insert_data(table_name='Products',data=data)
#            return
#
#    def get_products(self, category=None):  # Condition - это условие , если стоит True , то выполняем запрос с условием
#        if category:
#            rows = self.db.select_data(table_name='Products', condition=f"CategoryID = '{category}'")
#            return rows
#        else:
#            rows = self.db.select_data(table_name='Products')
#            return rows
#
#    def get_categories(self):  # Выводим категории
#        query = db.cur.execute(f"SELECT C FROM product")
#        query = query.fetchall()
#        return query
#
#
# class Cart:
#    def __init__(self, db):
#        self.db = db
#
#    def cart_exists(self, product_id):
#        condition = f"ProductID = '{product_id}'"
#        rows = self.db.select_data("Cart", condition)
#        return len(rows) > 0
#
#    def add_to_cart(self, telegram_id: int, username: str, product_id: int, product: str, price: int, quantity: int):
#        if self.cart_exists(product_id) == False:
#            full_price = quantity * price
#            db.insert_data(table_name='Cart',
#                           data=(None, telegram_id, username, product_id, product, quantity, full_price))
#        else:
#            return False
#
#    def get_cart_items(self, telegram_id):
#        condition = f"TelegramID = {telegram_id}"
#        rows = self.db.select_data("Cart", condition)
#        for i in rows:
#            return rows


db = DataBase('database.db')  # Подключаемся к базе данных
# db.create_table(table_name="Users",  # Создаем таблицы, если их не существует
#               columns=["id INTEGER PRIMARY KEY AUTOINCREMENT",
#                         "UserName TEXT NOT NULL",
#                         "TelegramID INTEGER NOT NULL",
#                         "Phone INTEGER ",
#                         "Email TEXT NOT NULL", "reg_date TEXT NOT NULL"])


db.create_table(table_name='Categories', columns=["CategoryID INTEGER PRIMARY KEY ,"
                                                  "CategoryName TEXT NOT NULL"])

db.create_table(table_name="Products",
                columns=["ProductID INTEGER PRIMARY KEY AUTOINCREMENT",
                         "ProductName TEXT NOT NULL",
                         "CategoryID INTEGER NOT NULL",
                         "Description TEXT",
                         "Price INTEGER NOT NULL",
                         "Quantity INTEGER NOT NULL",
                         "Image BLOB NOT NULL",
                         "FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)"])

db.create_table(table_name="Cart",
                columns=["id INTEGER PRIMARY KEY AUTOINCREMENT",
                         "TelegramID INTEGER NOT NULL",
                         "ProductID INTEGER NOT NULL",
                         "Quantity INTEGER NOT NULL",
                         "CategoryID INTEGER NOT NULL ",
                         "FullPrice INTEGER NOT NULL",
                         "FOREIGN KEY (ProductID) REFERENCES Products(ProductID)"])
