from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import Customer

def category_image_upload_to(instance, filename):
    return f'categories/{instance.name}/{filename}'
class Category(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to=category_image_upload_to, blank=True, null=True)

    def __str__(self):
        return self.name


def product_image_upload_to(instance, filename):
    return f'products/{instance.category}/{instance.name}/{filename}'


class Product(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField()
    price = models.DecimalField(default=0, max_digits=12, decimal_places=0)
    image = models.ImageField(upload_to=product_image_upload_to)
    created_at = models.DateTimeField(default=timezone.now)
    views_count = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)
    star = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=12, decimal_places=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product', args=[str(self.id)])

