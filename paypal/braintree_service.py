import braintree
from django.conf import settings

# class BraintreeService:
#     def __init__(self, environment, merchant_id, public_key, private_key):
#         self.environment = environment
#         self.merchant_id = merchant_id
#         self.public_key = public_key
#         self.private_key = private_key
#         self.configure_braintree()

#     def configure_braintree(self):
#         braintree.Configuration.configure(
#             self.environment,
#             merchant_id=self.merchant_id,
#             public_key=self.public_key,
#             private_key=self.private_key
#         )

#     def generate_client_token(self):
#         gateway = braintree.BraintreeGateway(
#             braintree.Configuration(
#                 self.environment,
#                 merchant_id=self.merchant_id,
#                 public_key=self.public_key,
#                 private_key=self.private_key
#             )
#         )
#         return gateway.client_token.generate()


class BraintreeService:
    def __init__(self):
        self.gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.Sandbox,
                merchant_id='nhqd9gds74k85ymn',
                public_key='q5yg3ybysr9r6z3f',
                private_key='ac9dee81a3287f16a61395171acf4a57'
            )
        )

    def generate_client_token(self):
        return self.gateway.client_token.generate()


# merchant_id=merchant_id,
# public_key=public_key,
# private_key=private_key