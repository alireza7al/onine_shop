from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .cart import Cart
from shop.models import Product
from django.http import JsonResponse


# Create your views here.
def cart_view(request):
    cart = Cart(request)
    cart_items = cart.get_product()

    total_price = cart.get_total_price()
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))  # اگر تعدادی ارسال نشده بود، پیش‌فرض 1 در نظر گرفته می‌شود
        cart.add(product=product, quantity=quantity)

        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_delete(request):
    cart = Cart(request)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart.remove(product_id)

        cart_quantity = cart.__len__()
        total_price = cart.get_total_price()
        response = JsonResponse({'qty': cart_quantity , 'total_price': total_price})
        return response



