from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, F
from .models import Product, Category
from comment.models import Comment
from django.core.paginator import Paginator

def index_view(request):
    all_products = Product.objects.all()

    # فیلتر بر اساس دسته‌بندی
    category_filter = request.GET.get('category')
    if category_filter:
        all_products = all_products.filter(category__name=category_filter)

    # فیلتر بر اساس قیمت
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        all_products = all_products.filter(price__gte=min_price)
    if max_price:
        all_products = all_products.filter(price__lte=max_price)

    # فیلتر بر اساس محبوب‌ترین‌ها (بیشترین ستاره)
    popular_filter = request.GET.get('popular')
    if popular_filter:
        all_products = all_products.order_by('-star')

    # فیلتر بر اساس پرفروش‌ترین‌ها (بیشترین فروش)
    best_selling_filter = request.GET.get('best_selling')
    if best_selling_filter:
        all_products = all_products.order_by('-sales_count')

    # فیلتر بر اساس پر بازدیدترین‌ها (بیشترین بازدید)
    most_viewed_filter = request.GET.get('most_viewed')
    if most_viewed_filter:
        all_products = all_products.order_by('-views_count')

    # فیلتر بر اساس فروش ویژه
    on_sale_filter = request.GET.get('on_sale')
    if on_sale_filter:
        all_products = all_products.filter(is_sale=True)

    context = {
        'products': all_products,
        'categories': Category.objects.all()  # برای نمایش دسته‌بندی‌ها در تمپلیت
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
    # دریافت محصول بر اساس شناسه (pk)
    product = get_object_or_404(Product, id=pk)

    # افزایش تعداد بازدیدهای محصول
    Product.objects.filter(id=pk).update(views_count=F('views_count') + 1)

    # دریافت کامنت‌های تاییدشده مربوط به محصول
    comments = Comment.objects.filter(product=product)

    # مرتب‌سازی کامنت‌ها بر اساس پارامتر دریافتی از کاربر
    sort_by = request.GET.get('sort_by')
    if sort_by == 'newest':
        comments = comments.order_by('-created_date')
    elif sort_by == 'oldest':
        comments = comments.order_by('created_date')
    elif sort_by == 'most_liked':
        comments = comments.order_by('-likes')
    elif sort_by == 'most_disliked':
        comments = comments.order_by('-dislikes')

    # صفحه‌بندی کامنت‌ها (۱۰ کامنت در هر صفحه)
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # آماده‌سازی داده‌ها برای ارسال به تمپلیت
    context = {
        'product': product,
        'comments': page_obj,
    }

    # رندر کردن تمپلیت با داده‌های آماده‌شده
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