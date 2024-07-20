from django.urls import path

from . import views

app_name = 'paypalclient'

urlpatterns = [
    path('sp1/client-payment/', views.paypal_client_payment, name='paypal_client_payment'),
]