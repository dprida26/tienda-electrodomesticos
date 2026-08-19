from django import forms
from django.forms import inlineformset_factory
from .models import Customer, CreditSale, CreditSaleItem, Payment


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
            'total_amount': forms.NumberInput(attrs={'class': 'form-control price-input', 'step': '0.01', 'min': '0'}),
            'installments_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '60'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class CreditSaleItemForm(forms.ModelForm):
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
            'unit_price': forms.NumberInput(attrs={'class': 'form-control price-input', 'step': '0.01', 'min': '0'}),
        }


CreditSaleItemFormSet = inlineformset_factory(CreditSale, CreditSaleItem, form=CreditSaleItemForm, extra=1)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount', 'paid_at')
        labels = {
            'amount': 'Monto Pagado (Gs.)',
            'paid_at': 'Fecha de Pago',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control price-input', 'step': '0.01', 'min': '0'}),
            'paid_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
