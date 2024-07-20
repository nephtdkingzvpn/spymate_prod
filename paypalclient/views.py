from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from paypalcheckoutsdk.orders import OrdersCaptureRequest
import json

from .paypal import PayPalClient

def paypal_client_payment(request):

    client_id = settings.PAYPAL_CLIENT_ID

    context = {'client_id':client_id}
    return render(request, 'paypalclient/payment_client.html', context)


@csrf_exempt
def capture_payment(request):
    if request.method == 'POST':
        PPClient = PayPalClient()
        data = json.loads(request.body)
        order_id = data.get('orderID')
        
        # url success and failure
        success_url = request.build_absolute_uri(reverse('paypalclient:payment_success'))
        failure_url = request.build_absolute_uri(reverse('paypalclient:payment_failure'))

        # Capture the payment using PayPal Python SDK
        order_request = OrdersCaptureRequest(order_id)
        response = PPClient.client.execute(order_request)

        # Handle response from PayPal
        if response.result.status == 'COMPLETED':
            # Payment captured successfully
            payer_name = response.result.payer.name.given_name
            return JsonResponse({'status': 'success', 'payerName': payer_name,
                                'success_url':success_url})
        else:
            # Payment capture failed
            return JsonResponse({'status': 'error', 'message': 'Failed to capture payment.', 'failure_url':failure_url})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def payment_success(request):
    return render(request, 'paypalclient/payment_success.html')

def payment_failure(request):
    return render(request, 'paypalclient/payment_failure.html')