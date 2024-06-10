import requests
import math
import random
import hmac
import hashlib
import base64
import uuid
import time


def bitcoin_payment_type(request):
    return

def card_payment(name, email, phone, url, ref):
    s_key = 'FLWSECK_TEST-b7225a52e224af68a0f5199c0ddaac5c-X'
    payload = {
        "tx_ref": ref,  
        "amount": 30,
        "currency": "USD",
        "email": email,
        "redirect_url": url,
        "meta":{
            "consumer_id":23,
            "consumer_mac":"92a3-912ba-1192a"
        },
        "customer":{
            "email":email,
            "phone_number":phone,
            "name":name
        },
    }

    # Make a POST request to Flutterwave's payment endpoint
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+ s_key,
    }
    response = requests.post("https://api.flutterwave.com/v3/payments", json=payload, headers=headers)


    # print("Response Headers:")
    # for header, value in response.headers.items():
    #     print(f"{header}: {value}")

    # print("Response Content:")
    # print(response.text)

    # response.raise_for_status()
    
    if response.ok:
        return response.json(), None
    else:
        # If the response is not okay, extract and return the error message
        error_message = response.json().get('message', 'Payment request failed')
        return None, error_message



def verify_flutterwave_signature(request):
    # Retrieve the signature and payload from the request headers
    signature = request.headers.get('verif-hash')
    payload = request.body

    # Retrieve your Flutterwave webhook secret from your environment variables or settings
    # Make sure to replace 'YOUR_FLUTTERWAVE_WEBHOOK_SECRET' with your actual secret
    webhook_secret = 'blazisworkingwell'

    # Calculate the expected signature using HMAC-SHA256
    # expected_signature = base64.b64encode(
    #     hmac.new(
    #         webhook_secret.encode('utf-8'),
    #         payload,
    #         hashlib.sha256
    #     ).digest()
    # ).decode('utf-8')

    # Compare the expected signature with the received signature
    if signature == webhook_secret:
        # Signature is valid
        return True
    else:
        # Signature is not valid
        return False



def generate_tx_ref():
    # Generate a unique identifier
    unique_id = str(uuid.uuid4()).replace('-', '')[:8]  # Take the first 8 characters of a UUID
    
    # Generate a timestamp (Unix time)
    timestamp = str(int(time.time()))
    
    # Generate a random string
    random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
    
    # Concatenate the elements to form the tx_ref
    tx_ref = f'{timestamp}-{unique_id}-{random_string}'
    
    return tx_ref
