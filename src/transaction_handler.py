import datetime
from env import STRIPE_SK
import stripe


stripe.api_key = STRIPE_SK


class TransactionHandler:

    def __init__(self, transaction_session_id: str) -> None:
        self._transaction_session_id = transaction_session_id
        self._checkout_session_data = None
        self._MAX_DURATION_DIFF = 300
        self._uid = None
        self._amount_total = None

    def _retrieve_checkout_session(self) -> None:
        self._checkout_session_data = stripe.checkout.Session.retrieve(self._transaction_session_id)

    def _validate_checkout_session(self) -> bool:
        payment_status = self._checkout_session_data.get('payment_status', None)
        self._uid = self._checkout_session_data.get('client_reference_id', None)
        self._amount_total = self._checkout_session_data.get('amount_total', None)
        if self._uid is not None and self._amount_total is not None and payment_status == "paid":
            curr_unix_time = datetime.datetime.now().timestamp()
            expires_at_unix_time = self._checkout_session_data.get('expires_at', None)
            if expires_at_unix_time is not None:
                return curr_unix_time - expires_at_unix_time < self._MAX_DURATION_DIFF
        return False
          
    def process(self, transaction_accumulator) -> bool:
        self._retrieve_checkout_session()
        transaction_accumulator.add_top_up_task(self._uid, self._amount_total)
        