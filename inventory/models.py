from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from core.models import TimeStampedModel


class ProductCategory(TimeStampedModel):
    code = models.CharField(max_length=50, unique=True, help_text='Código interno (ej: refrigerator)')
    name = models.CharField(max_length=100, help_text='Nombre a mostrar (ej: Refrigerador)')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text='Orden en listas')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Categoría de Producto'
        verbose_name_plural = 'Categorías de Productos'
        ordering = ('order', 'name')

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products')
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_quantity = models.PositiveIntegerField(default=0)
    min_stock_quantity = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ('name',)
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.name} ({self.brand} {self.model})"

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.min_stock_quantity


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Imagen de Producto'
        verbose_name_plural = 'Imágenes de Productos'
        ordering = ('order',)

    def __str__(self):
        return f"Imagen {self.order} - {self.product.name}"


class StockMovement(TimeStampedModel):
    MOVEMENT_TYPES = [
        ('IN', 'Entrada'),
        ('OUT', 'Salida'),
        ('ADJUSTMENT', 'Ajuste'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    reason = models.TextField(help_text='Descripción de por qué se registra este movimiento')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Movimiento de Stock'
        verbose_name_plural = 'Movimientos de Stock'
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['product', '-created_at']),
        ]

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity} unidades)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.movement_type == 'IN':
            self.product.stock_quantity += self.quantity
        elif self.movement_type == 'OUT':
            self.product.stock_quantity = max(0, self.product.stock_quantity - self.quantity)
        elif self.movement_type == 'ADJUSTMENT':
            self.product.stock_quantity = self.quantity

        self.product.save()
