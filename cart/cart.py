from shop.models import Product
from user.models import Profile


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request

        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def db_add(self, product, quantity_and_price):
        product_id = str(product)
        if product_id in self.cart:
            pass  # اگر محصول از قبل در سبد خرید وجود دارد، کاری نکنید
        else:
            if isinstance(quantity_and_price, dict):
                self.cart[product_id] = quantity_and_price

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace('\'', '\"')
            current_user.update(old_cart=db_cart)

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity  # افزایش تعداد محصول
        elif product_id not in self.cart and product.sale_price != 0:
            self.cart[product_id] = {'price': str(product.sale_price), 'quantity': quantity}
        else:
            self.cart[product_id] = {'price': str(product.price), 'quantity': quantity}

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace('\'', '\"')
            current_user.update(old_cart=db_cart)

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_product(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_items = []

        for product in products:
            product_id = str(product.id)
            quantity = self.cart[product_id]['quantity']
            price = self.cart[product_id]['price']
            sum_quantity_price = int(quantity) * int(price)
            cart_items.append({'product': product, 'quantity': quantity, 'sum_quantity_price': sum_quantity_price})

        return cart_items

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace('\'', '\"')
            current_user.update(old_cart=db_cart)

    def get_total_price(self):
        total_price = 0
        for item in self.cart.values():
            total_price += (int(item['price']) * int(item['quantity']))

        return total_price
