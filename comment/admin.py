from django.contrib import admin
from .models import Comment

# اکشن سفارشی برای تایید کامنت‌ها
@admin.action(description="Approve selected comments")
def approve_comments(modeladmin, request, queryset):
    queryset.update(approved_comment=True)

# اکشن سفارشی برای رد کامنت‌ها
@admin.action(description="Reject selected comments")
def reject_comments(modeladmin, request, queryset):
    queryset.update(approved_comment=False)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'text', 'created_date', 'approved_comment', 'likes', 'dislikes', 'reports', 'rating')
    list_display_links = ('user', 'product')
    search_fields = ('user__username', 'product__name', 'text')
    list_filter = ('approved_comment', 'created_date')
    date_hierarchy = 'created_date'
    actions = [approve_comments, reject_comments]

    fieldsets = (
        ('اطلاعات پایه', {
            'fields': ('user', 'product', 'text', 'parent')
        }),
        ('وضعیت', {
            'fields': ('approved_comment', 'created_date')
        }),
        ('تعاملات', {
            'fields': ('likes', 'dislikes', 'reports', 'rating')
        }),
    )