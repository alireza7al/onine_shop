from django.contrib import admin
from .models import Category, Product, Comment

# اکشن سفارشی برای حذف چندین رکورد
@admin.action(description="Delete selected items")
def delete_selected_items(modeladmin, request, queryset):
    queryset.delete()

# اکشن سفارشی برای تایید کامنت‌ها
@admin.action(description="Approve selected comments")
def approve_comments(modeladmin, request, queryset):
    queryset.update(approved_comment=True)

# اکشن سفارشی برای رد کامنت‌ها
@admin.action(description="Reject selected comments")
def reject_comments(modeladmin, request, queryset):
    queryset.update(approved_comment=False)

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

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'text', 'created_date', 'approved_comment')
    list_display_links = ('user', 'product')
    search_fields = ('user__username', 'product__name', 'text')
    list_filter = ('approved_comment', 'created_date')
    date_hierarchy = 'created_date'
    actions = [delete_selected_items, approve_comments, reject_comments]

    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('user', 'product', 'text')
        }),
        ('وضعیت', {
            'fields': ('approved_comment', 'created_date')
        }),
    )