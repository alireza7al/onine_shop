from django.urls import path
from Products import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'Products'

urlpatterns = [

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
