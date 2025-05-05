from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from user.models import Profile
from .models import Order, OrderItem, ShippingAddress, Wallet, Transaction
from .forms import ShippingAddressForm, DepositForm
from cart.cart import Cart
import requests
import logging

logger = logging.getLogger(__name__)


@login_required
def create_shipping_address(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    cart = Cart(request)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.Shipping_user = user
            shipping_address.save()

            order = Order.objects.create(
                user=user,
                shipping_address=shipping_address,
                total_price=cart.get_total_price(),
                is_paid=False,
                status='pending'  # اضافه شدن وضعیت سفارش
            )
            request.session['order_id'] = order.id
            request.session['cart_total'] = cart.get_total_price()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=int(item['price'])
                )

            return redirect('payment:choose_payment_method', order_id=order.id)
    else:
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


@login_required
def choose_payment_method(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    needed_amount = max(0, order.total_price - wallet.balance)

    context = {
        'order': order,
        'wallet_balance': wallet.balance,
        'needed_amount': needed_amount,
    }
    return render(request, 'payment/choose_payment_method.html', context)


@login_required
def process_payment(request, order_id):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if payment_method == 'wallet':
            return pay_with_wallet(request, order.id)
        elif payment_method == 'gateway':
            return redirect_to_payment_gateway(order)
        else:
            messages.error(request, 'روش پرداخت نامعتبر است')
            return redirect('payment:choose_payment_method', order_id=order.id)
    else:
        return redirect('payment:choose_payment_method', order_id=order_id)


def redirect_to_payment_gateway(order):
    MERCHANT = "aaaaaaaaaabbbbbbbbbbcccccccccc123456"
    amount = order.total_price
    description = f"Payment for order #{order.id}"
    callback_url = 'http://localhost:8000/payment/verify/'

    data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "description": description,
        "callback_url": callback_url,
    }

    response = requests.post('https://sandbox.zarinpal.com/pg/v4/payment/request.json', json=data)
    if response.status_code == 200:
        result = response.json()
        if result['data']['code'] == 100:
            payment_url = f"https://sandbox.zarinpal.com/pg/StartPay/{result['data']['authority']}"
            return redirect(payment_url)
        else:
            return redirect('payment:error')
    else:
        return redirect('payment:error')


def verify_payment(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if status == 'OK':
        MERCHANT = "aaaaaaaaaabbbbbbbbbbcccccccccc123456"
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        amount = float(order.total_price)

        data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": authority,
        }

        response = requests.post('https://sandbox.zarinpal.com/pg/v4/payment/verify.json', json=data)
        if response.status_code == 200:
            result = response.json()
            if result['data']['code'] == 100:
                with transaction.atomic():
                    order.is_paid = True
                    order.ref_id = result['data']['ref_id']
                    order.payment_method = 'gateway'
                    order.status = 'paid'  # به روزرسانی وضعیت سفارش
                    order.save()

                    for order_item in order.items.all():
                        product = order_item.product
                        product.sales_count = F('sales_count') + order_item.quantity
                        product.save(update_fields=['sales_count'])

                    cart = Cart(request)
                    cart.clear()
                    if 'cart_total' in request.session:
                        del request.session['cart_total']

                messages.success(request, 'پرداخت شما با موفقیت انجام شد.')
                return redirect('payment:order_detail', order_id=order.id)
            else:
                messages.error(request, 'پرداخت ناموفق بود. لطفاً مجدداً تلاش کنید.')
                return redirect('payment:order_detail', order_id=order.id)
        else:
            messages.error(request, 'خطا در ارتباط با درگاه پرداخت')
            return redirect('payment:order_detail', order_id=order.id)
    else:
        messages.warning(request, 'پرداخت توسط شما لغو شد.')
        order_id = request.session.get('order_id')
        if order_id:
            return redirect('payment:order_detail', order_id=order_id)
        return redirect('payment:error')


