from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('update-password/', views.UpdatePasswordView, name='update_password'),



]








