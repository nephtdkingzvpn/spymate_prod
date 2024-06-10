import json
import time
import math
import random
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User

from .payment_type import card_payment, verify_flutterwave_signature, generate_tx_ref
from .models import Payment

def home(request):
    return render(request, 'index.html')

def make_payment(request):
    if request.method == 'POST':
        selected_payment = request.POST.get('paymentType', None)
        name = request.POST.get('full_name', None)
        email = request.POST.get('email', None)
        phone_number = request.POST.get('phone_number', None)

        # redirect url
        url = request.build_absolute_uri(reverse('frontend:payment_processing'))
        ref = generate_tx_ref()
        # ref = ''+str(math.floor(10000000 + random.random()*90000000)),

        if selected_payment:
            if selected_payment == 'Card':              
                payment_response, error_message = card_payment(name,email,phone_number, url, ref)

                if payment_response:
                    payment_url = payment_response.get('data').get('link')

                    # create a new payment
                    new_payment = Payment.objects.create(ref=ref, name=name, email=email, phone=phone_number)
                    request.session['payment_id'] = new_payment.id
                    return redirect(payment_url)
                else:
                    # Payment request failed, handle the error
                    return JsonResponse({"error": error_message}, status=400)
            
            elif selected_payment == 'Bitcoin':
                print('bitcoin payment')
                return redirect('frontend:make_payment')
        else:
            return redirect('frontend:make_payment')
    return render(request, 'payment.html')


@csrf_exempt
def flutterwave_webhook(request):

    if request.method == 'POST':
        if verify_flutterwave_signature(request):

            # getting payload infromations
            payload = json.loads(request.body)
            data = payload.get('data')
            customer_data = payload.get('data', {}).get('customer', {})

            # getting customer details from payload informations
            customer_name = customer_data.get('name')
            customer_email = customer_data.get('email')
            customer_phone_number = customer_data.get('phone_number')

            # getting transaction details
            status = data.get('status')
            ref = data.get('tx_ref')

            # check if payment was successful
            if status == 'successful':
                payment = Payment.objects.get(ref=ref)
                payment.is_success = True
                payment.save()
                return redirect('frontend:payment_processing')
        else:
            # Return an error response if the signature verification fails
            return HttpResponse(status=403)
    
    else:
        # Return an error response if the request method is not POST
        return HttpResponse(status=405)


def payment_processing(request):
    payment_id = request.session.get('payment_id')

    if payment_id is None:
        # Redirect to an error page or handle the error appropriately
        return HttpResponse("Error: Payment ID not found in session")
    
    try:
        # Retrieve payment from the database
        payment = Payment.objects.get(pk=payment_id)
        
        # Simulate processing time
        time.sleep(3)
        
        # If payment successful, redirect to confirmation page
        if payment.is_success:
            return redirect('frontend:payment_complete')
        else:
            # Render the processing page if payment status is not successful
            return render(request, 'payment_processing.html')
    except Payment.DoesNotExist:
        # Handle the case where the payment record does not exist
        return HttpResponse("Error: Payment does not exist")
    

def payment_complete(request):
    return render(request, 'payment_comlete.html')
