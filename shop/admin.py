from django.contrib import admin
from .models import Category, Product

# اکشن سفارشی برای حذف چندین رکورد
@admin.action(description="حذف موارد انتخاب‌شده")
def delete_selected_items(modeladmin, request, queryset):
    queryset.delete()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')  # فقط فیلدهای موجود در مدل
    search_fields = ('name',)
    actions = [delete_selected_items]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'star', 'views_count', 'sales_count', 'is_sale', 'created_at')
    list_display_links = ('name', 'category')
    search_fields = ('name', 'description')
    list_filter = ('category', 'is_sale', 'created_at')
    readonly_fields = ('created_at', 'views_count', 'sales_count')
    date_hierarchy = 'created_at'
    actions = [delete_selected_items]

    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('name', 'category', 'description', 'price', 'star', 'image')
        }),
        ('تخفیف', {
            'fields': ('is_sale', 'sale_price')
        }),
        ('آمار', {
            'fields': ('views_count', 'sales_count')
        }),
        ('تاریخ ایجاد', {
            'fields': ('created_at',)
        }),
    )