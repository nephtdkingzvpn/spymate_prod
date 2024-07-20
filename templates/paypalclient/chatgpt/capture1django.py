from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
import json
from django.conf import settings

@csrf_exempt
def capture_paypal_payment(request):
    # Set up PayPal SDK environment
    environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID,
                                     client_secret=settings.PAYPAL_CLIENT_SECRET)
    client = PayPalHttpClient(environment)

    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('orderID')

        # Capture the payment
        request = OrdersCaptureRequest(order_id)
        response = client.execute(request)

        # Handle response from PayPal
        if response.status_code == 201:
            # Payment captured successfully
            return JsonResponse({'status': 'success', 'message': 'Payment captured successfully.'})
        else:
            # Payment capture failed
            return JsonResponse({'status': 'error', 'message': 'Failed to capture payment.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
