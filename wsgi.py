import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"\n{'='*80}")
print(f"WSGI STARTUP - DATABASE_URL present: {bool(DATABASE_URL)}")
if DATABASE_URL:
    print(f"DATABASE_URL starts with: {DATABASE_URL[:50]}...")
print(f"{'='*80}\n")

sys.path.insert(0, str(BASE_DIR))

from config.wsgi import application

__all__ = ['application']
