from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import F
from .models import Comment
from .forms import CommentForm
from shop.models import Product
from django.contrib.auth.models import User
from .forms import RatingForm
@login_required
def add_comment_to_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            # تگ کردن کاربران
            tagged_users = request.POST.get('tagged_users')
            if tagged_users:
                for username in tagged_users.split(','):
                    user = User.objects.get(username=username.strip())
                    send_mail(
                        'شما در یک کامنت تگ شده‌اید',
                        f'شما در یک کامنت در محصول {product.name} تگ شده‌اید.',
                        'from@example.com',
                        [user.email],
                        fail_silently=False,
                    )
            return redirect('shop:product', pk=product.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_product.html', {'form': form})

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        return redirect('shop:product', pk=comment.product.pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('shop:product', pk=comment.product.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        return redirect('shop:product', pk=comment.product.pk)
    comment.delete()
    return redirect('shop:product', pk=comment.product.pk)

@login_required
def reply_to_comment(request, pk):
    parent_comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = parent_comment.product
            comment.user = request.user
            comment.parent = parent_comment
            comment.save()
            return redirect('shop:product', pk=parent_comment.product.pk)
    else:
        form = CommentForm()
    return render(request, 'reply_to_comment.html', {'form': form, 'parent_comment': parent_comment})

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.likes += 1
    comment.save()
    return redirect('shop:product', pk=comment.product.pk)

@login_required
def dislike_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.dislikes += 1
    comment.save()
    return redirect('shop:product', pk=comment.product.pk)

@login_required
def approve_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approved_comment = True
    comment.save()
    return redirect('shop:product', pk=comment.product.pk)

@login_required
def report_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.reports += 1
    comment.save()
    return redirect('shop:product', pk=comment.product.pk)

@login_required
def rate_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == "POST":
        form = RatingForm(request.POST)  # ایجاد فرم با داده‌های ارسالی
        if form.is_valid():  # اعتبارسنجی فرم
            rating = form.cleaned_data['rating']  # دریافت مقدار rating از فرم
            comment.rating = int(rating)  # تبدیل به عدد و ذخیره
            comment.save()
            messages.success(request, 'امتیاز شما با موفقیت ثبت شد.')
            return redirect('shop:product', pk=comment.product.pk)
        else:
            messages.error(request, 'لطفاً یک امتیاز معتبر انتخاب کنید.')
    else:
        form = RatingForm()  # ایجاد فرم خالی برای درخواست GET

    return render(request, 'rate_comment.html', {'comment': comment, 'form': form})