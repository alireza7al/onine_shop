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


]

