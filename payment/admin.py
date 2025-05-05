from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import ShippingAddress, Order, OrderItem, Wallet, Transaction


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'Shipping_city', 'Shipping_address1',
                    'Shipping_postal_code')  # تغییر نام فیلدها به حالت CamelCase
    list_display_links = ('id', 'user_link')
    list_filter = ('Shipping_city', 'Shipping_province')
    search_fields = ('Shipping_user__username', 'Shipping_full_name', 'Shipping_postal_code')
    raw_id_fields = ('Shipping_user',)

    fieldsets = (
        (_('اطلاعات کاربر'), {
            'fields': ('Shipping_user', 'Shipping_full_name', 'Shipping_email', 'Shipping_phone_number')
        }),
        (_('آدرس'), {
            'fields': ('Shipping_province', 'Shipping_city', 'Shipping_address1', 'Shipping_postal_code')
        }),
    )

    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.Shipping_user.id])
        return format_html('<a href="{}">{}</a>', url, obj.Shipping_user.username)

    user_link.short_description = _('کاربر')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ('product',)
    readonly_fields = ('total_price',)

    def total_price(self, instance):
        return instance.total_price

    total_price.short_description = _('قیمت کل')


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_link',
        'total_price_formatted',
        'status_display',
        'payment_method_display',
        'is_paid',
        'created_at',
        'order_actions'  # تغییر نام از actions به order_actions
    )
    list_filter = ('status', 'payment_method', 'is_paid', 'created_at')
    search_fields = ('user__username', 'payment_id', 'ref_id')
    raw_id_fields = ('user', 'shipping_address')
    inlines = (OrderItemInline,)
    readonly_fields = ('created_at', 'updated_at', 'payment_details')
    actions = ['mark_as_paid', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_canceled']

    fieldsets = (
        (_('اطلاعات اصلی'), {
            'fields': ('user', 'shipping_address', 'total_price', 'status', 'payment_method')
        }),
        (_('وضعیت پرداخت'), {
            'fields': ('is_paid', 'payment_id', 'ref_id', 'payment_details')
        }),
        (_('تاریخ‌ها'), {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = _('کاربر')

    def total_price_formatted(self, obj):
        return f"{obj.total_price:,} تومان"

    total_price_formatted.short_description = _('مبلغ کل')

    def payment_details(self, obj):
        if obj.payment_id:
            return format_html(
                '<div style="direction: ltr; text-align: left;">'
                '<strong>Payment ID:</strong> {}<br>'
                '<strong>Ref ID:</strong> {}'
                '</div>',
                obj.payment_id,
                obj.ref_id or '---'
            )
        return '---'

    payment_details.short_description = _('جزئیات پرداخت')

    # تغییر نام متد از actions به order_actions
    def order_actions(self, obj):
        links = []
        if obj.status != 'paid':
            links.append(
                f'<a href="{reverse("admin:payment_order_mark_paid", args=[obj.id])}" class="button">تغییر به پرداخت شده</a>'
            )
        if obj.status != 'shipped':
            links.append(
                f'<a href="{reverse("admin:payment_order_mark_shipped", args=[obj.id])}" class="button">تغییر به ارسال شده</a>'
            )
        return format_html(' '.join(links))

    order_actions.short_description = _('اقدامات')
    order_actions.allow_tags = True

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status='paid', is_paid=True)
        self.message_user(request, f'{updated} سفارش با موفقیت به وضعیت پرداخت شده تغییر یافت.')

    mark_as_paid.short_description = _('تغییر وضعیت به پرداخت شده')

    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} سفارش با موفقیت به وضعیت ارسال شده تغییر یافت.')

    mark_as_shipped.short_description = _('تغییر وضعیت به ارسال شده')

    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} سفارش با موفقیت به وضعیت تحویل داده شده تغییر یافت.')

    mark_as_delivered.short_description = _('تغییر وضعیت به تحویل داده شده')

    def mark_as_canceled(self, request, queryset):
        updated = queryset.update(status='canceled')
        self.message_user(request, f'{updated} سفارش با موفقیت به وضعیت لغو شده تغییر یافت.')

    mark_as_canceled.short_description = _('تغییر وضعیت به لغو شده')

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:order_id>/mark-paid/',
                self.admin_site.admin_view(self.mark_paid_view),
                name='payment_order_mark_paid',
            ),
            path(
                '<int:order_id>/mark-shipped/',
                self.admin_site.admin_view(self.mark_shipped_view),
                name='payment_order_mark_shipped',
            ),
        ]
        return custom_urls + urls

    def mark_paid_view(self, request, order_id):
        from django.shortcuts import redirect
        from django.contrib import messages
        order = Order.objects.get(id=order_id)
        order.status = 'paid'
        order.is_paid = True
        order.save()
        messages.success(request, 'وضعیت سفارش با موفقیت به پرداخت شده تغییر یافت.')
        return redirect('admin:payment_order_changelist')

    def mark_shipped_view(self, request, order_id):
        from django.shortcuts import redirect
        from django.contrib import messages
        order = Order.objects.get(id=order_id)
        order.status = 'shipped'
        order.save()
        messages.success(request, 'وضعیت سفارش با موفقیت به ارسال شده تغییر یافت.')
        return redirect('admin:payment_order_changelist')


