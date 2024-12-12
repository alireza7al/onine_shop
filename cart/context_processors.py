from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}

def cart_quantity(request):
    cart = Cart(request)
    return {'cart_quantity': cart.__len__()}