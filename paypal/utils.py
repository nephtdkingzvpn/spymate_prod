import paypalrestsdk
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def configure_paypal():
    try:
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,  # Or "live"
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })
        logger.info("PayPal SDK configured successfully.")
    except Exception as e:
        logger.error(f"Failed to configure PayPal SDK: {e}")
        raise
