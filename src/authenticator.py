import datetime
from valid_record import ValidRecord
from user_credentials import UserCredentials


class Authenticator:

    def __init__(self, user_cred: UserCredentials, valid_rec: ValidRecord):
        self.user_cred = user_cred
        self.valid_rec = valid_rec
        self.AGE_LIMIT = 18

    def _check_age_validity(self):
        return (datetime.datetime.now().year - self.user_cred._get_birthday().year) >= self.AGE_LIMIT

    def _check_credentials_matching(self):
        return self.valid_rec._equals(self.user_cred)

    def _check_authentication(self):
        return self._check_credentials_matching() and self._check_age_validity()


if __name__ == "__main__":
    govt_rec = ValidRecord("baba yaga", datetime.datetime.strptime(
        "2002-01-25", "%Y-%m-%d"), 69420, "21 White house")
    user_cred = ValidRecord("baba yagA", datetime.datetime.strptime(
        "2002-01-25", "%Y-%m-%d"), 69420, "21 White HoUse")
    auth = Authenticator(user_cred, govt_rec)
    print(auth._check_authentication())
    print(auth._check_age_validity())
    print(auth._check_credentials_matching())
