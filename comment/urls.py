from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('add_comment_to_product/<int:pk>/', views.add_comment_to_product, name='add_comment_to_product'),
    path('like_comment/', views.like_comment, name='like_comment'),
    path('dislike_comment/', views.dislike_comment, name='dislike_comment'),
    path('history/', views.user_comment_history, name='comment_history'),
    path('edit/<int:pk>/', views.edit_comment, name='edit_comment'),
    path('delete/<int:pk>/', views.delete_comment, name='delete_comment'),
]