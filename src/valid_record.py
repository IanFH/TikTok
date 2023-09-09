import datetime
from user_credentials import UserCredentials


class ValidRecord:
    def __init__(self, name: str, birthday: datetime, identification_num: int, address: str):
        self.name = name
        self.birthday = birthday
        self.identification_num = identification_num
        self.address = address

    def _get_name(self):
        return self.name

    def _get_birthday(self):
        return self.birthday

    def _get_identification_num(self):
        return self.identification_num

    def _get_address(self):
        return self.address

    def _equals(self, user_cred: UserCredentials):

        return self.name.lower() == user_cred._get_name().lower() and \
            self.birthday == user_cred._get_birthday() and \
            self.identification_num == user_cred._get_identification_num() and \
            self.address.lower() == user_cred._get_address().lower()

# self.birthday == user_cred._get_birthday() and \
