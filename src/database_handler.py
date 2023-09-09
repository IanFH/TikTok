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
                    password_hashed_one: int, password_hashed_two: int):
        """

        """
        # TODO: Implement SQL query (Jeff)
        sql_query = """
                    INSERT INTO User_Table(uid, username, username_hashed, password_hashed_one, password_hashed_two, phone_no, balance, registration_timestamp, activation_timestamp, ic_no)
                    VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
        self.cursor.execute(sql_query, (username, username_hashed, password_hashed_one, password_hashed_two))
        self.connection.commit()

    
    def fetch_user_data(self, username: str, username_hashed: int):
        """

        """
        # TODO: Implement SQL query (Jeff)
        sql_query = """
                    SELECT uid, username, username_hashed)
                    FROM User_Table;
                    """
        self.cursor.execute(sql_query, (username_hashed, ))
        results = self.cursor.fetchall()
        # assuming that the username is in position 1
        for result in results:
            if result[1] == username:
                return result
        return None
        

    def delete(self, uid: int):
        """

        """
        # TODO: Implement SQL query (Jeff)
        sql_query = """
                    DELETE FROM User_Table
                    WHERE uid = %s;
                    """
        self.cursor.execute(sql_query, (uid, ))
        self.connection.commit()

    def update_password(self, uid: int, password_hashed_one: int, password_hashed_two: int):
        """

        """
        # TODO: Implement SQL query (Jeff)
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
        # TODO: Implement SQL query (Jeff)
        sql_query = """
                    UPDATE User_Table
                    SET balance = balance + %s
                    WHERE uid = %s
                    """
        self.cursor.execute(sql_query, (tran_amt, uid))
        self.connection.commit()

    def bulk_update_balance(self, entries: list[int, float]):
        """
        Updates the balance of multiple users in the database based on uid
        """
         # TODO: modify table name if necessary (Jeff)
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
        # TODO: Implement SQL query (Jeff)
        sql_query = """
                    INSERT INTO Transaction_Table(tran_id, tran_amt, recepient_id, sender_id, tran_timestamp)
                    VALUES (NULL, %s, %s, %s, %s); 
                    """
        self.cursor.execute(sql_query, (sender_uid, receiver_uid, amount, date))
        self.connection.commit()
    
    def bulk_insert_transactions(self, entries: list[int, int, float, datetime.datetime]):
        """
        Adds multiple transactions to the database
        """
        # TODO: modify table name if necessary (Jeff)
        sql_query = """
                    INSERT INTO Transaction_Table VALUES (%s, %s, %s, %s)
                    """
        self.cursor.executemany(sql_query, entries)
        self.connection.commit()

    def fetch_transactions(self, uid: int, start_date: datetime.datetime, end_date: datetime.datetime):
        """
        Fetches the transactions of a user from the database
        Each transaction is a tuple of (sender_uid, receiver_uid, amount, date)
        """
        # TODO: Implement SQL query (Jeff)
        sql_query = """
                    SELECT tran_id, tran_amt, recepient_id, sender_id, tran_timestamp
                    FROM Transaction_Table
                    WHERE uid = %s AND tran_timestamp >= %s AND tran_timestamp <= %s;
                    """
        self.cursor.execute(sql_query, (uid, start_date, end_date))
        results = self.cursor.fetchall()
        return results

    def rollback(self):
        """
        Rolls back the database to the last commit
        """
        self.connection.rollback()

    def list_tables(self):
        # TODO: Remove in production
        query = """
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE (table_schema = 'public')
                ORDER BY table_name;
                """
        self.cursor.execute(query)
        self.connection.commit()
        result = self.cursor.fetchall()
        return result


    def list_fields(self, name):
        # TODO: Remove in production
        """
        returns a python list of field names
        """
        query = """ 
                SELECT column_name FROM
                INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = %s;
                """
        self.cursor.execute(query, (name, ))
        result = self.cursor.fetchall()
        fields = [field[0] for field in result]
        return fields


    def list_schema(self):
        table_names = self.list_tables()
        with open("DB_SCHEMA.txt", "w") as f:
            for el in table_names:
                if el[1] != 'pg_stat_statements':
                    query = f""" SELECT * FROM "{el[1]}" ; """
                    self.cursor.execute(query)
                    result = self.cursor.fetchall()
                    f.write(f"===TABLE: {el[1]}===\n")
                    f.write(f"Columns: {self.list_fields(el[1])}\n")
                    for r in result:
                        f.write(f"{r}\n")

    def __del__(self):
        self.connection.close()


# SAMPLE
# In this function, the table name is 'users'
# def insert_user(self, username, password):
#    self.cursor.execute('INSERT INTO users VALUES (NULL, %s, %s)', (username, password))
#    self.connection.commit()
#

if __name__ == "__main__":
    # For testing of queries and execution of one off queries
    db_handler = DatabaseHandler()
    # sql_query = """

    #             """
    # db_handler.cursor.execute(sql_query)
    # db_handler.connection.commit()

    # To see what is in the db
    db_handler.list_schema()