@login_required
@transaction.atomic
def pay_with_wallet(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart = Cart(request)

    if order.is_paid:
        messages.error(request, 'این سفارش قبلاً پرداخت شده است.')
        return redirect('payment:order_detail', order_id=order.id)

    wallet = Wallet.objects.select_for_update().get(user=request.user)

    if wallet.balance >= order.total_price:
        try:
            wallet.deduct_balance(order.total_price,
                                  description=f'پرداخت سفارش #{order.id}',
                                  transaction_type='purchase')

            order.is_paid = True
            order.payment_method = 'wallet'
            order.status = 'paid'  # به روزرسانی وضعیت سفارش
            order.save()

            cart.clear()
            if 'cart_total' in request.session:
                del request.session['cart_total']

            messages.success(request, 'پرداخت با کیف پول با موفقیت انجام شد.')
            return redirect('payment:order_detail', order_id=order.id)

        except Exception as e:
            messages.error(request, 'خطا در پرداخت با کیف پول')
            logger.error(f"Wallet payment error: {str(e)}")
            return redirect('payment:order_detail', order_id=order.id)
    else:
        messages.error(request, 'موجودی کیف پول شما کافی نیست.')
        return redirect('payment:choose_payment_method', order_id=order.id)


@login_required
def deposit(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    needed_amount = request.GET.get('needed_amount')
    order_id = request.session.get('order_id')

    # بررسی وجود سفارش معتبر
    valid_order = False
    if order_id:
        try:
            order = Order.objects.get(id=order_id, user=request.user, is_paid=False)
            valid_order = True
        except Order.DoesNotExist:
            order_id = None
            if 'order_id' in request.session:
                del request.session['order_id']

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            Transaction.objects.filter(
                wallet=wallet,
                status='pending',
                transaction_type='deposit'
            ).delete()

            payment_transaction = Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type='deposit',
                description='در انتظار پرداخت شارژ کیف پول',
                status='pending'
            )

            MERCHANT = "aaaaaaaaaabbbbbbbbbbcccccccccc123456"
            description = f"شارژ کیف پول به مبلغ {amount} تومان"
            callback_url = request.build_absolute_uri(
                reverse('payment:verify_deposit') + f'?order_id={order_id}' if valid_order else reverse('payment:verify_deposit')
            )

            data = {
                "merchant_id": MERCHANT,
                "amount": amount,
                "description": description,
                "callback_url": callback_url,
                "metadata": {"transaction_id": str(payment_transaction.id)}
            }

            response = requests.post(
                'https://sandbox.zarinpal.com/pg/v4/payment/request.json',
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                if result['data']['code'] == 100:
                    payment_transaction.payment_id = result['data']['authority']
                    payment_transaction.save()
                    payment_url = f"https://sandbox.zarinpal.com/pg/StartPay/{result['data']['authority']}"
                    return redirect(payment_url)
                else:
                    messages.error(request, f'خطا در اتصال به درگاه پرداخت. کد خطا: {result["data"]["code"]}')
            else:
                messages.error(request, 'خطا در ارتباط با سرور پرداخت')
    else:
        form = DepositForm(initial={'amount': needed_amount} if needed_amount else None)

    return render(request, 'wallet/deposit.html', {
        'form': form,
        'needed_amount': needed_amount,
        'from_order': valid_order  # اضافه کردن این متغیر برای نمایش در تمپلیت
    })


@login_required
def verify_deposit(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    order_id = request.GET.get('order_id')

    if status != 'OK':
        messages.warning(request, 'پرداخت توسط شما لغو شد.')
        return redirect('payment:deposit')

    try:
        MERCHANT = "aaaaaaaaaabbbbbbbbbbcccccccccc123456"
        payment_transaction = Transaction.objects.select_related('wallet').get(
            payment_id=authority,
            wallet__user=request.user,
            status='pending'
        )
        amount = payment_transaction.amount

        data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": authority,
        }

        response = requests.post(
            'https://sandbox.zarinpal.com/pg/v4/payment/verify.json',
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            if result['data']['code'] == 100:
                with transaction.atomic():
                    payment_transaction.wallet.add_balance(
                        amount=amount,
                        description=f"شارژ کیف پول ({result['data']['ref_id']})",
                        transaction_type='deposit',
                        update_transaction=payment_transaction
                    )

                    payment_transaction.payment_id = result['data']['ref_id']
                    payment_transaction.save()

                messages.success(request, f'کیف پول شما با موفقیت به مبلغ {amount:,} تومان شارژ شد.')

                # تغییر اصلی اینجا است:
                if order_id and Order.objects.filter(id=order_id, user=request.user, is_paid=False).exists():
                    # فقط اگر سفارش پرداخت نشده وجود دارد به صفحه انتخاب روش پرداخت برو
                    return redirect('payment:choose_payment_method', order_id=order_id)
                # در غیر این صورت به صفحه کیف پول برگرد
                return redirect('payment:wallet_detail')

            else:
                error_msg = f'پرداخت ناموفق بود. کد خطا: {result["data"]["code"]}'
                if result["data"]["code"] == 101:
                    error_msg = "این تراکنش قبلاً با موفقیت ثبت شده است"
                payment_transaction.status = 'failed'
                payment_transaction.save()
                messages.error(request, error_msg)
        else:
            payment_transaction.status = 'failed'
            payment_transaction.save()
            messages.error(request, 'خطا در ارتباط با سرور پرداخت')
    except Transaction.DoesNotExist:
        messages.error(request, 'تراکنش معتبر نیست')
    except Exception as e:
        messages.error(request, 'خطا در تأیید پرداخت')
        logger.error(f"Deposit verification error: {str(e)}")

    return redirect('payment:deposit')


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


@login_required
def wallet_detail(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = wallet.transactions.all().order_by('-created_at')
    context = {
        'wallet': wallet,
        'transactions': transactions,
    }
    return render(request, 'wallet/detail.html', context)