import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib import messages
from cart.cart import Cart
from .forms import SingUpForm, ProfileUpdateForm, UpdatePasswordForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from .models import Profile
from django.contrib.auth import login


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            try:
                current_user = Profile.objects.get(user__id=request.user.id)
                save_cart = current_user.old_cart

                if save_cart:
                    converted_cart = json.loads(save_cart)
                    cart = Cart(request)
                    for key, value in converted_cart.items():
                        cart.db_add(product=key, quantity_and_price=value)
            except (Profile.DoesNotExist, json.JSONDecodeError) as e:
                messages.error(request, 'مشکلی در بازیابی سبد خرید وجود داشت.')

            messages.success(request, 'با موفقیت وارد شدید !')
            return redirect('shop:home')
        else:
            messages.error(request, 'مشکلی در لاگین وجود داشت !')
            return redirect('user:login')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید!')
    return redirect('shop:home')


def translate_error(field, error):
    translations = {'first_name': {
        'This field is required.': 'نام نمی‌تواند خالی باشد.',
        'Ensure this value has at most 30 characters (it has 31).': 'نام نمی‌تواند بیشتر از 30 کاراکتر باشد.',
    }, 'last_name': {
        'This field is required.': 'نام خانوادگی نمی‌تواند خالی باشد.',
        'Ensure this value has at most 30 characters (it has 31).': 'نام خانوادگی نمی‌تواند بیشتر از 30 کاراکتر باشد.',
    }, 'email': {
        'This field is required.': 'ایمیل نمی‌تواند خالی باشد.',
        'Enter a valid email address.': 'ایمیل وارد شده معتبر نیست.',
    }, 'username': {
        'This field is required.': 'نام کاربری نمی‌تواند خالی باشد.',
        'Ensure this value has at most 20 characters (it has 21).': 'نام کاربری نمی‌تواند بیشتر از 20 کاراکتر باشد.',
        'A user with that username already exists.': 'این نام کاربری قبلا استفاده شده است.',
    }, 'password1': {
        'This field is required.': 'رمز عبور نمی‌تواند خالی باشد.',
        'This password is too short. It must contain at least 8 characters.': 'رمز عبور باید حداقل 8 کاراکتر داشته باشد.',
        'This password is too common.': 'رمز عبور باید به سادگی قابل حدس زدن نباشد.',
        'This password is entirely numeric.': 'رمز عبور نمی‌تواند کاملا عددی باشد.',
    }, 'password2': {
        'This field is required.': 'تکرار رمز عبور نمی‌تواند خالی باشد.',
    }}
    return translations.get(field, {}).get(error, None)


def signup_user(request):
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # ایجاد کاربر با نام کاربری و رمز عبور

            # ایجاد پروفایل خالی برای کاربر
            profile = Profile.objects.get(user=user)
            profile.save()  # ذخیره پروفایل بدون ایمیل

            # ورود خودکار کاربر
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)

            messages.success(request, 'ثبت نام با موفقیت انجام شد. لطفا اطلاعات پروفایل خود را تکمیل کنید.')
            return redirect('user:profile_update')  # هدایت به صفحه تکمیل پروفایل
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    translated_error = translate_error(field, error)
                    if translated_error:
                        messages.error(request, f'{form.fields[field].label}: {translated_error}')
            return render(request, 'singup.html', {'form': form})
    else:
        form = SingUpForm()
        return render(request, 'singup.html', {'form': form})


@login_required
def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            # به روزرسانی ایمیل در مدل User اگر تغییر کرده باشد
            if 'email' in form.changed_data:
                user = request.user
                user.email = form.cleaned_data['email']
                user.save()

            return redirect('shop:home')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'profile_update.html', {'form': form})


def UpdatePasswordView(request):
    # بررسی لاگین بودن کاربر
    if not request.user.is_authenticated:
        messages.warning(request, 'برای تغییر رمز عبور، لطفاً ابتدا وارد حساب کاربری خود شوید.')
        return redirect('user:login')

    current_user = request.user

    if request.method == 'POST':
        form = UpdatePasswordForm(current_user, request.POST)
        if form.is_valid():
            try:
                user = form.save()
                update_session_auth_hash(request, user)  # جلوگیری از خروج کاربر پس از تغییر رمز
                messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت.')
                return redirect('shop:home')
            except Exception as e:
                messages.error(request, f'خطا در تغییر رمز عبور: {str(e)}')
                return redirect('user:update_password')
        else:
            # نمایش خطاهای فرم به صورت دقیق‌تر
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
            return render(request, 'update_password.html', {'form': form})

    # درخواست GET - نمایش فرم خالی
    form = UpdatePasswordForm(current_user)
    return render(request, 'update_password.html', {
        'form': form,
        'title': 'تغییر رمز عبور'
    })

