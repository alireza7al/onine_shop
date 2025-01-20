from django.contrib import admin
from django.utils.html import format_html
from .models import ShippingAddress, Order, OrderItem


# تابع کمکی برای فرمت‌کردن قیمت‌ها
def format_price(price):
    return "{:,.0f}".format(price)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'formatted_total_price')

    def formatted_total_price(self, obj):
        if obj.quantity is not None and obj.price is not None:
            return format_price(obj.quantity * obj.price)
        return "N/A"

    formatted_total_price.short_description = 'قیمت کل'


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('Shipping_user', 'Shipping_full_name', 'Shipping_city', 'Shipping_address1', 'Shipping_postal_code')
    list_filter = ('Shipping_city', 'Shipping_province')
    search_fields = ('Shipping_user__username', 'Shipping_full_name', 'Shipping_postal_code')
    readonly_fields = ('Shipping_user',)  # فیلد کاربر فقط قابل مشاهده باشد


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shipping_address', 'formatted_total_price', 'is_paid', 'created_at', 'updated_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username', 'id', 'ref_id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    def formatted_total_price(self, obj):
        return format_price(obj.total_price)

    formatted_total_price.short_description = 'قیمت کل'

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

    def formatted_price(self, obj):
        return format_price(obj.price)

    formatted_price.short_description = 'قیمت واحد'

    def formatted_total_price(self, obj):
        if obj.quantity is not None and obj.price is not None:
            return format_price(obj.quantity * obj.price)
        return "N/A"

    formatted_total_price.short_description = 'قیمت کل'
