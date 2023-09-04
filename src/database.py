import sqlite3

class DatabaseHandler:

    def __init__(self):
        self.connection = self._get_connection()
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
        self.connection.commit()

    def _get_connection(self):
        return sqlite3.connect('database.db')
    
    
    def insert_user(self, username, password):
        self.cursor.execute('INSERT INTO users VALUES (NULL, ?, ?)', (username, password))
        self.connection.commit()

    def fetch_users(self):
        self.cursor.execute('SELECT * FROM users')
        rows = self.cursor.fetchall()
        return rows

    def fetch_user(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        rows = self.cursor.fetchall()
        return rows

    def delete_user(self, username):
        self.cursor.execute('DELETE FROM users WHERE username=?', (username,))
        self.connection.commit()

    def update_user(self, username, password):
        self.cursor.execute('UPDATE users SET password=? WHERE username=?', (password, username))
        self.connection.commit()

    def __del__(self):
        self.connection.close()


if __name__ == "__main__":
    db = DatabaseHandler()