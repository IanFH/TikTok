import stripe
from env import STRIPE_SK


stripe.api_key = STRIPE_SK


class Merchant:

    def __init__(self, merchant_id: str) -> None:
        self._merchant_id = merchant_id

    def get_merchant_id(self) -> str:
        return self._merchant_id
    
    def create_account(self) -> str:
        """
        Returns URL to create a Stripe account for the merchant
        """
        account_id = stripe.Account.create(type="express")["id"]
        resp = stripe.AccountLink.create(
            account=account_id,
            refresh_url="https://example.com/reauth",
            return_url="https://example.com/return",
            type="account_onboarding",
        )
        return resp["url"]
    
