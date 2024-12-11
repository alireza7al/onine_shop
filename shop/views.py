from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.contrib import messages


# views.py
# def custom_404_view(request, exception):
#     return render(request, 'parts/error_404.html', status=404)


def index_view(request):
    all_products = Product.objects.all()
    context = {
        'products': all_products
    }
    return render(request, 'index.html', context)


def about_view(request):
    return render(request, 'about.html')


def detail_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)


def category_view(request, cat):
    cat = cat.replace('_', ' ')
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        context = {
            'products': products,
            'category': category
        }
        return render(request, 'category_product.html', context)
    except Category.DoesNotExist:
        return redirect('shop:home')
        messages.success(request, 'دسته بندی وجود نداشت !')


