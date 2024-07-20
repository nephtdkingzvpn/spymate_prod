from django.urls import path

from . import views

app_name = 'paypalclient'

urlpatterns = [
    path('sp1/client-payment/', views.paypal_client_payment, name='paypal_client_payment'),
    path('sp1/capture-payment/', views.capture_payment, name='capture_payment'),
    path('sp1/payment-success/', views.payment_success, name='payment_success'),
    path('sp1/payment-failure/', views.payment_failure, name='payment_failure'),
]