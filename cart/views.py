from django.shortcuts import render, get_object_or_404

from .cart import Cart
from shop.models import Product
from django.http import JsonResponse


# Create your views here.
def cart_view(request):
    return render(request, 'cart.html', {})


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
    pass


def cart_update(request):
    pass
