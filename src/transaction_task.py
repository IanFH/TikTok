class TransactionTask:

    def __init__(self, sender_uid: int, recipient_uid: int, amount: float) -> None:
        self._sender_uid = sender_uid
        self._recipient_uid = recipient_uid
        self._amount = amount

    def get_sender_uid(self) -> int:
        return self._sender_uid
    
    def get_recipient_uid(self) -> int:
        return self._recipient_uid
    
    def get_amount(self) -> float:
        return self._amount
    
    def set_sender_uid(self, sender_uid: int) -> None:
        self._sender_uid = sender_uid

    def set_recipient_uid(self, recipient_uid: int) -> None:
        self._recipient_uid = recipient_uid

    def set_amount(self, amount: float) -> None:
        self._amount = amount

    