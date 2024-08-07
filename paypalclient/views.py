from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from django.contrib.auth.models import User
import json

from .paypal import PayPalClient
from frontend.models import Payment
from frontend.send_email import send_html_email


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
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')

        # url success and failure
        success_url = request.build_absolute_uri(reverse('paypalclient:payment_success'))
        failure_url = request.build_absolute_uri(reverse('paypalclient:payment_failure'))

        # Capture the payment using PayPal Python SDK
        order_request = OrdersCaptureRequest(order_id)
        response = PPClient.client.execute(order_request)

        # Handle response from PayPal
        if response.result.status == 'COMPLETED':
            # create a new payment instance
            new_payment = Payment.objects.create(ref=order_id, name=name, email=email, phone=phone, is_success = True)

            # create user account
            password_one = new_payment.email.split("@")[0]
            password_two = new_payment.phone[2:8]
            d_ref = new_payment.ref[:13]
            main_password = f'{password_one}{password_two}@@'
            main_username = f"{password_one}-{d_ref}"

            new_user = User.objects.create_user(username=main_username, email=new_payment.email, password=main_password)

            # email contents
            subject = "Your lifetime access to spymate has been approved."
            html_template = 'emails/success_purchase_email.html'
            context = {
                'subject': subject,
                'name': new_payment.name,
                'username': main_username,
                'password': main_password
            }

            # sending email
            try:
                send_html_email(subject, html_template, context, new_payment.email)
            except:
                pass
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