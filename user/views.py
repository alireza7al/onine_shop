from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SingUpForm


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'با موفقیت وارد شدید !')
            return redirect('shop:home')
        else:
            messages.success(request, 'مشکلی در لاگین وجود داشت !')
            return redirect('user:login')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید!')
    return redirect('shop:home')









def translate_error(field, error):
    translations = {
        'first_name': {
            'This field is required.': 'نام نمی‌تواند خالی باشد.',
            'Ensure this value has at most 30 characters (it has 31).': 'نام نمی‌تواند بیشتر از 30 کاراکتر باشد.',
        },
        'last_name': {
            'This field is required.': 'نام خانوادگی نمی‌تواند خالی باشد.',
            'Ensure this value has at most 30 characters (it has 31).': 'نام خانوادگی نمی‌تواند بیشتر از 30 کاراکتر باشد.',
        },
        'email': {
            'This field is required.': 'ایمیل نمی‌تواند خالی باشد.',
            'Enter a valid email address.': 'ایمیل وارد شده معتبر نیست.',
        },
        'username': {
            'This field is required.': 'نام کاربری نمی‌تواند خالی باشد.',
            'Ensure this value has at most 20 characters (it has 21).': 'نام کاربری نمی‌تواند بیشتر از 20 کاراکتر باشد.',
            'A user with that username already exists.': 'این نام کاربری قبلا استفاده شده است.',
        },
        'password1': {
            'This field is required.': 'رمز عبور نمی‌تواند خالی باشد.',
            'This password is too short. It must contain at least 8 characters.': 'رمز عبور باید حداقل 8 کاراکتر داشته باشد.',
            'This password is too common.': 'رمز عبور باید به سادگی قابل حدس زدن نباشد.',
            'This password is entirely numeric.': 'رمز عبور نمی‌تواند کاملا عددی باشد.',
        },
        'password2': {
            'This field is required.': 'تکرار رمز عبور نمی‌تواند خالی باشد.',
            'The two password fields didn’t match.': 'رمز عبور و تکرار آن باید یکسان باشند.',
        },
    }
    return translations.get(field, {}).get(error, None)

def signup_user(request):
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            messages.success(request, ('اکانت شما با موفقیت ساخته شد'))
            return redirect('shop:home')
        else:
            # نمایش خطاهای خاص به کاربر
            for field, errors in form.errors.items():
                for error in errors:
                    translated_error = translate_error(field, error)
                    if translated_error:
                        messages.error(request, f'{form.fields[field].label}: {translated_error}')
            return redirect('user:signup')
    else:
        form = SingUpForm()
        return render(request, 'singup2.html', {'form': form})
