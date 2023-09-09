import datetime


class TransactionTask:

    def __init__(self, sender_uid: int, recipient_uid: int, 
                 amount: float, date: datetime.datetime) -> None:
        self._sender_uid = sender_uid
        self._recipient_uid = recipient_uid
        if (amount <= 0):
            print("Insufficient balance")
        else:
            self._amount = amount
        self._date = date
        self._sender_update_success = False
        self._recipient_update_success = False
        self._transaction_history_update_success = False

    def __repr__(self) -> str:
        return f"TransactionTask(sender_uid={self._sender_uid}, recipient_uid={self._recipient_uid}, amount={self._amount}, date={self._date})"

    def get_sender_uid(self) -> int:
        return self._sender_uid

    def get_recipient_uid(self) -> int:
        return self._recipient_uid

    def get_amount(self) -> float:
        return self._amount

    def get_date(self) -> str:
        return self._date
    
    def get_sender_update_success(self) -> bool:
        return self._sender_update_success
    
    def get_recipient_update_success(self) -> bool:
        return self._recipient_update_success
    
    def get_transaction_history_update_success(self) -> bool:
        return self._transaction_history_update_success

    def set_sender_uid(self, sender_uid: int) -> None:
        self._sender_uid = sender_uid

    def set_recipient_uid(self, recipient_uid: int) -> None:
        self._recipient_uid = recipient_uid

    def set_amount(self, amount: float) -> None:
        self._amount = amount

    def set_date(self, date: str) -> None:
        self._date = date

    def set_sender_update_success(self, sender_update_success: bool) -> None:
        self._sender_update_success = sender_update_success

    def set_recipient_update_success(self, recipient_update_success: bool) -> None:
        self._recipient_update_success = recipient_update_success

    def set_transaction_history_update_success(self, transaction_history_update_success: bool) -> None:
        self._transaction_history_update_success = transaction_history_update_success
        
    def to_row(self):
        return (self._sender_uid, self._recipient_uid, self._amount, self._date)
