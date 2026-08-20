#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import CompanyConfiguration

config, created = CompanyConfiguration.objects.get_or_create(pk=1)
if created:
    config.company_name = 'Tienda Electrodomesticos'
    config.phone = '595987654321'
    config.whatsapp_number = '595987654321'
    config.email = 'info@tienda.com.py'
    config.address = 'Asuncion, Paraguay'
    config.city = 'Asuncion'
    config.country = 'Paraguay'
    config.facebook_url = 'https://facebook.com/tienda'
    config.instagram_url = 'https://instagram.com/tienda'
    config.twitter_url = 'https://twitter.com/tienda'
    config.youtube_url = 'https://youtube.com/@tienda'
    config.business_hours = 'Lun-Vie: 8:00 - 18:00'
    config.shipping_time = '2-3 dias en Asuncion'
    config.save()
    sys.stdout.write("Configuracion de empresa creada\n")
else:
    sys.stdout.write("Configuracion de empresa ya existe\n")

sys.stdout.write(f"Empresa: {config.company_name}\n")
sys.stdout.write(f"Telefono: {config.phone}\n")
sys.stdout.write(f"Email: {config.email}\n")
sys.stdout.write(f"Ciudad: {config.city}\n")
