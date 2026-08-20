#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from credits.models import CreditConfiguration

config, created = CreditConfiguration.objects.get_or_create(pk=1)
if created:
    config.interest_rate = 15.00
    config.min_installments = 1
    config.max_installments = 24
    config.installment_options = "1,3,6,9,12,18,24"
    config.save()
    sys.stdout.write("Configuracion inicial creada\n")
else:
    sys.stdout.write("Configuracion ya existe\n")

sys.stdout.write(f"Interes: {config.interest_rate}%\n")
sys.stdout.write(f"Cuotas min-max: {config.min_installments}-{config.max_installments}\n")
sys.stdout.write(f"Opciones: {config.installment_options}\n")
