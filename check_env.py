#!/usr/bin/env python
import os
import sys

print("=== ENVIRONMENT VARIABLES CHECK ===")
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'NOT SET')}")
print(f"DEBUG: {os.environ.get('DEBUG', 'NOT SET')}")
print(f"SECRET_KEY: {'SET' if os.environ.get('SECRET_KEY') else 'NOT SET'}")
print(f"ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS', 'NOT SET')}")
print(f"NODE_ENV/ENVIRONMENT: {os.environ.get('ENVIRONMENT', 'NOT SET')}")
print("====================================")

if not os.environ.get('DATABASE_URL'):
    print("ERROR: DATABASE_URL no está configurada en el entorno!")
    sys.exit(1)

print("✓ DATABASE_URL está configurada correctamente")
