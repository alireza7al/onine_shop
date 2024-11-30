from django.shortcuts import render
from .models import Product


def index_view(request):
    all_products = Product.objects.all()
    context = {
        'products': all_products
    }
    return render(request, 'index.html', context)
