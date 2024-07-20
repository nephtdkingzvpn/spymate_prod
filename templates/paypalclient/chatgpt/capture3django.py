from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
import json
from django.conf import settings

# Initialize PayPal SDK environment
environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID,
                                 client_secret=settings.PAYPAL_CLIENT_SECRET)
client = PayPalHttpClient(environment)

@csrf_exempt
def capture_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('orderID')

        # Capture the payment using PayPal Python SDK
        request = OrdersCaptureRequest(order_id)
        response = client.execute(request)

        # Handle response from PayPal
        if response.result.status == 'COMPLETED':
            # Payment captured successfully
            payer_name = response.result.payer.name.given_name
            return JsonResponse({'status': 'success', 'payerName': payer_name})
        else:
            # Payment capture failed
            return JsonResponse({'status': 'error', 'message': 'Failed to capture payment.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
