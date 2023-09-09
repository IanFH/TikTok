import datetime


class UserCredentials:
    def __init__(self, ic_number: str):
        self.ic_number = ic_number

    def get_ic_number(self):
        return self.ic_number
