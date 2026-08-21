import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Gunicorn configuration
bind = '0.0.0.0:10000'
workers = 2
worker_class = 'sync'
timeout = 60
keepalive = 5
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'tienda-electrodomesticos'
