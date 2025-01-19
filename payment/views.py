from django.shortcuts import render, redirect
from .forms import ShippingAddressForm
from user.models import Profile


def create_shipping_address(request):
    user = request.user
    profile = Profile.objects.get(user=user)  # گرفتن پروفایل کاربر

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.Shipping_user = user
            shipping_address.save()
            return redirect('shop:home')  # تغییر به URL مناسب
    else:
        # تنظیم مقادیر پیش‌فرض از پروفایل کاربر
        initial_data = {
            'Shipping_full_name': f"{profile.first_name} {profile.last_name}",
            'Shipping_email': profile.email,
            'Shipping_phone_number': profile.phone_number,
            'Shipping_province': profile.province,
            'Shipping_city': profile.city,
            'Shipping_address1': profile.address1,
            'Shipping_postal_code': profile.postal_code,
        }
        form = ShippingAddressForm(initial=initial_data)

    return render(request, 'shipping_address_form.html', {'form': form})

