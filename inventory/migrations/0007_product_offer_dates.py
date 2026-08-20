# Generated migration for adding offer start and end dates

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_product_is_on_sale_product_sale_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer_start_date',
            field=models.DateTimeField(blank=True, help_text='Fecha y hora de inicio de la oferta', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='offer_end_date',
            field=models.DateTimeField(blank=True, help_text='Fecha y hora de fin de la oferta', null=True),
        ),
    ]
