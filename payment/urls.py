from django.urls import path
from payment import views

app_name = 'payment'


urlpatterns = [
    path('shipping_address/', views.create_shipping_address, name='create_shipping_address'),

]

