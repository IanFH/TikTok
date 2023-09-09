from database_handler import DatabaseHandler
from user import User


class LoginHandler:

    def __init__(self, raw_username: str, raw_password: str):
        self._raw_username = raw_username
        self._raw_password = raw_password

    def login(self, db_hanlder: DatabaseHandler):
        user_data = db_hanlder.fetch_user_data(self._raw_username, User.hash_username(self._raw_username))
        user = User.from_tuple(user_data)
        print(user)
        curr_hashed_password_one = self._hash_password_one()
        curr_hashed_password_two = self._hash_password_two()
        hashed_password_one = user.get_password_hashed_one()
        hashed_password_two = user.get_password_hashed_two()
        if (curr_hashed_password_one == hashed_password_one) and (curr_hashed_password_two == hashed_password_two):
            return user 
        return None
    
    def _hash_password_one(self):
        return User.hash_password_one(self._raw_password)

    def _hash_password_two(self):
        return User.hash_password_two(self._raw_password)