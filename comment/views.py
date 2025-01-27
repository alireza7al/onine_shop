from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
from shop.models import Product
from django.http import JsonResponse
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
            return redirect('shop:product', pk=product.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_product.html', {'form': form})

@login_required
def like_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_id)

        if f'liked_{comment_id}' not in request.session:
            comment.likes += 1
            comment.save()
            request.session[f'liked_{comment_id}'] = True
            return JsonResponse({'likes': comment.likes})
        else:
            return JsonResponse({'error': 'شما قبلاً این نظر را لایک کرده‌اید.'}, status=400)


@login_required
def dislike_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_id)

        if f'disliked_{comment_id}' not in request.session:
            comment.dislikes += 1
            comment.save()
            request.session[f'disliked_{comment_id}'] = True
            return JsonResponse({'dislikes': comment.dislikes})
        else:
            return JsonResponse({'error': 'شما قبلاً این نظر را دیس‌لایک کرده‌اید.'}, status=400)


@login_required
def user_comment_history(request):
    # دریافت تمام کامنت‌های کاربر جاری و مرتب‌سازی بر اساس تاریخ (جدیدترین اول)
    comments = Comment.objects.filter(user=request.user).order_by('-created_date')

    # ارسال کامنت‌ها به تمپلیت
    return render(request, 'comment_history.html', {'comments': comments})
@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.user:
        messages.error(request, 'شما مجاز به ویرایش این نظر نیستید.')
        return redirect('comment:comment_history')

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'نظر شما با موفقیت ویرایش شد.')
            return redirect('comment:comment_history')
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.user:
        messages.error(request, 'شما مجاز به حذف این نظر نیستید.')
        return redirect('comment:comment_history')

    if request.method == "POST":
        comment.delete()
        messages.success(request, 'نظر شما با موفقیت حذف شد.')
        return redirect('comment:comment_history')

    return render(request, 'confirm_delete_comment.html', {'comment': comment})