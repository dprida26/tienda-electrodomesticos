from django.contrib import admin
from .models import Customer, CreditSale, CreditSaleItem, Installment, Payment, CreditConfiguration


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'document_number', 'phone', 'total_credit_debt', 'overdue_count')
    search_fields = ('full_name', 'document_number')
    readonly_fields = ('created_at', 'updated_at')


class CreditSaleItemInline(admin.TabularInline):
    model = CreditSaleItem
    extra = 1


@admin.register(CreditSale)
class CreditSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'installments_count', 'status', 'start_date')
    list_filter = ('status', 'start_date')
    search_fields = ('customer__full_name',)
    inlines = [CreditSaleItemInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('credit_sale', 'number', 'amount', 'due_date', 'status', 'paid_amount', 'pending_amount')
    list_filter = ('status', 'due_date')
    search_fields = ('credit_sale__customer__full_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('installment', 'amount', 'paid_at', 'registered_by')
    list_filter = ('paid_at',)
    search_fields = ('installment__credit_sale__customer__full_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CreditConfiguration)
class CreditConfigurationAdmin(admin.ModelAdmin):
    list_display = ('interest_rate', 'min_installments', 'max_installments', 'updated_at')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('Configuración General', {
            'fields': ('interest_rate', 'min_installments', 'max_installments')
        }),
        ('Opciones de Cuotas', {
            'fields': ('installment_options',),
            'description': 'Ingrese las opciones separadas por coma (ej: 1,3,6,12,24)'
        }),
        ('Información', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not CreditConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
