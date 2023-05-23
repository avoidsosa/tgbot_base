import sqlite3

class Database:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                               (id INTEGER PRIMARY KEY, name TEXT, uname TEXT, date TEXT, balance INTEGER)''')
        self.connection.commit()

    def add_user(self, id, username, user_name, date):
        self.cursor.execute("INSERT OR IGNORE INTO users (id, name, uname, date) VALUES (?, ?, ?, ?)",
                            (id, username, user_name, date))
        self.connection.commit()
        return True

    def user_exist(self, id):
        self.cursor.execute("SELECT id FROM users WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        return result is not None

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT id FROM users").fetchall()

    def get_table(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM users').fetchall()

    def get_user_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM users')
        result = self.cursor.fetchone()[0]
        return result

    def get_user(self, user_id):
        with self.connection:
            # Получаем информацию о пользователе с заданным user_id из таблицы "users"
            return self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

    def create_banned_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS banned_users
                                          (id INTEGER PRIMARY KEY, name TEXT, uname TEXT, date TEXT, balance INTEGER)''')
        self.connection.commit()

    def ban_user(self, user_id):
        # Получаем информацию о пользователе из базы данных
        user = self.get_user(user_id)

        # Добавляем информацию о забаненном пользователе в новую таблицу "banned_users"
        self.cursor.execute('INSERT INTO banned_users (id, name, uname, date, balance) VALUES (?, ?, ?, ?)', user)
        self.connection.commit()

        # Удаляем информацию о пользователе из таблицы "users"
        self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.connection.commit()

    def get_banned(self):
        with self.connection:
            # Создаем таблицу "banned_users", если она еще не существует
            self.create_banned_table()

            # Получаем список забаненных пользователей из таблицы "banned_users"
            return self.cursor.execute('SELECT * FROM banned_users').fetchall()

    def get_banned_user(self, user_id):
        with self.connection:
            # Получаем информацию о пользователе с заданным user_id из таблицы "users"
            return self.cursor.execute('SELECT * FROM banned_users WHERE id = ?', (user_id,)).fetchone()

    def unban_user(self, user_id):
        # Получаем информацию о пользователе из базы данных
        user = self.get_banned_user(user_id)

        self.cursor.execute('INSERT INTO users (id, name, uname, date, balance) VALUES (?, ?, ?, ?)', user)
        self.connection.commit()

        self.cursor.execute('DELETE FROM banned_users WHERE id = ?', (user_id,))
        self.connection.commit()

    def get_banned_id(self, user_id):
        with self.connection:
            # Получаем информацию о пользователе с заданным user_id из таблицы "banned_users"
            result = self.cursor.execute('SELECT * FROM banned_users WHERE id = ?', (user_id,)).fetchone()
            # Если пользователь находится в таблице забаненных, то возвращаем его user_id, иначе возвращаем None
            return result[0] if result else None

    def is_banned_empty(self):
        with self.connection:
            result = self.cursor.execute("SELECT COUNT(*) FROM banned_users").fetchone()
            return result[0] == 0

    def add_balance(self, user_id, amount):
        self.cursor.execute('''UPDATE users SET balance = balance + ? WHERE id = ?''', (amount, user_id))
        self.connection.commit()

    #def create_table_trades(self):
        #self.cursor.execute('')
        #self.connection.commit()
