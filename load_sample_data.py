#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

# Fix encoding on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventory.models import ProductCategory, Product, ProductImage
from django.core.files.base import ContentFile

# Crear categorías
categories_data = [
    {'code': 'refrigerator', 'name': 'Refrigerador', 'order': 1},
    {'code': 'washer', 'name': 'Lavadora', 'order': 2},
    {'code': 'stove', 'name': 'Estufa', 'order': 3},
    {'code': 'microwave', 'name': 'Microonda', 'order': 4},
    {'code': 'tv', 'name': 'Televisor', 'order': 5},
    {'code': 'air_conditioner', 'name': 'Aire Acondicionado', 'order': 6},
]

print("Creando categorías...")
for cat_data in categories_data:
    category, created = ProductCategory.objects.get_or_create(
        code=cat_data['code'],
        defaults={'name': cat_data['name'], 'order': cat_data['order']}
    )
    if created:
        print(f"✓ Categoría creada: {category.name}")
    else:
        print(f"✓ Categoría ya existe: {category.name}")

# Crear productos
products_data = [
    {
        'name': 'Refrigerador Samsung 500L',
        'category': 'refrigerator',
        'brand': 'Samsung',
        'model': 'RS25R5011SR',
        'description': 'Refrigerador de última generación con tecnología inverter',
        'price': 1500000,
        'stock': 5,
    },
    {
        'name': 'Refrigerador LG 450L',
        'category': 'refrigerator',
        'brand': 'LG',
        'model': 'GB440PLHL',
        'description': 'Refrigerador con compresor inverter y ahorro de energía',
        'price': 1200000,
        'stock': 8,
    },
    {
        'name': 'Lavadora Samsung 8kg',
        'category': 'washer',
        'brand': 'Samsung',
        'model': 'WA80M5110XM',
        'description': 'Lavadora automática de carga frontal',
        'price': 800000,
        'stock': 3,
    },
    {
        'name': 'Estufa Bosch 4 hornillas',
        'category': 'stove',
        'brand': 'Bosch',
        'model': 'HCS5E6S0',
        'description': 'Estufa eléctrica de 4 hornillas con horno',
        'price': 950000,
        'stock': 2,
    },
    {
        'name': 'Microonda LG 25L',
        'category': 'microwave',
        'brand': 'LG',
        'model': 'MS2055LO',
        'description': 'Microonda con grill y funciones variadas',
        'price': 350000,
        'stock': 10,
    },
    {
        'name': 'Televisor Samsung 55" 4K',
        'category': 'tv',
        'brand': 'Samsung',
        'model': 'UN55TU8000FXZA',
        'description': 'Smart TV 4K Ultra HD con procesador dinámico',
        'price': 2200000,
        'stock': 4,
    },
    {
        'name': 'Aire Acondicionado LG 18000 BTU',
        'category': 'air_conditioner',
        'brand': 'LG',
        'model': 'LS180BSBA',
        'description': 'Aire acondicionado inverter de bajo consumo',
        'price': 1800000,
        'stock': 6,
    },
]

print("\nCreando productos...")
for prod_data in products_data:
    category = ProductCategory.objects.get(code=prod_data.pop('category'))
    stock = prod_data.pop('stock')

    product, created = Product.objects.get_or_create(
        name=prod_data['name'],
        defaults={
            **prod_data,
            'category': category,
        }
    )

    if created:
        product.stock_quantity = stock
        product.save()
        print(f"✓ Producto creado: {product.name} (Gs. {product.price:,})")
    else:
        print(f"✓ Producto ya existe: {product.name}")

print("\n✓ Datos de prueba cargados exitosamente")
print("\nAccede a:")
print("  - API: http://localhost:8000/api/v1/")
print("  - Admin: http://localhost:8000/admin/")
print("  - Categorías: http://localhost:8000/api/v1/categories/")
print("  - Productos: http://localhost:8000/api/v1/products/")
