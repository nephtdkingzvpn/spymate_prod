import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from .paypal_services import PayPalPaymentService, PayPalWebhookService
from django.http import JsonResponse, HttpResponseBadRequest

from frontend.payment_type import generate_tx_ref
from frontend.models import Payment
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


def make_paypal_payment(request):
    if request.method == 'POST':
        name = request.POST.get('full_name', None)
        email = request.POST.get('email', None)
        phone_number = request.POST.get('phone_number', None)
        return_url = request.build_absolute_uri(reverse('paypal:payment_return'))
        cancel_url = request.build_absolute_uri(reverse('paypal:payment_cancel'))

        new_payment = Payment.objects.create(ref=generate_tx_ref(), name=name, email=email, phone=phone_number)

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
    return render(request, 'paypal/payment.html')


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
