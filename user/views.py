from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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