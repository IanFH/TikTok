from src.database_handler import DatabaseHandler


class User:

    def __init__(self, uid: int, 
                 username: str, username_hashed: int = None, 
                 password_hashed_one: int = None, password_hashed_two: int = None,
                 balance: float = None):
        self._uid = uid
        self._username = username
        self._username_hashed = username_hashed
        self._password_hashed_one = password_hashed_one
        self._password_hashed_two = password_hashed_two
        self._balance = balance
        self._contacts = None
        self._favouite_contacts = None

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
        self.favourite_contacts = favourite_contacts

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
        return self.favourite_contacts
    
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
            db_handler.insert_user(self._username, self._username_hashed, 
                                   self._password_hashed_one, self._password_hashed_two)
            return True