import braintree
from django.conf import settings


class BraintreeService:
    def __init__(self):
        self.gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.Sandbox,
                merchant_id=settings.BRAINTREE_MERCHANT_ID,
                public_key=settings.BRAINTREE_PUBLIC_KEY,
                private_key=settings.BRAINTREE_PRIVATE_KEY
            )
        )

    def generate_client_token(self):
        return self.gateway.client_token.generate()
    
    def create_transaction(self, amount, nonce):
        return self.gateway.transaction.sale({
            "amount": amount,
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })


# environment = braintree.Environment.Sandbox
# merchant_id = settings.BRAINTREE_MERCHANT_ID
# public_key = settings.BRAINTREE_PUBLIC_KEY
# private_key = settings.BRAINTREE_PRIVATE_KEY