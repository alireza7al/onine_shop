from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('add_comment_to_product/<int:pk>/', views.add_comment_to_product, name='add_comment_to_product'),
    path('edit_comment/<int:pk>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('reply_to_comment/<int:pk>/', views.reply_to_comment, name='reply_to_comment'),
    path('like/<int:pk>/', views.like_comment, name='like_comment'),
    path('dislike/<int:pk>/', views.dislike_comment, name='dislike_comment'),
    path('approve_comment/<int:pk>/', views.approve_comment, name='approve_comment'),
    path('report_comment/<int:pk>/', views.report_comment, name='report_comment'),
    path('rate_comment/<int:pk>/', views.rate_comment, name='rate_comment'),
]