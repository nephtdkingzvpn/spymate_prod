import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from .paypal_services import PayPalPaymentService, PayPalWebhookService
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings

from frontend.payment_type import generate_tx_ref
from frontend.models import Payment
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


def make_paypal_payment(request):
    if request.method == 'POST':
        selected_payment = request.POST.get('paymentType', None)
        name = request.POST.get('full_name', None)
        email = request.POST.get('email', None)
        phone_number = request.POST.get('phone_number', None)
        return_url = request.build_absolute_uri(reverse('paypal:payment_return'))
        cancel_url = request.build_absolute_uri(reverse('paypal:payment_cancel'))

        new_payment = Payment.objects.create(ref=generate_tx_ref(), name=name, email=email, phone=phone_number)

        if selected_payment:
            if selected_payment == 'paypal':  
                # constructing a payment data
                payment_data = {
                    "intent": "sale",
                    "payer": {
                        "payment_method": "paypal"
                    },
                    "transactions": [
                        {
                            "amount": {
                                "total": "15.00",
                                "currency": "USD",
                            },
                            "item_list": {
                                "items": [
                                    {
                                        "name": name,
                                        "sku": str(new_payment.id),
                                        "price": "15.00",
                                        "currency": "USD",
                                        "quantity": 1
                                    }
                                ]
                            },
                            "description": "This is a one time payment for spymate purchase."
                        }
                    ],
                    "redirect_urls": {
                        "return_url": return_url,
                        "cancel_url": cancel_url
                    }
                }

                try:
                    paypal_payment_service = PayPalPaymentService()
                    payment = paypal_payment_service.create_payment(payment_data)
                    return redirect(payment)
                except Exception as e:
                    logger.error(f"Unhandled exception: {e}")
                    return JsonResponse({'status': 'failure', 'message': str(e)}, status=500)
            elif selected_payment == 'credit_card':
                return JsonResponse({'status': 'success', 'message': 'Proceed with credit card hosted fields', 'order_id': None})
        else:
            return HttpResponseBadRequest("You need to select a payment type")
    context = {'client_id':settings.PAYPAL_CLIENT_ID}
    return render(request, 'paypal/payment.html', context)


def payment_return(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if payment_id and payer_id:
        try:
            paypal_payment_service = PayPalPaymentService()
            payment = paypal_payment_service.execute_payment(payment_id, payer_id)
            
            if payment.success():
                payment_details = payment.to_dict()
                transactions = payment_details['transactions']
                item_list = transactions[0]['item_list']['items']

                # Store a single SKU value
                if item_list:
                    single_sku = item_list[0]['sku']

                    # get and update payment
                    payment = Payment.objects.get(id=int(single_sku))
                    payment.is_success = True
                    payment.save()

                    # create an account
                    password_one = payment.email.split("@")[0]
                    password_two = payment.phone[2:8]
                    d_ref = payment.ref.split("-")[1]
                    main_password = f'{password_one}{password_two}@@'
                    main_username = f"{password_one}-{d_ref}"

                    User.objects.create_user(username=main_username, email=payment.email, password=main_password)

                return redirect(reverse('paypal:payment_success'))
            else:
                logger.error(f"Payment execution error: {payment.error}")
                return redirect(reverse('paypal:payment_failure'))
        except Exception as e:
            logger.error(f"Unhandled exception: {e}")
            return redirect(reverse('paypal:payment_failure'))
    else:
        return redirect(reverse('paypal:payment_failure'))


def payment_cancel(request):
    # Handle the cancel from PayPal
    return render(request, 'paypal/payment_cancel.html')


def payment_success(request):
    return render(request, 'paypal/payment_success.html')

def payment_failure(request):
    return render(request, 'paypal/payment_failure.html')



import json
from django.http import JsonResponse
from django.views import View
from .braintree_service import BraintreeService
import braintree
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


class GenerateClientTokenView(View):
    def get(self, request):
        # Create an instance of BraintreeService with credentials
        braintree_service = BraintreeService()

        # Initialize client_token with a default value
        client_token = None

        # Generate client token using BraintreeService method
        try:
            client_token = braintree_service.generate_client_token()
            return JsonResponse({'clientToken': client_token})
        
        except braintree.exceptions.authorization_error.AuthorizationError as e:
            logger.error(f"Authorization error: {e}")
            return JsonResponse({'error': 'Authorization'}, status=500)

        except braintree.exceptions.authentication_error.AuthenticationError as e:
            
            # Handle authentication errors
            logger.error(f"Authentication error: {e}")
            return JsonResponse({'error': 'Authentication error'}, status=500)

        except braintree.exceptions.NotFoundError as e:
            # Handle specific errors
            logger.error(f"Not found error: {e}")
            return JsonResponse({'error': 'Not found error'}, status=500)

        except Exception as e:
            # Catch any unexpected exceptions
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({'error': 'Unexpected error'}, status=500)
    

@csrf_exempt  # This is needed if you are not using CSRF tokens for this endpoint
def execute_payment(request):
    if request.method == 'POST':
        try:
            # Extract payment method nonce from the request
            data = json.loads(request.body)
            payment_method_nonce = data.get('nonce')
            amount = "15.00"  

            # Initialize Braintree gateway
            braintree_service = BraintreeService()


            # Create a transaction
            result = braintree_service.create_transaction(amount, payment_method_nonce)

            if result.success:
                return JsonResponse({'status': 'success', 'transaction_id': result.transaction.id})
            else:
                return JsonResponse({'status': 'failure', 'message': result.message}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
