import psycopg
from env import DB_USER, DB_PASS, DB_HOST, DB_PORT
import datetime


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
                    password_hashed_one: int, password_hashed_two: int,
                    phone_number: int, balance: float,
                    registration_timestamp: datetime.datetime, activation_timestamp: datetime.datetime,
                    ic_no: str):
        """
        Insert a user into the database
        """

        sql_query = """
                    INSERT INTO User_Table(username, username_hashed, password_hashed_one, password_hashed_two, phone_no, balance, registration_timestamp, activation_timestamp, ic_no)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
        self.cursor.execute(sql_query, (username, username_hashed, password_hashed_one, password_hashed_two, 
                                        phone_number, balance, registration_timestamp, activation_timestamp, ic_no))
        self.connection.commit()

    def fetch_creds(self, ic_number: str):
        """
        name: str, birthday: datetime, identification_num: int, address: str
        """
        sql_query = """
                    SELECT ic_no, birthdate, address
                    FROM Credential_Table
                    WHERE ic_no = %s;
                    """
        self.cursor.execute(sql_query, (ic_number, ))
        results = self.cursor.fetchone()
        return results

    
    def fetch_user_data(self, username: str, username_hashed: int):
        """
        Fetches the user data from the database based on username
        """
        sql_query = """
                    SELECT uid, username, username_hashed, password_hashed_one, password_hashed_two, phone_no, balance, registration_timestamp, activation_timestamp, ic_no
                    FROM User_Table
                    WHERE username_hashed = %s;
                    """
        self.cursor.execute(sql_query, (username_hashed, ))
        results = self.cursor.fetchall()
        # assuming that the username is in position 1
        for result in results:
            if result[1] == username:
                return result
        return None
    
    def fetch_user_data_by_phone(self, phone_number: int):
        """
        Fetches the user data from the database based on username
        """
        sql_query = """
                    SELECT uid, username, username_hashed, password_hashed_one, password_hashed_two, phone_no, balance, registration_timestamp, activation_timestamp, ic_no
                    FROM User_Table
                    WHERE phone_no = %s;
                    """
        self.cursor.execute(sql_query, (phone_number, ))
        results = self.cursor.fetchone()
        return results
    
    def fetch_user_data_uid(self, uid: int):
        """
        Fetches the user data from the database based on username
        """
        sql_query = """
                    SELECT uid, username, username_hashed, password_hashed_one, password_hashed_two, phone_no, balance, registration_timestamp, activation_timestamp, ic_no
                    FROM User_Table
                    WHERE uid = %s;
                    """
        self.cursor.execute(sql_query, (uid, ))
        results = self.cursor.fetchone()
        return results

    def delete(self, uid: int):
        """
        Delete a user from the database by UID
        """
        sql_query = """
                    DELETE FROM User_Table
                    WHERE uid = %s;
                    """
        self.cursor.execute(sql_query, (uid, ))
        self.connection.commit()

    def update_password(self, uid: int, password_hashed_one: int, password_hashed_two: int):
        """
        Updates the password of a user in the database based on uid
        """
        sql_query = """        
                    UPDATE User_Table
                    SET password_hashed_one = %s, password_hashed_two = %s
                    WHERE uid = %s;
                    """
        self.cursor.execute(sql_query, (uid, password_hashed_one, password_hashed_two))
        self.connection.commit()

    def update_balance(self, uid: int, tran_amt: float):
        """
        Updates the balance of a user in the database based on uid
        """
        sql_query = """
                    UPDATE User_Table
                    SET balance = balance + %s
                    WHERE uid = %s
                    """
        self.cursor.execute(sql_query, (tran_amt, uid))
        self.connection.commit()

    def bulk_activate_user(self, entries: list[datetime.datetime, str]):
        """
        Bulk activate the users
        """
        sql_query = """        
                    UPDATE User_Table
                    SET activation_timestamp = %s
                    WHERE ic_no = %s;
                    """
        self.cursor.executemany(sql_query, entries)
        self.connection.commit()

    def bulk_update_balance(self, entries: list[int, float]):
        """
        Updates the balance of multiple users in the database based on uid
        """
        sql_query = """
                    UPDATE User_Table
                    SET balance = balance + %s
                    WHERE uid = %s
                    """
        self.cursor.executemany(sql_query, entries)
        self.connection.commit()

    def insert_transaction(self, sender_uid: int, receiver_uid: int, amount: float, date: datetime.datetime):
        """
        Adds a transaction to the database
        """
        sql_query = """
                    INSERT INTO Transaction_Table(sender_id, recepient_id, tran_amt, tran_timestamp)
                    VALUES (%s, %s, %s, %s); 
                    """
        self.cursor.execute(sql_query, (sender_uid, receiver_uid, amount, date))
        self.connection.commit()
    
    def bulk_insert_transactions(self, entries: list[int, int, float, datetime.datetime]):
        """
        Adds multiple transactions to the database
        """
        sql_query = """
                    INSERT INTO Transaction_Table(sender_id, recepient_id, tran_amt, tran_timestamp) VALUES (%s, %s, %s, %s)
                    """
        self.cursor.executemany(sql_query, entries)
        self.connection.commit()

    def fetch_transactions(self, uid: int, start_date: datetime.datetime, end_date: datetime.datetime):
        """
        Fetches the transactions of a user from the database
        Each transaction is a tuple of (sender_uid, receiver_uid, amount, date)
        """
        sql_query = """
                    SELECT tran_id, tran_amt, recepient_id, sender_id, tran_timestamp
                    FROM Transaction_Table
                    WHERE (sender_id = %s OR recepient_id = %s) AND tran_timestamp >= %s AND tran_timestamp <= %s;
                    """
        self.cursor.execute(sql_query, (uid, uid, start_date, end_date))
        results = self.cursor.fetchall()
        return results

    def rollback(self):
        """
        Rolls back the database to the last commit
        """
        self.connection.rollback()

    def __del__(self):
        self.connection.close()


# SAMPLE
# In this function, the table name is 'users'
# def insert_user(self, username, password):
#    self.cursor.execute('INSERT INTO users VALUES (NULL, %s, %s)', (username, password))
#    self.connection.commit()
#



    


