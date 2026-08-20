from django import forms
from django.forms import inlineformset_factory
from decimal import Decimal
from .models import Customer, CreditSale, CreditSaleItem, Payment


class CurrencyField(forms.DecimalField):
    """Campo decimal que acepta números con separadores de miles (. o ,)"""

    def to_python(self, value):
        if not value:
            return None
        # Convertir a string si es necesario
        value = str(value).strip()
        # Remover espacios
        value = value.replace(' ', '')
        # Si usa punto como separador de miles y coma como decimal (formato europeo)
        if ',' in value and value.rfind(',') > value.rfind('.'):
            value = value.replace('.', '').replace(',', '.')
        # Si usa coma como separador de miles (formato latino)
        elif ',' in value:
            value = value.replace(',', '')
        # Si usa punto como separador de miles y no hay coma
        elif value.count('.') > 1:
            value = value.replace('.', '')
        # Limpiar punto final si quedó
        value = value.strip('.')
        return super().to_python(value)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('full_name', 'document_number', 'phone', 'address')
        labels = {
            'full_name': 'Nombre Completo',
            'document_number': 'Número de Documento',
            'phone': 'Teléfono',
            'address': 'Dirección',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CreditSaleForm(forms.ModelForm):
    total_amount = CurrencyField(
        label='Monto Total (Gs.)',
        decimal_places=2,
        max_digits=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control price-input',
            'placeholder': 'ej: 1.500.000 o 1500000',
            'inputmode': 'numeric'
        })
    )

    class Meta:
        model = CreditSale
        fields = ('customer', 'total_amount', 'installments_count', 'start_date', 'status')
        labels = {
            'customer': 'Cliente',
            'total_amount': 'Monto Total (Gs.)',
            'installments_count': 'Cantidad de Cuotas',
            'start_date': 'Fecha de Inicio',
            'status': 'Estado',
        }
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'installments_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '60'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class CreditSaleItemForm(forms.ModelForm):
    unit_price = CurrencyField(
        label='Precio Unitario (Gs.)',
        decimal_places=2,
        max_digits=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control price-input',
            'placeholder': 'ej: 1.500.000 o 1500000',
            'inputmode': 'numeric'
        })
    )

    class Meta:
        model = CreditSaleItem
        fields = ('product', 'quantity', 'unit_price')
        labels = {
            'product': 'Producto',
            'quantity': 'Cantidad',
            'unit_price': 'Precio Unitario (Gs.)',
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }


CreditSaleItemFormSet = inlineformset_factory(CreditSale, CreditSaleItem, form=CreditSaleItemForm, extra=1)


class PaymentForm(forms.ModelForm):
    amount = CurrencyField(
        label='Monto Pagado (Gs.)',
        decimal_places=2,
        max_digits=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control price-input',
            'placeholder': 'ej: 500.000 o 500000',
            'inputmode': 'numeric'
        })
    )

    class Meta:
        model = Payment
        fields = ('amount', 'paid_at')
        labels = {
            'amount': 'Monto Pagado (Gs.)',
            'paid_at': 'Fecha de Pago',
        }
        widgets = {
            'paid_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
