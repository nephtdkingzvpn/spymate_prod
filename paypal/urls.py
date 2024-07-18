from django.urls import path

from . import views

app_name = 'paypal'

urlpatterns = [
    path('sp1/paypal_payment/', views.make_paypal_payment, name='make_paypal_payment'),
    path('sp1/payment-return/', views.payment_return, name='payment_return'),
    path('sp1/payment-cancel/', views.payment_cancel, name='payment_cancel'),
]