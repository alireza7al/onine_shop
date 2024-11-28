from django.shortcuts import render

# Create your views here.


from django.shortcuts import render


def home_view(request):
    return render(request, 'home-2.html')
