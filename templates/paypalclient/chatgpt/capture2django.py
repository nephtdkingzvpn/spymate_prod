# views.py

from django.http import JsonResponse
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def capture_payment(request):
    if request.method == 'POST':
        # Initialize PayPal environment
        environment = SandboxEnvironment(client_id='YOUR_PAYPAL_SANDBOX_CLIENT_ID', client_secret='YOUR_PAYPAL_SANDBOX_CLIENT_SECRET')
        client = PayPalHttpClient(environment)

        # Capture PayPal payment
        order_id = request.POST.get('orderID')
        request = OrdersCaptureRequest(order_id)
        
        try:
            response = client.execute(request)
            # Handle successful payment capture
            return JsonResponse({'status': 'success', 'message': 'Payment captured successfully.'})
        except Exception as e:
            # Handle capture failure
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
