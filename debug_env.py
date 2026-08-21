#!/usr/bin/env python
import os
import sys

print("\n" + "="*80)
print("ENVIRONMENT DEBUG - Before Django loads")
print("="*80)

print(f"\nRENDER variable: {os.environ.get('RENDER', 'NOT SET')}")
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'NOT SET')}")
print(f"SECRET_KEY: {'SET' if os.environ.get('SECRET_KEY') else 'NOT SET'}")
print(f"DEBUG: {os.environ.get('DEBUG', 'NOT SET')}")

if os.environ.get('DATABASE_URL'):
    db_url = os.environ.get('DATABASE_URL')
    print(f"\n✓ DATABASE_URL found!")
    print(f"  First 60 chars: {db_url[:60]}")
    print(f"  Looks like PostgreSQL: {'postgresql://' in db_url}")
else:
    print(f"\n✗ DATABASE_URL NOT found in os.environ")
    print(f"  Available keys: {list(os.environ.keys())[:10]}")

print("="*80 + "\n")

# Exit if critical vars missing
if not os.environ.get('DATABASE_URL'):
    print("WARNING: DATABASE_URL is missing!")

sys.exit(0)
