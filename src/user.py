from database_handler import DatabaseHandler
import datetime
import psycopg
from hash import hash


class User:

    def __init__(self, uid: int, 
                 username: str, username_hashed: int = None, 
                 password_hashed_one: int = None, password_hashed_two: int = None,
                 balance: float = 0, ic_no: str = None,
                 registration_timestamp: datetime.datetime = None,
                 activation_timestamp: datetime.datetime = None,
                 phone_number: int = None):
        self._uid = uid
        self._username = username
        self._username_hashed = username_hashed
        self._password_hashed_one = password_hashed_one
        self._password_hashed_two = password_hashed_two
        self._balance = balance
        self._contacts = None
        self._favourite_contacts = None
        self._ic_no = ic_no
        self._registration_timestamp = registration_timestamp
        self._activation_timestamp = activation_timestamp
        self._phone_number = phone_number

    def __repr__(self):
        return f"User(uid={self._uid}, ic_no:{self._ic_no}, phone_number: {self._phone_number}, balance: {self._balance})" 

    def set_uid(self, uid: int):
        self._uid = uid

    def set_username(self, username: str):
        self._username = username

    def set_username_hashed(self, username_hashed: int):
        self._username_hashed = username_hashed

    def set_password_hashed_one(self, password_hashed_one: int):
        self._password_hashed_one = password_hashed_one

    def set_password_hashed_two(self, password_hashed_two: int):
        self._password_hashed_two = password_hashed_two

    def set_balance(self, balance: float):
        self._balance = balance

    def set_contacts(self, contacts: list[str]):
        self._contacts = contacts

    def set_favourite_contacts(self, favourite_contacts: list[str]):
        self._favourite_contacts = favourite_contacts

    def set_ic_no(self, ic_no: str):
        self._ic_no = ic_no

    def set_registration_timestamp(self, registration_timestamp: datetime.datetime):
        self._registration_timestamp = registration_timestamp

    def set_activation_timestamp(self, activation_timestamp: datetime.datetime):
        self._activation_timestamp = activation_timestamp

    def set_phone_number(self, phone_number: int):
        self._phone_number = phone_number

    def get_uid(self):
        return self._uid
    
    def get_username(self):
        return self._username
    
    def get_username_hashed(self):
        return self._username_hashed
    
    def get_password_hashed_one(self):
        return self._password_hashed_one
    
    def get_password_hashed_two(self):
        return self._password_hashed_two

    def get_balance(self):
        return self._balance
    
    def get_contacts(self):
        return self._contacts
    
    def get_favourite_contacts(self):
        return self._favourite_contacts
    
    def get_ic_no(self):
        return self._ic_no
    
    def get_registration_timestamp(self):
        return self._registration_timestamp
    
    def get_activation_timestamp(self):
        return self._activation_timestamp
    
    def get_phone_number(self):
        return self._phone_number
    
    @staticmethod
    def from_tuple(user_tuple: tuple[int, str, int, int, int, float]):
        uid = user_tuple[0]
        username = user_tuple[1]
        username_hashed = user_tuple[2]
        password_hashed_one = user_tuple[3]
        password_hashed_two = user_tuple[4]
        balance = user_tuple[5]
        return User(uid, username, username_hashed, 
                    password_hashed_one, password_hashed_two, balance)

    def insert_to_database(self, db_handler: DatabaseHandler):
        result = db_handler.fetch_user_data(self._username, self._username_hashed)
        if result:
            return False
        else:
            curr_timestamp = datetime.datetime.now()
            print("INSERTING...")
            # (uid, username, username_hashed, password_hashed_one, password_hashed_two, phone_no, 
            #  balance, registration_timestamp, activation_timestamp, ic_no)
            db_handler.insert_user(self._username, self._username_hashed, 
                                   self._password_hashed_one, self._password_hashed_two, 
                                   self._phone_number, self._balance, curr_timestamp, None,
                                   self._ic_no)
            print("INSERTED")
            return True
        
    def activate(self, db_handler: DatabaseHandler):
        curr_timestamp = datetime.datetime.now()
        try:
            db_handler.bulk_activate_user(self._uid, curr_timestamp)
            return
        except psycopg.errors.Error:
            return False
        
    def get_transaction_history(self, 
                                db_handler: DatabaseHandler, 
                                start_date: datetime.datetime, 
                                end_date: datetime.datetime):
        return db_handler.fetch_transactions(self._uid, start_date, end_date)
    
    @staticmethod
    def hash_password_two(password: str):
        n = len(password)
        salted_password = password[0:n//4] + "$" + password[n//4:n//2] + "$" + password[n//2: n * 3 // 4] + "$" + password[n * 3 // 4:]
        return abs(hash(salted_password)) % (2 ** 31 - 1)
    
    @staticmethod
    def hash_password_one(password: str):
        return abs(hash(password)) % (2 ** 31 - 1)

    @staticmethod 
    def hash_username(username: str):
        return abs(hash(username)) % (2 ** 31 - 1)

    @staticmethod
    def username_exists(db_handler: DatabaseHandler, username: str):
        result = db_handler.fetch_user_data(username, User.hash_username(username))
        return result is not None
    
    @staticmethod
    def create_user(username: str, password: str, phone_number: int, ic_no: str):
        username_hashed = User.hash_username(username)
        password_hashed_one = User.hash_password_one(password)
        password_hashed_two = User.hash_password_two(password)
        return User(None, username, username_hashed, password_hashed_one, 
                    password_hashed_two, balance=0, 
                    phone_number=phone_number, ic_no=ic_no)
        
    def serialise(self):
        return {
            'uid': self._uid,
            'username': self._username,
            'username_hashed': self._username_hashed,
            'password_hashed_one': self._password_hashed_one,
            'password_hashed_two': self._password_hashed_two,
            'balance': self._balance
        }
    
    @staticmethod
    def deserialise(serialised_user: dict):
        uid = serialised_user['uid']
        username = serialised_user['username']
        username_hashed = serialised_user['username_hashed']
        password_hashed_one = serialised_user['password_hashed_one']
        password_hashed_two = serialised_user['password_hashed_two']
        balance = serialised_user['balance']
        return User(uid, username, username_hashed, 
                    password_hashed_one, password_hashed_two, balance)
    
