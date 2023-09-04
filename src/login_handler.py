from database_handler import DatabaseHandler
from user import User


class LoginHandler:

    def __init__(self, raw_username: str, raw_password: str):
        self._raw_username = raw_username
        self._raw_password = raw_password

    def login(self, db_hanlder: DatabaseHandler):
        user_data = db_hanlder.fetch_user_data(self._raw_username)
        uid = user_data[0]
        hashed_password = self._hash_password()
        hashed_password_one = db_hanlder.fetch_password_one(uid)
        hashed_password_two = db_hanlder.fetch_password_two(uid)
        if (hashed_password == hashed_password_one) and (hashed_password == hashed_password_two):
            return User(uid, self._raw_username)
        return None
    
    def _hash_password(self):
        pass