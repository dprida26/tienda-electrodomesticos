from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('owner', 'Dueño'),
        ('seller', 'Vendedor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='seller')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
