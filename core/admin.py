from django.contrib import admin
from .models import CompanyConfiguration


@admin.register(CompanyConfiguration)
class CompanyConfigurationAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone', 'email', 'city', 'updated_at')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('company_name', 'phone', 'email', 'city', 'country', 'address')
        }),
        ('Contacto WhatsApp', {
            'fields': ('whatsapp_number',),
            'description': 'Número de WhatsApp para contactos'
        }),
        ('Redes Sociales', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
        ('Información de Servicio', {
            'fields': ('business_hours', 'shipping_time'),
            'classes': ('collapse',)
        }),
        ('Información', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not CompanyConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
