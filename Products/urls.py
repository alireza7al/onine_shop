from django.urls import path
from Products import views

app_name = 'Products'

urlpatterns = [
    path('', views.homeView, name='home'),
]