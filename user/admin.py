from django.contrib import admin
from .models import Customer

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'پروفایل'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


# ثبت مدل User با کلاس CustomUserAdmin
admin.site.unregister(User)  # ابتدا مدل User را از پنل ادمین حذف می‌کنیم
admin.site.register(User, CustomUserAdmin)  # سپس آن را با کلاس CustomUserAdmin ثبت می‌کنیم


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('email',)
