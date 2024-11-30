from django.contrib import admin
from .models import Category, Product, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)





@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'star', 'views_count', 'sales_count')
    search_fields = ('name', 'description')
    list_filter = ('category', 'created_at')
    readonly_fields = ('created_at', 'views_count', 'sales_count')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'quantity', 'date', 'status')
    search_fields = ('customer__first_name', 'customer__last_name', 'product__name')
    list_filter = ('status', 'date')
    readonly_fields = ('date',)
