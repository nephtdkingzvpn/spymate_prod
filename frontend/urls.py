from django.urls import path

from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('sp1/payment/', views.make_payment, name='make_payment'),
    path('sp1/payment/processing/', views.payment_processing, name='payment_processing'),
    path('sp1/payment/complete/', views.payment_complete, name='payment_complete'),
    path('payement/details/ar-ab-ac', views.flutterwave_webhook, name='flutterwave_webhook'),
]