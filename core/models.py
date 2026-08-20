from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CompanyConfiguration(models.Model):
    """Configuración de datos de la empresa"""
    company_name = models.CharField(
        max_length=255,
        default='Tienda Electrodomésticos',
        help_text='Nombre de la empresa'
    )
    phone = models.CharField(
        max_length=20,
        default='595987654321',
        help_text='Número de teléfono principal (ej: 595987654321)'
    )
    whatsapp_number = models.CharField(
        max_length=20,
        default='595987654321',
        help_text='Número de WhatsApp (ej: 595987654321)'
    )
    email = models.EmailField(
        default='info@tienda.com.py',
        help_text='Email de contacto'
    )
    address = models.TextField(
        default='Asunción, Paraguay',
        help_text='Dirección física de la empresa'
    )
    city = models.CharField(
        max_length=100,
        default='Asunción',
        help_text='Ciudad'
    )
    country = models.CharField(
        max_length=100,
        default='Paraguay',
        help_text='País'
    )
    facebook_url = models.URLField(
        blank=True,
        help_text='URL de Facebook'
    )
    instagram_url = models.URLField(
        blank=True,
        help_text='URL de Instagram'
    )
    twitter_url = models.URLField(
        blank=True,
        help_text='URL de Twitter/X'
    )
    youtube_url = models.URLField(
        blank=True,
        help_text='URL de YouTube'
    )
    business_hours = models.CharField(
        max_length=100,
        default='Lun-Vie: 8:00 - 18:00',
        help_text='Horarios de atención'
    )
    shipping_time = models.CharField(
        max_length=100,
        default='2-3 días en Asunción',
        help_text='Tiempo de envío'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuración de Empresa'
        verbose_name_plural = 'Configuración de Empresa'

    def __str__(self):
        return self.company_name

    @classmethod
    def get_config(cls):
        """Obtiene o crea la configuración por defecto"""
        config, _ = cls.objects.get_or_create(pk=1)
        return config
