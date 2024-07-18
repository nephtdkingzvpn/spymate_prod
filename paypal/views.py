from django.shortcuts import render
from django.urls import reverse


def make_paypal_payment(request):
    if request.method == 'POST':
        name = request.POST.get('full_name', None)
        email = request.POST.get('email', None)
        phone_number = request.POST.get('phone_number', None)
        return_url = request.build_absolute_uri(reverse('paypal:payment_return'))
        cancel_url = request.build_absolute_uri(reverse('paypal:payment_cancel'))

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
                                "sku": "",
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

        print(payment_data)

    return render(request, 'paypal/payment.html')


def payment_return(request):
    # Handle the return from PayPal
    return render(request, 'payment_return.html')


def payment_cancel(request):
    # Handle the cancel from PayPal
    return render(request, 'payment_cancel.html')
