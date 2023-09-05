import psycopg
from env import DB_USER, DB_PASS, DB_HOST, DB_PORT


class DatabaseHandler:

    def __init__(self):
        self.connection = self._get_connection()
        self.cursor = self.connection.cursor()

    def _get_connection(self):
        return psycopg.connect(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
    
    def insert_user(self, username: str, username_hashed: int, 
                    password_hashed_one: int, password_hashed_two: int):
        """
        Inserts a user into the database
        """
        # TODO: Implement SQL query (Jeff)
        sql_query = ''
        self.cursor.execute(sql_query, (username, username_hashed, password_hashed_one, password_hashed_two))
        self.connection.commit()

    
    def fetch_user_data(self, username: str, username_hashed: int):
        """
        Fetches the data of a user from the database (exluding contacts and favourite contacts)
        """
        # TODO: Implement SQL query (Jeff)
        sql_query = ''
        self.cursor.execute(sql_query, (username_hashed, ))
        results = self.cursor.fetchall()
        # assuming that the username is in position 1
        for result in results:
            if result[1] == username:
                return result
        return None
        

    def delete(self, uid: int):
        """
        Deletes a user from the database based on uid
        """
        # TODO: Implement SQL query (Jeff)
        sql_query = ''
        self.cursor.execute(sql_query, (uid, ))
        self.connection.commit()

    def update_password(self, uid: int, password_hashed_one: int, password_hashed_two: int):
        """
        Updates the password of a user in the database based on uid
        """
        # TODO: Implement SQL query (Jeff)
        sql_query = ''
        self.cursor.execute(sql_query, (uid, password_hashed_one, password_hashed_two))
        self.connection.commit()

    def update_balance(self, uid: int, balance: float):
        """
        Updates the balance of a user in the database based on uid
        """
        # TODO: Implement SQL query (Jeff)
        sql_query = ''
        self.cursor.execute(sql_query, (uid, balance))
        self.connection.commit()

    def add_transaction(self, sender_uid: int, receiver_uid: int, amount: float, date: str):
        """
        Adds a transaction to the database
        """
        # TODO: Implement SQL query (Jeff)
        sql_query = ''
        self.cursor.execute(sql_query, (sender_uid, receiver_uid, amount, date))
        self.connection.commit()

    def fetch_transactions(self, uid: int, start_date: str, end_date: str):
        """
        Fetches the transactions of a user from the database
        """
        # TODO: Implement SQL query (Jeff)
        sql_query = ''
        self.cursor.execute(sql_query, (uid, start_date, end_date))
        self.connection.commit()

    def __del__(self):
        self.connection.close()


# SAMPLE
# In this function, the table name is 'users'
# def insert_user(self, username, password):
#    self.cursor.execute('INSERT INTO users VALUES (NULL, ?, ?)', (username, password))
#    self.connection.commit()
#