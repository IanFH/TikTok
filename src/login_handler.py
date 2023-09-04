from database_handler import DatabaseHandler
from user import User


class LoginHandler:

    def __init__(self, raw_username: str, raw_password: str):
        self._raw_username = raw_username
        self._raw_password = raw_password

    def login(self, db_hanlder: DatabaseHandler):
        user_data = db_hanlder.fetch_user_data(self._raw_username)
        user = User.from_tuple(user_data)
        curr_hashed_password_one = self._hash_password_one()
        curr_hashed_password_two = self._hash_password_two()
        hashed_password_one = user.get_password_hashed_one()
        hashed_password_two = user.get_password_hashed_two()
        if (curr_hashed_password_one == hashed_password_one) and (curr_hashed_password_two == hashed_password_two):
            return 
        return None
    
    def _hash_password_one(self):
        # TODO: Implement hashing algorithm (Joseph)
        return 0

    def _hash_password_two(self):
        # TODO: Implement hashing algorithm (Joseph)
        return 1