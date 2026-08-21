from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from core.views import dashboard

urlpatterns = [
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
