from django.db import models
from django.contrib.auth.models import User


class ShippingAddress(models.Model):
    Shipping_user = models.ForeignKey(User, on_delete=models.CASCADE)
    Shipping_full_name = models.CharField(max_length=100)
    Shipping_email = models.EmailField(max_length=100, blank=True)
    Shipping_phone_number = models.CharField(max_length=15, blank=True)
    Shipping_province = models.CharField(max_length=25, blank=True)
    Shipping_city = models.CharField(max_length=25, blank=True)
    Shipping_address1 = models.CharField(max_length=100, blank=True)
    Shipping_postal_code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.Shipping_user},{self.Shipping_city}, {self.Shipping_address1},"

    class Meta:
        verbose_name_plural = 'Shipping Address'
