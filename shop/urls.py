from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from shop import views

app_name = 'shop'


urlpatterns = [
    path('', views.index_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('product/<int:pk>', views.detail_view, name='product'),
    path('category/<str:cat>', views.category_view, name='category'),
    path('category/page/', views.categories_page, name='categories_page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

