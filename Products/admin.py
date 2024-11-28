from django.contrib import admin
from .models import Category, Product, Size, ProductVariant


class StockFilter(admin.SimpleListFilter):
    title = 'stock'
    parameter_name = 'stock'

    def lookups(self, request, model_admin):
        return [
            ('low', 'Low (0-10)'),
            ('medium', 'Medium (11-50)'),
            ('high', 'High (50+)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(stock__lte=10)
        if self.value() == 'medium':
            return queryset.filter(stock__gt=10, stock__lte=50)
        if self.value() == 'high':
            return queryset.filter(stock__gt=50)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price', 'is_new', 'is_popular')
    list_filter = ('category', 'is_new', 'is_popular')
    prepopulated_fields = {'slug': ('name',)}


class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'stock')
    list_filter = ('product', 'size', StockFilter)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
