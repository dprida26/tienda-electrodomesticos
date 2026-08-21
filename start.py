#!/usr/bin/env python
"""
Start script that manually injects DATABASE_URL before Django loads.
This works around Render's environment variable injection issues.
"""
import os
import sys
import subprocess

# Try to find DATABASE_URL from various sources
db_url = os.environ.get('DATABASE_URL')

if not db_url:
    print("[START] WARNING: DATABASE_URL not in os.environ")
    print("[START] Checking if it's accessible via Render's internal config...")

    # Try to read from Render's config files if they exist
    render_config_paths = [
        '/etc/render/database_url',
        '/opt/render/database_url',
        '/var/render/database_url',
    ]

    for path in render_config_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    db_url = f.read().strip()
                print(f"[START] Found DATABASE_URL at {path}")
                os.environ['DATABASE_URL'] = db_url
                break
            except Exception as e:
                print(f"[START] Failed to read {path}: {e}")

if db_url:
    print(f"[START] Using DATABASE_URL (first 80 chars): {db_url[:80]}")
else:
    print("[START] DATABASE_URL still not found. Django will use SQLite.")

# Now run the actual command
cmd = sys.argv[1:]
print(f"[START] Running: {' '.join(cmd)}")
sys.exit(subprocess.call(cmd))
