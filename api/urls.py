from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.viewsets import ProductViewSet, ProductCategoryViewSet

router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet, basename='api-category')
router.register(r'products', ProductViewSet, basename='api-product')

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
]
