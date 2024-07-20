from django.shortcuts import render
from django.conf import settings


def paypal_client_payment(request):

    client_id = settings.PAYPAL_CLIENT_ID

    context = {'client_id':client_id}
    return render(request, 'paypalclient/payment_client.html', context)
