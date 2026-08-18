from django import forms
from .models import Product, StockMovement, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'brand', 'model', 'description', 'price', 'stock_quantity', 'min_stock_quantity', 'is_active')
        labels = {
            'name': 'Nombre del Producto',
            'category': 'Categoría',
            'brand': 'Marca',
            'model': 'Modelo',
            'description': 'Descripción',
            'price': 'Precio ($)',
            'stock_quantity': 'Stock Actual',
            'min_stock_quantity': 'Stock Mínimo',
            'is_active': 'Activo',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'min_stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
