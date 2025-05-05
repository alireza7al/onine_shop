from django.urls import path
from payment import views

app_name = 'payment'


urlpatterns = [
    path('shipping_address/', views.create_shipping_address, name='create_shipping_address'),
    path('verify/', views.verify_payment, name='verify_payment'),
    path('success/', views.success, name='success'),
    path('error/', views.error, name='error'),
    path('order_history/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    path('choose-payment/<int:order_id>/', views.choose_payment_method, name='choose_payment_method'),
    path('process-payment/<int:order_id>/', views.process_payment, name='process_payment'),

    path('wallet/', views.wallet_detail, name='wallet_detail'),
    path('wallet/deposit/', views.deposit, name='wallet_deposit'),
    path('wallet/deposit/verify/', views.verify_deposit, name='verify_deposit'),
    path('pay/<int:order_id>/', views.pay_with_wallet, name='pay'),








]

