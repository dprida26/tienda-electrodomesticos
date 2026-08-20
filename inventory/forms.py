from django import forms
from decimal import Decimal, InvalidOperation
from .models import Product, StockMovement, ProductImage, ProductCategory


class DecimalFieldWithDotSeparator(forms.DecimalField):
    def to_python(self, value):
        if value is None or value == '':
            return None
        value = str(value).strip()
        # Si tiene coma, es formato local (2.800.000,00) -> convertir a 2800000.00
        if ',' in value:
            value = value.replace('.', '').replace(',', '.')
        # Si no tiene coma, dejar como está (puede ser 15.00 o 1000000)
        return super().to_python(value)


class ProductForm(forms.ModelForm):
    price = DecimalFieldWithDotSeparator(
        max_digits=15,
        decimal_places=2,
        widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'ej: 1000000', 'inputmode': 'decimal'}),
        label='Precio al Contado (Gs.)',
    )
    installment_interest_rate = DecimalFieldWithDotSeparator(
        max_digits=5,
        decimal_places=2,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: 15', 'inputmode': 'decimal'}),
        label='Interés para Cuotas (%)',
    )
    sale_price = DecimalFieldWithDotSeparator(
        max_digits=15,
        decimal_places=2,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control price-input', 'placeholder': 'ej: 1500000', 'inputmode': 'decimal'}),
        label='Precio de Oferta (Gs.)',
    )

    class Meta:
        model = Product
        fields = ('name', 'category', 'brand', 'model', 'description', 'price', 'installment_interest_rate', 'installment_options', 'stock_quantity', 'min_stock_quantity', 'is_active', 'is_on_sale', 'sale_price', 'offer_start_date', 'offer_end_date')
        labels = {
            'name': 'Nombre del Producto',
            'category': 'Categoría',
            'brand': 'Marca',
            'model': 'Modelo',
            'description': 'Descripción',
            'installment_options': 'Opciones de Cuotas',
            'stock_quantity': 'Stock Actual',
            'min_stock_quantity': 'Stock Mínimo',
            'is_active': 'Activo',
            'is_on_sale': 'En Oferta',
            'sale_price': 'Precio de Oferta (Gs.)',
            'offer_start_date': 'Inicio de Oferta',
            'offer_end_date': 'Fin de Oferta',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'installment_options': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: 1,3,6,9,12,18,24'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'min_stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_on_sale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'offer_start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'offer_end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ('product', 'movement_type', 'quantity', 'reason')
        labels = {
            'product': 'Producto',
            'movement_type': 'Tipo de Movimiento',
            'quantity': 'Cantidad',
            'reason': 'Motivo/Razón',
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'movement_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ej: Entrada de compra #123, Venta a cliente X, etc.'}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image', 'order')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
