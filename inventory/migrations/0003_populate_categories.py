# Populate initial categories

from django.db import migrations


def create_initial_categories(apps, schema_editor):
    ProductCategory = apps.get_model('inventory', 'ProductCategory')

    categories = [
        {'code': 'refrigerator', 'name': 'Refrigerador', 'order': 1},
        {'code': 'oven', 'name': 'Horno', 'order': 2},
        {'code': 'washer', 'name': 'Lavadora', 'order': 3},
        {'code': 'dryer', 'name': 'Secadora', 'order': 4},
        {'code': 'dishwasher', 'name': 'Lava Platos', 'order': 5},
        {'code': 'microwave', 'name': 'Microondas', 'order': 6},
        {'code': 'furniture', 'name': 'Muebles', 'order': 7},
        {'code': 'other', 'name': 'Otro', 'order': 8},
    ]

    for cat in categories:
        ProductCategory.objects.get_or_create(
            code=cat['code'],
            defaults={'name': cat['name'], 'order': cat['order'], 'is_active': True}
        )


def reverse_categories(apps, schema_editor):
    ProductCategory = apps.get_model('inventory', 'ProductCategory')
    ProductCategory.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_productcategory_alter_product_category'),
    ]

    operations = [
        migrations.RunPython(create_initial_categories, reverse_categories),
    ]
