from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.contrib import messages
from django.db.models import Q


def index_view(request):
    all_products = Product.objects.all()
    context = {
        'products': all_products
    }
    return render(request, 'index.html', context)


def search_view(request):
    if request.method == 'POST':
        search_value = request.POST.get('search')

        products = Product.objects.filter(Q(name__icontains=search_value) | Q(description__icontains=search_value))
        if products:
            return render(request, 'search.html', {'products': products})
        else:
            messages.success(request, ('نتیجه ای برای جستجوی شما یافت نشد !'))
            return redirect('shop:search')
    else:
        return render(request, 'search.html', {})


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


def categories_page(request):
    all_category = Category.objects.all()
    context = {
        'all_category': all_category
    }
    return render(request, 'categories_page.html', context)
