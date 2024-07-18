import json
import requests
import logging
from django.conf import settings
from paypalrestsdk import configure, Payment

logger = logging.getLogger(__name__)

class BasePayPalService:
    def __init__(self):
        self.configure_paypal_sdk()
        self.access_token = self.get_paypal_access_token()

    def configure_paypal_sdk(self):
        try:
            configure({
                "mode": settings.PAYPAL_MODE,
                "client_id": settings.PAYPAL_CLIENT_ID,
                "client_secret": settings.PAYPAL_CLIENT_SECRET
            })
            logger.info("PayPal SDK configured successfully.")
        except Exception as e:
            logger.error(f"Failed to configure PayPal SDK: {e}")
            raise

    def get_paypal_access_token(self):
        url = "https://api.sandbox.paypal.com/v1/oauth2/token" if settings.PAYPAL_MODE == "sandbox" else "https://api.paypal.com/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US"
        }
        data = {
            "grant_type": "client_credentials"
        }

        try:
            response = requests.post(url, headers=headers, data=data, auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET))
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to obtain PayPal access token: {e}")
            raise Exception("Could not obtain PayPal access token")
        

class PayPalPaymentService(BasePayPalService):
    def create_payment(self, payment_data):
        try:
            payment = Payment(payment_data)
            if payment.create():
                logger.info("Payment created successfully")
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = str(link.href)
                        return approval_url
                return payment
            else:
                logger.error(f"Payment creation failed: {payment.error}")
                raise Exception("Payment creation failed")
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            raise

    def execute_payment(self, payment_id, payer_id):
        try:
            payment = Payment.find(payment_id)
            if payment.execute({"payer_id": payer_id}):
                logger.info("Payment executed successfully")
                return payment
            else:
                logger.error(f"Payment execution failed: {payment.error}")
                raise Exception("Payment execution failed")
        except Exception as e:
            logger.error(f"Error executing payment: {e}")
            raise


class PayPalWebhookService(BasePayPalService):
    def verify_webhook(self, headers, body, webhook_id):
        transmission_id = headers.get('PAYPAL-TRANSMISSION-ID')
        transmission_time = headers.get('PAYPAL-TRANSMISSION-TIME')
        cert_url = headers.get('PAYPAL-CERT-URL')
        actual_sig = headers.get('PAYPAL-TRANSMISSION-SIG')
        auth_algo = headers.get('PAYPAL-AUTH-ALGO')

        try:
            response = requests.post(
                url='https://api.sandbox.paypal.com/v1/notifications/verify-webhook-signature' if settings.PAYPAL_MODE == "sandbox" else 'https://api.paypal.com/v1/notifications/verify-webhook-signature',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.access_token}'
                },
                json={
                    'transmission_id': transmission_id,
                    'transmission_time': transmission_time,
                    'cert_url': cert_url,
                    'auth_algo': auth_algo,
                    'transmission_sig': actual_sig,
                    'webhook_id': webhook_id,
                    'webhook_event': json.loads(body)
                }
            )

            response.raise_for_status()
            verification_status = response.json().get('verification_status')
            return verification_status == 'SUCCESS'
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to verify PayPal webhook: {e}")
            return False
