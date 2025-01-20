from django.contrib import admin
from .models import Category, Product


# اکشن سفارشی برای حذف چندین رکورد
@admin.action(description="Delete selected items")
def delete_selected_items(modeladmin, request, queryset):
    queryset.delete()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    actions = [delete_selected_items]  # افزودن اکشن سفارشی


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'star', 'views_count', 'sales_count')
    search_fields = ('name', 'description')
    list_filter = ('category', 'created_at')
    readonly_fields = ('created_at', 'views_count', 'sales_count')
    actions = [delete_selected_items]  # افزودن اکشن سفارشی


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'customer', 'product', 'quantity', 'date', 'status')
#     search_fields = ('customer__first_name', 'customer__last_name', 'product__name')
#     list_filter = ('status', 'date')
#     readonly_fields = ('date',)
#     actions = [delete_selected_items]  # افزودن اکشن سفارشی