class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'balance_formatted', 'created_at', 'transactions_link')
    list_display_links = ('id', 'user_link')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = _('کاربر')

    def balance_formatted(self, obj):
        return f"{obj.balance:,} تومان"

    balance_formatted.short_description = _('موجودی')

    def transactions_link(self, obj):
        url = reverse('admin:payment_transaction_changelist') + f'?wallet__id__exact={obj.id}'
        count = obj.transactions.count()
        return format_html('<a href="{}">{} تراکنش</a>', url, count)

    transactions_link.short_description = _('تراکنش‌ها')


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'wallet_link',
        'amount_formatted',
        'transaction_type_display',
        'status_display',
        'created_at',
        'order_link'
    )
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('wallet__user__username', 'payment_id', 'description')
    raw_id_fields = ('wallet', 'order')
    readonly_fields = ('created_at', 'transaction_details')

    fieldsets = (
        (_('اطلاعات اصلی'), {
            'fields': ('wallet', 'order', 'amount', 'transaction_type', 'status')
        }),
        (_('جزئیات'), {
            'fields': ('description', 'payment_id', 'transaction_details')
        }),
        (_('تاریخ‌ها'), {
            'fields': ('created_at',)
        }),
    )

    def wallet_link(self, obj):
        url = reverse('admin:payment_wallet_change', args=[obj.wallet.id])
        return format_html('<a href="{}">{}</a>', url, obj.wallet.user.username)

    wallet_link.short_description = _('کیف پول')

    def order_link(self, obj):
        if obj.order:
            url = reverse('admin:payment_order_change', args=[obj.order.id])
            return format_html('<a href="{}">سفارش #{}</a>', url, obj.order.id)
        return '---'

    order_link.short_description = _('سفارش')

    def amount_formatted(self, obj):
        return f"{obj.amount:,} تومان"

    amount_formatted.short_description = _('مبلغ')

    def transaction_type_display(self, obj):
        return obj.get_transaction_type_display()

    transaction_type_display.short_description = _('نوع تراکنش')

    def status_display(self, obj):
        status_colors = {
            'pending': 'orange',
            'completed': 'green',
            'failed': 'red',
        }
        color = status_colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )

    status_display.short_description = _('وضعیت')

    def transaction_details(self, obj):
        details = []
        if obj.payment_id:
            details.append(f'<strong>شناسه پرداخت:</strong> {obj.payment_id}')
        if obj.description:
            details.append(f'<strong>توضیحات:</strong> {obj.description}')

        if details:
            return format_html('<br>'.join(details))
        return '---'

    transaction_details.short_description = _('جزئیات تراکنش')


admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)