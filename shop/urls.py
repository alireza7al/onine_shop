from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from shop import views

app_name = 'shop'

urlpatterns = [
                  path('', views.index_view, name='product_list'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
