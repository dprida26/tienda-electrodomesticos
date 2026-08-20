#!/usr/bin/env python
import os
import sys
import django
from django.core.management import call_command

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    print("✓ Django setup complete")
    print("✓ Starting development server on http://localhost:8000/")
    print("✓ API available at http://localhost:8000/api/v1/")
    print("✓ Admin at http://localhost:8000/admin/ (user: admin, password: admin)")
    print("\nPress Ctrl+C to stop server\n")

    call_command('runserver', '0.0.0.0:8000', verbosity=1)
