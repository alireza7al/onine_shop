from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError


class SingUpForm(UserCreationForm):
    first_name = forms.CharField(
        label='',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'نام خود را وارد کنید'}),

    )

    last_name = forms.CharField(
        label='',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'نام خانوادگی خود را وارد کنید'}),

    )

    email = forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'ایمیل خود را وارد کنید '}),
        help_text='ایمیل معتبر وارد کنید'
    )

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
                'placeholder': 'رمز خود را وارد کنید ',
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
                'placeholder': 'رمز خود را دوباره وارد کنید ',
                'name': 'password',
                'type': 'password',
            }
        ),
        help_text='رمز عبور باید با رمز عبور اولیه یکسان باشد'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
