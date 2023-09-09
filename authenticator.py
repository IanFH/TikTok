import datetime
from valid_record import OfficialRecord
from user_credentials import UserCredentials
from database_handler import DatabaseHandler
import datetime


class Authenticator:

    def __init__(self):
        self.AGE_LIMIT = 18
        self.VALID_LOCATIONS = ["Singapore"]
        self.user_creds = {}

    def _check_age_validity(self, official_record: OfficialRecord):
        return (datetime.datetime.now().year - official_record.get_birth_date().year) >= self.AGE_LIMIT

    def _check_location_validity(self, official_record: OfficialRecord):
        for loc in self.VALID_LOCATIONS:
            if loc.lower() in official_record.get_address().lower():
                return True
        return False
    
    def add_user_credentials(self, user_cred: UserCredentials):
        self.user_creds[user_cred.get_ic_number()] = user_cred

    def authenticate_credentials(self, db_handler: DatabaseHandler):
        ic_numbers = list(self.user_creds.keys())
        ic_numbers = [(ic_number, ) for ic_number in ic_numbers]
        to_activate = []
        for ic_number in self.user_creds:
            official_record = db_handler.fetch_creds(ic_number)
            if len(official_record) > 0:
                official_record = OfficialRecord(official_record[1], official_record[0], official_record[2])
                if official_record is not None:
                    if (self._check_age_validity(official_record) and 
                        self._check_location_validity(official_record)):
                        curr_date = datetime.datetime.now()
                        to_activate.append((curr_date, ic_number))
        db_handler.bulk_activate_user(to_activate)
