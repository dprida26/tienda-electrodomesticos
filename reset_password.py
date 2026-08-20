#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

user = CustomUser.objects.filter(username='admin').first()
if user:
    user.set_password('admin123')
    user.save()
    print("Contraseña actualizada: admin123")
else:
    print("Usuario admin no encontrado. Usuarios disponibles:")
    for u in CustomUser.objects.all():
        print(f"  - {u.username}")
