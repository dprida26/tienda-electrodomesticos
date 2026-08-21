from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import HttpResponse
from core.views import dashboard
import os
from pathlib import Path

def debug_env_view(request):
    """Return the debug environment log file"""
    log_path = os.path.join(Path(__file__).resolve().parent.parent, 'django_startup_debug.log')
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/plain')
    return HttpResponse("Debug log not found", status=404)

urlpatterns = [
    path('debug/env/', debug_env_view, name='debug_env'),
    path('', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('accounts/', include('accounts.urls')),
    path('inventory/', include('inventory.urls')),
    path('credits/', include('credits.urls')),
    path('reports/', include('reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
