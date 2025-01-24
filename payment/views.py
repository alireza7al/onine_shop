from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from user.models import Profile
from .models import Order, OrderItem, ShippingAddress
from .forms import ShippingAddressForm
from cart.cart import Cart  # فرض کنید یک سیستم سبد خرید دارید
import requests  # برای اتصال به درگاه پرداخت

import logging
from django.urls import reverse
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException


@login_required
def create_shipping_address(request):
    user = request.user
    profile = Profile.objects.get(user=user)  # گرفتن پروفایل کاربر
    cart = Cart(request)  # سبد خرید کاربر

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            # ذخیره آدرس ارسال
            shipping_address = form.save(commit=False)
            shipping_address.Shipping_user = user
            shipping_address.save()

            # ایجاد سفارش
            order = Order.objects.create(
                user=user,
                shipping_address=shipping_address,
                total_price=cart.get_total_price(),  # مبلغ کل سبد خرید
                is_paid=False  # هنوز پرداخت نشده
            )
            request.session['order_id'] = order.id
            # ذخیره آیتم‌های سفارش
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=int(item['price'])
                )

            # پاک کردن سبد خرید
            cart.clear()

            # انتقال به درگاه پرداخت
            return redirect_to_payment_gateway(order)  # فراخوانی تابع برای هدایت به درگاه پرداخت
    else:
        # تنظیم مقادیر پیش‌فرض از پروفایل کاربر
        initial_data = {
            'Shipping_full_name': f"{profile.first_name} {profile.last_name}",
            'Shipping_email': profile.email,
            'Shipping_phone_number': profile.phone_number,
            'Shipping_province': profile.province,
            'Shipping_city': profile.city,
            'Shipping_address1': profile.address1,
            'Shipping_postal_code': profile.postal_code,
        }
        form = ShippingAddressForm(initial=initial_data)

    return render(request, 'shipping_address.html', {'form': form})


def redirect_to_payment_gateway(order):
    MERCHANT = "aaaaaaaaaabbbbbbbbbbcccccccccc123456"  # کد مرچنت زرین‌پال
    amount = order.total_price  # مبلغ سفارش
    description = f"Payment for order #{order.id}"  # توضیحات پرداخت
    callback_url = 'http://localhost:8000/payment/verify/'  # آدرس بازگشت پس از پرداخت

    data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "description": description,
        "callback_url": callback_url,
    }

    # ارسال درخواست به زرین‌پال
    response = requests.post('https://sandbox.zarinpal.com/pg/v4/payment/request.json', json=data)
    if response.status_code == 200:
        result = response.json()
        if result['data']['code'] == 100:
            # انتقال کاربر به درگاه پرداخت
            payment_url = f"https://sandbox.zarinpal.com/pg/StartPay/{result['data']['authority']}"
            return redirect(payment_url)
        else:
            # خطا در اتصال به درگاه پرداخت
            return redirect('payment:error')
    else:
        # خطا در ارتباط با سرور زرین‌پال
        return redirect('payment:error')


def verify_payment(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if status == 'OK':
        MERCHANT = "aaaaaaaaaabbbbbbbbbbcccccccccc123456"
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        amount = float(order.total_price)  # تبدیل به float

        data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": authority,
        }

        response = requests.post('https://sandbox.zarinpal.com/pg/v4/payment/verify.json', json=data)
        if response.status_code == 200:
            result = response.json()
            print("Response from Zarinpal:", result)  # چاپ پاسخ زرین‌پال برای دیباگ
            if result['data']['code'] == 100:
                # پرداخت موفق
                order.is_paid = True
                order.ref_id = result['data']['ref_id']
                order.save()

                for order_item in order.items.all():  # استفاده از related_name='items'
                    product = order_item.product
                    product.sales_count = F('sales_count') + order_item.quantity
                    product.save(update_fields=['sales_count'])
                return redirect('payment:success')
            else:
                # پرداخت ناموفق
                return redirect('payment:error')
        else:
            # خطا در ارتباط با سرور زرین‌پال
            print("Failed to connect to Zarinpal. Status code:", response.status_code)
            return redirect('payment:error')
    else:
        # کاربر از پرداخت انصراف داده است
        print("User canceled the payment.")
        return redirect('payment:error')


def success(request):
    return render(request, 'success.html')


def error(request):
    return render(request, 'error.html')


@login_required
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})