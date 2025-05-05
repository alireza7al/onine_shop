from django.contrib import admin
from django.utils.html import format_html
from .models import Comment

# اکشن‌های سفارشی
@admin.action(description="تایید کامنت‌های انتخاب شده")
def approve_comments(modeladmin, request, queryset):
    queryset.update(approved_comment=True)

@admin.action(description="رد کامنت‌های انتخاب شده")
def reject_comments(modeladmin, request, queryset):
    queryset.update(approved_comment=False)

@admin.action(description="حذف کامنت‌های انتخاب شده")
def delete_comments(modeladmin, request, queryset):
    queryset.delete()

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # تنظیمات نمایش لیست
    list_display = (
        'get_user_info',
        'get_product_info',
        'truncated_text',
        'formatted_created_date',
        'approval_status',
        'like_dislike_display'  # تغییر نام به تابع نمایش جدید
    )
    list_display_links = ('get_user_info', 'get_product_info')
    search_fields = ('user__username', 'product__name', 'text')
    list_filter = (
        'approved_comment',
        ('created_date', admin.DateFieldListFilter),
    )
    date_hierarchy = 'created_date'
    list_per_page = 20
    actions = [approve_comments, reject_comments, delete_comments]
    readonly_fields = ('created_date', 'likes', 'dislikes')

    # گروه‌بندی فیلدها در صفحه ویرایش
    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('user', 'product', 'parent', 'text'),
        }),
        ('وضعیت تایید', {
            'fields': ('approved_comment',),
            'classes': ('collapse',),
        }),
        ('تعاملات کاربران', {
            'fields': ('likes', 'dislikes'),
            'classes': ('collapse',),
        }),
        ('اطلاعات زمانی', {
            'fields': ('created_date',),
            'classes': ('collapse',),
        }),
    )

    # متدهای کمکی برای نمایش بهتر اطلاعات
    @admin.display(description='کاربر')
    def get_user_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            obj.user.username,
            obj.user.email
        )

    @admin.display(description='محصول')
    def get_product_info(self, obj):
        return obj.product.name

    @admin.display(description='متن خلاصه')
    def truncated_text(self, obj):
        return format_html(
            '<span title="{}">{}...</span>',
            obj.text,
            obj.text[:50]
        )

    @admin.display(description='تاریخ', ordering='created_date')
    def formatted_created_date(self, obj):
        return obj.created_date.strftime("%Y-%m-%d %H:%M")

    @admin.display(description='وضعیت', boolean=True)
    def approval_status(self, obj):
        return obj.approved_comment

    @admin.display(description='تعاملات')
    def like_dislike_display(self, obj):
        return format_html(
            '<div style="display: flex; gap: 10px; align-items: center;">'
            '<div style="color: green;">👍 {}</div>'
            '<div style="color: red;">👎 {}</div>'
            '</div>',
            obj.likes,
            obj.dislikes
        )

    # سفارشی‌سازی ظاهر
    empty_value_display = '-'
    list_select_related = ('user', 'product')
    save_on_top = True