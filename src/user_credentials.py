import datetime


class UserCredentials:
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
