class TransactionHandler:

    def __init__(self, uid: int) -> None:
        self._uid = uid
        self._date = None

        
        
    @staticmethod
    def process(transaction_session_id: str) -> bool:
        return True