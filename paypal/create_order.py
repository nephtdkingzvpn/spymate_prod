import json
from django.http import JsonResponse
from .paypal_services import PayPalPaymentService
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def create_order(request):
    try:
        data = json.loads(request.body)
        payment_method = data.get('payment_method')

        if payment_method == 'credit_card':
            payment_data = {
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"  # This tells PayPal to use the hosted fields
                },
                "transactions": [{
                    "amount": {
                        "total": str(data['item_price'] * data['item_quantity']),
                        "currency": data['item_currency'],
                    },
                    "item_list": {
                        "items": [{
                            "name": data['item_name'],
                            "sku": data['item_sku'],
                            "price": str(data['item_price']),
                            "currency": data['item_currency'],
                            "quantity": data['item_quantity']
                        }]
                    },
                    "description": "This is the payment transaction description."
                }],
                "redirect_urls": {
                    "return_url": request.build_absolute_uri(reverse('payment_return')),
                    "cancel_url": request.build_absolute_uri(reverse('payment_cancel'))
                }
            }

            paypal_payment_service = PayPalPaymentService()
            payment = paypal_payment_service.create_payment(payment_data)
            if payment.create():
                return JsonResponse({'orderID': payment.id})
            else:
                return JsonResponse({'error': payment.error}, status=500)
        else:
            return JsonResponse({'error': 'Invalid payment method'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
