import os
import sys
from pathlib import Path
import environ
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

is_render = 'RENDER' in os.environ
db_url_env = os.environ.get('DATABASE_URL')
is_production = os.environ.get('ENVIRONMENT') == 'production' or is_render or bool(db_url_env)

# DEBUG: Write environment variables IMMEDIATELY and to stderr
sys.stderr.write("\n" + "="*100 + "\n")
sys.stderr.write("DJANGO STARTUP - CRITICAL DEBUG INFO\n")
sys.stderr.write("="*100 + "\n")
sys.stderr.write(f"DATABASE_URL in os.environ: {bool(db_url_env)}\n")
sys.stderr.write(f"RENDER in os.environ: {bool(os.environ.get('RENDER'))}\n")
sys.stderr.write(f"is_render: {is_render}\n")
sys.stderr.write(f"is_production: {is_production}\n")

if db_url_env:
    sys.stderr.write(f"DATABASE_URL (first 80 chars): {db_url_env[:80]}\n")
else:
    sys.stderr.write("WARNING: DATABASE_URL is NOT SET in os.environ!\n")
    sys.stderr.write(f"Available env keys count: {len(os.environ.keys())}\n")
sys.stderr.write("="*100 + "\n\n")
sys.stderr.flush()

# Also write to file for inspection
debug_log_path = os.path.join(BASE_DIR, 'django_startup_debug.log')
try:
    with open(debug_log_path, 'w') as f:
        f.write("="*100 + "\n")
        f.write(f"DJANGO STARTUP - All Environment Variables\n")
        f.write("="*100 + "\n")
        for key in sorted(os.environ.keys()):
            value = os.environ[key]
            if 'SECRET' in key or 'PASSWORD' in key or 'KEY' in key:
                f.write(f"  {key}: ***REDACTED***\n")
            else:
                if len(value) > 100:
                    f.write(f"  {key}: {value[:100]}...\n")
                else:
                    f.write(f"  {key}: {value}\n")
        f.write("="*100 + "\n")
        f.write(f"DATABASE_URL present: {bool(os.environ.get('DATABASE_URL'))}\n")
        f.write(f"is_render: {is_render}\n")
        f.write(f"is_production: {is_production}\n")
        f.write("="*100 + "\n")
except Exception as e:
    sys.stderr.write(f"Failed to write debug log: {e}\n")
    sys.stderr.flush()

# CRITICAL: Never read .env if DATABASE_URL is already set (production/Render)
env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file) and not is_production:
    environ.Env.read_env(env_file)
    print(f"[Django] Loaded .env from {env_file}")
else:
    print(f"[Django] Skipping .env: is_production={is_production}")

env = environ.Env(
    DEBUG=(bool, False)
)

SECRET_KEY = env('SECRET_KEY', default='dev-insecure-key')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'core',
    'accounts',
    'inventory',
    'credits',
    'reports',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database configuration
db_url = os.environ.get('DATABASE_URL')

print(f"\n{'='*80}")
print(f"DATABASE CONFIGURATION DEBUG")
print(f"is_render: {is_render}")
print(f"is_production: {is_production}")
print(f"DATABASE_URL in os.environ: {bool(db_url)}")
if db_url:
    print(f"DATABASE_URL (first 80 chars): {db_url[:80]}")
print(f"{'='*80}\n")

if db_url:
    # Use dj-database-url to parse the PostgreSQL URL
    try:
        DATABASES = {'default': dj_database_url.config(conn_max_age=600, conn_health_checks=True)}
        print("[DB] Using PostgreSQL from DATABASE_URL via dj-database-url")
    except Exception as e:
        print(f"[DB ERROR] Failed to parse DATABASE_URL: {e}")
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }
else:
    # Fallback to SQLite (this happens on Render when DATABASE_URL is not injected)
    print("[DB] DATABASE_URL not found, using SQLite as fallback")
    print("[DB] NOTE: This is likely Render not injecting DATABASE_URL. Check dashboard Environment vars.")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-py'
TIME_ZONE = 'America/Asuncion'
USE_I18N = True
USE_TZ = True
USE_L10N = True

# Formato de números y moneda para Paraguay (Guaraní)
NUMBER_FORMAT = '#,##0.##'
DECIMAL_SEPARATOR = ','
THOUSANDS_SEPARATOR = '.'
CURRENCY_SYMBOL = 'Gs.'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS es opcional si no tienes archivos estáticos adicionales
if os.path.exists(os.path.join(BASE_DIR, 'static')):
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# CORS Configuration - permitir Next.js y localhost
CORS_ALLOWED_ORIGINS = env('CORS_ALLOWED_ORIGINS', default='http://localhost:3000,http://localhost:3001,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:3001,http://127.0.0.1:8000').split(',')

CORS_ALLOW_CREDENTIALS = True

# Security settings for production
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT', default=not DEBUG)
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE', default=not DEBUG)
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', default=not DEBUG)
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
