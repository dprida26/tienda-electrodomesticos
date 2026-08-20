from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.viewsets import ProductViewSet, ProductCategoryViewSet
from credits.views import CreditConfigurationAPIView
from core.views import CompanyConfigurationAPIView

router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet, basename='api-category')
router.register(r'products', ProductViewSet, basename='api-product')

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/credit-config/', CreditConfigurationAPIView.as_view(), name='credit-config'),
    path('v1/company-config/', CompanyConfigurationAPIView.as_view(), name='company-config'),
]
