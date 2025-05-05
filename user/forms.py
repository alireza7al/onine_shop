from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from .models import Profile
from django.core.exceptions import ValidationError


class SingUpForm(UserCreationForm):
    username = forms.CharField(
        label='',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'نام کاربری خود را وارد کنید'}),
        help_text='حداقل یک کاراکتر و حداکثر 20 کاراکتر'
    )

    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form__input',
                'placeholder': 'رمز خود را وارد کنید',
                'name': 'password',
                'type': 'password',
            }
        ),
        help_text='حداقل 8 کاراکتر، شامل حروف و اعداد و کاراکتر مثل@#$% و...'
    )

    password2 = forms.CharField(
        label=' ',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form__input',
                'placeholder': 'رمز خود را دوباره وارد کنید',
                'name': 'password',
                'type': 'password',
            }
        ),
        help_text='رمز عبور باید با رمز عبور اولیه یکسان باشد'
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # بدون ایمیل


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label='نام',
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'نام خود را وارد کنید'}),
        help_text=''
    )

    last_name = forms.CharField(
        label='نام خانوادگی',
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'نام خانوادگی خود را وارد کنید'}),
        help_text=''
    )

    email = forms.EmailField(
        label='ایمیل',
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form__input', 'placeholder': 'ایمیل خود را وارد کنید'}),
        help_text=''
    )
    province = forms.CharField(
        label='استان',
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'استان خود را وارد کنید'}),
        help_text=''
    )
    city = forms.CharField(
        label='شهر',
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'شهر خود را وارد کنید'}),
        help_text=''
    )

    address1 = forms.CharField(
        label='آدرس اول',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'آدرس خود را وارد کنید'}),
        help_text=''
    )

    address2 = forms.CharField(
        label='آدرس دوم',
        max_length=100,
        required=False,  # این فیلد اختیاری است
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'آدرس دوم (اختیاری)'}),
        help_text=''
    )

    postal_code = forms.CharField(
        label='کد پستی',
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'کد پستی خود را وارد کنید'}),
        help_text=''
    )

    phone_number = forms.CharField(
        label='شماره تلفن',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'شماره تلفن خود را وارد کنید'}),
        help_text=''
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'province', 'city', 'address1', 'address2', 'postal_code',
                  'phone_number']


class UpdatePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form__input',
            'placeholder': 'رمز عبور جدید را وارد کنید',
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form__input',
            'placeholder': 'رمز عبور جدید را دوباره وارد کنید',
        })




