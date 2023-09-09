import datetime
from user_credentials import UserCredentials


class OfficialRecord:
    def __init__(self, birth_date: datetime, identification_num: int, address: str):
        self.birth_date = birth_date
        self.identification_num = identification_num
        self.address = address

    def get_birth_date(self):
        return self.birth_date

    def get_identification_num(self):
        return self.identification_num

    def get_address(self):
        return self.address

    def _equals(self, user_cred: UserCredentials):

        return self.name.lower() == user_cred.get_ic_number().lower() and \
            self.birth_date == user_cred.get_birth_date() and \
            self.identification_num == user_cred.get_identification_num() and \
            self.address.lower() == user_cred.get_address().lower()

# self.birthday == user_cred._get_birthday() and \
