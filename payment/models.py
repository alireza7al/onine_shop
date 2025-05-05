from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.models import Product
from django.db import transaction as db_transaction
from django.db.models import F


class ShippingAddress(models.Model):
    Shipping_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_addresses')
    Shipping_full_name = models.CharField(max_length=100, verbose_name='نام کامل')
    Shipping_email = models.EmailField(max_length=100, blank=True, verbose_name='ایمیل')
    Shipping_phone_number = models.CharField(max_length=15, blank=True, verbose_name='شماره تلفن')
    Shipping_province = models.CharField(max_length=25, blank=True, verbose_name='استان')
    Shipping_city = models.CharField(max_length=25, blank=True, verbose_name='شهر')
    Shipping_address1 = models.CharField(max_length=100, blank=True, verbose_name='آدرس')
    Shipping_postal_code = models.CharField(max_length=10, blank=True, verbose_name='کد پستی')

    class Meta:
        verbose_name = 'آدرس حمل و نقل'
        verbose_name_plural = 'آدرس‌های حمل و نقل'
        ordering = ['-id']

    def __str__(self):
        return f"{self.Shipping_user.username} - {self.Shipping_city}, {self.Shipping_address1}"


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('wallet', 'کیف پول'),
        ('gateway', 'درگاه پرداخت'),
        ('unknown', 'نامشخص'),
    )

    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('canceled', 'لغو شده'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.ForeignKey(
        ShippingAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='آدرس حمل و نقل'
    )
    total_price = models.PositiveIntegerField(verbose_name='مبلغ کل')
    is_paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='شناسه پرداخت')
    ref_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='کد پیگیری')
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        default='unknown',
        verbose_name='روش پرداخت'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='وضعیت سفارش'
    )

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"سفارش #{self.id} - {self.user.username}"

    @property
    def payment_method_display(self):
        return dict(self.PAYMENT_METHOD_CHOICES).get(self.payment_method, 'نامشخص')

    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'نامشخص')


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='سفارش'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='محصول'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    price = models.PositiveIntegerField(verbose_name='قیمت واحد')

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def __str__(self):
        return f"{self.quantity} عدد {self.product.name} در سفارش #{self.order.id}"

    @property
    def total_price(self):
        return self.quantity * self.price


class Wallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wallet',
        verbose_name='کاربر'
    )
    balance = models.PositiveIntegerField(default=0, verbose_name='موجودی (تومان)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"کیف پول {self.user.username} - {self.balance} تومان"

    def add_balance(self, amount, description='', transaction_type='deposit', update_transaction=None):
        """
        افزایش موجودی کیف پول با امکان به‌روزرسانی تراکنش موجود
        :param update_transaction: اگر ارسال شود، این تراکنش به‌روزرسانی می‌شود
        """
        with db_transaction.atomic():  # استفاده از نام مستعار
            self.balance = F('balance') + amount
            self.save(update_fields=['balance'])
            self.refresh_from_db()

            if update_transaction:
                # به‌روزرسانی تراکنش موجود
                update_transaction.amount = amount
                update_transaction.description = description
                update_transaction.status = 'completed'
                update_transaction.save()
            else:
                # ایجاد تراکنش جدید
                Transaction.objects.create(
                    wallet=self,
                    amount=amount,
                    transaction_type=transaction_type,
                    description=description,
                    status='completed'
                )

    def deduct_balance(self, amount, description='', transaction_type='withdraw'):
        """
        کاهش موجودی کیف پول با ثبت تراکنش
        """
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            Transaction.objects.create(
                wallet=self,
                amount=amount,
                transaction_type=transaction_type,
                description=description,
                status='completed'
            )
            return True
        return False


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('deposit', 'واریز'),
        ('withdraw', 'برداشت'),
        ('purchase', 'خرید'),
        ('refund', 'عودت'),
    )

    STATUS_CHOICES = (
        ('pending', 'در انتظار'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق'),
    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='کیف پول'
    )
    amount = models.PositiveIntegerField(verbose_name='مبلغ (تومان)')
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='نوع تراکنش'
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='توضیحات'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='وضعیت'
    )
    payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='شناسه پرداخت'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name='سفارش مرتبط'
    )

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"تراکنش #{self.id} - {self.get_transaction_type_display()} - {self.amount} تومان"


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    """سیگنال برای ایجاد خودکار کیف پول هنگام ثبت نام کاربر جدید"""
    if created:
        Wallet.objects.create(user=instance)
