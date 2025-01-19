from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'Shipping_full_name',
            'Shipping_email',
            'Shipping_phone_number',
            'Shipping_province',
            'Shipping_city',
            'Shipping_address1',
            'Shipping_postal_code',
        ]
        labels = {
            'Shipping_full_name': 'نام کامل',
            'Shipping_email': 'ایمیل',
            'Shipping_phone_number': 'شماره تلفن',
            'Shipping_province': 'استان',
            'Shipping_city': 'شهر',
            'Shipping_address1': 'آدرس ',
            'Shipping_postal_code': 'کد پستی',
        }
        widgets = {
            'Shipping_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'Shipping_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'Shipping_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'Shipping_province': forms.TextInput(attrs={'class': 'form-control'}),
            'Shipping_city': forms.TextInput(attrs={'class': 'form-control'}),
            'Shipping_address1': forms.TextInput(attrs={'class': 'form-control'}),
            'Shipping_postal_code': forms.TextInput(attrs={'class': 'form-control'}),
        }