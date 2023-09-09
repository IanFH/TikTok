class TransactionTask:

    def __init__(self, sender_uid: int, recipient_uid: int, amount: float, date: str) -> None:
        self._sender_uid = sender_uid
        self._recipient_uid = recipient_uid
        if (amount <= 0):
            print("Insufficient balance")
        else:
            self._amount = amount
        self._date = date

    def get_sender_uid(self) -> int:
        return self._sender_uid

    def get_recipient_uid(self) -> int:
        return self._recipient_uid

    def get_amount(self) -> float:
        return self._amount

    def get_date(self) -> str:
        return self._date

    def set_sender_uid(self, sender_uid: int) -> None:
        self._sender_uid = sender_uid

    def set_recipient_uid(self, recipient_uid: int) -> None:
        self._recipient_uid = recipient_uid

    def set_amount(self, amount: float) -> None:
        self._amount = amount

    def set_date(self, date: str) -> None:
        self._date = date

    def to_row(self):
        return (self._sender_uid, self._recipient_uid, self._amount, self._date)
