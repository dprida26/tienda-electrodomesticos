from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils import timezone
from core.models import TimeStampedModel
from inventory.models import Product


class Customer(TimeStampedModel):
    full_name = models.CharField(max_length=255)
    document_number = models.CharField(max_length=50, unique=True, help_text='DNI, CUIT, etc.')
    phone = models.CharField(max_length=20)
    address = models.TextField()

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ('full_name',)
        indexes = [
            models.Index(fields=['document_number']),
            models.Index(fields=['full_name']),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.document_number})"

    @property
    def total_credit_debt(self):
        return sum(
            sale.pending_amount
            for sale in self.credit_sales.filter(status='ACTIVE')
        )

    @property
    def overdue_count(self):
        from django.db.models import Q
        return Installment.objects.filter(
            credit_sale__customer=self,
            status='PENDING',
            due_date__lt=timezone.now().date()
        ).count()


class CreditSale(TimeStampedModel):
    STATUS_CHOICES = [
        ('ACTIVE', 'Activa'),
        ('PAID', 'Pagada'),
        ('CANCELLED', 'Cancelada'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='credit_sales')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    installments_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Venta a Crédito'
        verbose_name_plural = 'Ventas a Crédito'
        ordering = ('-start_date',)
        indexes = [
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['start_date']),
        ]

    def __str__(self):
        return f"Venta #{self.id} - {self.customer.full_name}"

    @property
    def pending_amount(self):
        paid = self.installments.filter(status='PAID').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        return self.total_amount - paid

    def get_overdue_installments(self):
        return self.installments.filter(status='PENDING', due_date__lt=timezone.now().date())


class CreditSaleItem(models.Model):
    credit_sale = models.ForeignKey(CreditSale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Ítem de Venta'
        verbose_name_plural = 'Ítems de Venta'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.unit_price


class Installment(TimeStampedModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('PAID', 'Pagada'),
        ('OVERDUE', 'Vencida'),
    ]

    credit_sale = models.ForeignKey(CreditSale, on_delete=models.CASCADE, related_name='installments')
    number = models.PositiveIntegerField(help_text='Número de cuota (1, 2, 3...)')
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'
        ordering = ('credit_sale', 'number')
        unique_together = ('credit_sale', 'number')
        indexes = [
            models.Index(fields=['status', 'due_date']),
            models.Index(fields=['credit_sale', 'status']),
        ]

    def __str__(self):
        return f"Cuota {self.number}/{self.credit_sale.installments_count} - {self.credit_sale.customer.full_name}"

    def save(self, *args, **kwargs):
        if self.status == 'PENDING' and self.due_date < timezone.now().date():
            self.status = 'OVERDUE'
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        return self.status == 'PENDING' and self.due_date < timezone.now().date()

    @property
    def paid_amount(self):
        return self.payments.aggregate(total=models.Sum('amount'))['total'] or 0

    @property
    def pending_amount(self):
        return self.amount - self.paid_amount


class Payment(TimeStampedModel):
    installment = models.ForeignKey(Installment, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    paid_at = models.DateField()
    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ('paid_at',)
        indexes = [
            models.Index(fields=['installment', 'paid_at']),
        ]

    def __str__(self):
        return f"Pago de ${self.amount} - {self.installment}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_installment_status()

    def _update_installment_status(self):
        if self.installment.paid_amount >= self.installment.amount:
            self.installment.status = 'PAID'
            self.installment.save()
