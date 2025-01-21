from django.contrib import admin
from django.utils.html import format_html
from .models import ShippingAddress, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'formatted_price', 'formatted_total_price')

    @admin.display(description='قیمت واحد')
    def formatted_price(self, obj):
        if obj.price is not None:
            return f"{obj.price:,}"
        return "0"

    @admin.display(description='قیمت کل')
    def formatted_total_price(self, obj):
        if obj.total_price is not None:
            return f"{obj.total_price:,}"
        return "0"


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('Shipping_user', 'Shipping_full_name', 'Shipping_city', 'Shipping_address1', 'Shipping_postal_code')
    list_filter = ('Shipping_city', 'Shipping_province')
    search_fields = ('Shipping_user__username', 'Shipping_full_name', 'Shipping_postal_code')
    readonly_fields = ('Shipping_user',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shipping_address', 'formatted_total_price', 'is_paid', 'created_at', 'updated_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username', 'id', 'ref_id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    @admin.display(description='قیمت کل')
    def formatted_total_price(self, obj):
        if obj.total_price is not None:
            return f"{obj.total_price:,}"
        return "0"  # یا هر مقدار پیش‌فرض دیگر

    # اکشن‌های سفارشی برای تغییر وضعیت پرداخت
    actions = ['mark_as_paid', 'mark_as_unpaid']

    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True)

    mark_as_paid.short_description = "علامت‌گذاری به‌عنوان پرداخت شده"

    def mark_as_unpaid(self, request, queryset):
        queryset.update(is_paid=False)

    mark_as_unpaid.short_description = "علامت‌گذاری به‌عنوان پرداخت نشده"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'formatted_price', 'formatted_total_price')
    list_filter = ('order__is_paid',)
    search_fields = ('order__id', 'product__name')

    @admin.display(description='قیمت واحد')
    def formatted_price(self, obj):
        if obj.price is not None:
            return f"{obj.price:,}"
        return "0"  # یا هر مقدار پیش‌فرض دیگر

    @admin.display(description='قیمت کل')
    def formatted_total_price(self, obj):
        if obj.total_price is not None:
            return f"{obj.total_price:,}"
        return "0"  # یا هر مقدار پیش‌فرض دیگر