from django.contrib import admin
from .models import Product, ProductImage, StockMovement, ProductCategory


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    fieldsets = (
        ('Información', {
            'fields': ('code', 'name', 'description', 'order', 'is_active')
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'model', 'price', 'stock_quantity', 'min_stock_quantity', 'is_active', 'is_low_stock')
    list_filter = ('category', 'is_active', 'brand')
    search_fields = ('name', 'brand', 'model')
    inlines = [ProductImageInline]
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'category', 'brand', 'model', 'description', 'price')
        }),
        ('Stock', {
            'fields': ('stock_quantity', 'min_stock_quantity')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
    )

    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Bajo Stock'


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'user', 'created_at')
    list_filter = ('movement_type', 'created_at', 'product__category')
    search_fields = ('product__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'user')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)
