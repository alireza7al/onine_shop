from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


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


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.IntegerField()  # مبلغ کل سفارش
    is_paid = models.BooleanField(default=False)  # وضعیت پرداخت
    created_at = models.DateTimeField(auto_now_add=True)  # تاریخ ایجاد سفارش
    updated_at = models.DateTimeField(auto_now=True)  # تاریخ به‌روزرسانی سفارش
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    ref_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField()
    total_price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)