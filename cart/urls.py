from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'cart'


urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/', views.cart_add, name='add'),
    path('delete/', views.cart_delete, name='delete'),
    path('update/', views.cart_update, name='update'),

]

