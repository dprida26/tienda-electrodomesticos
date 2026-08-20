from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter, NumberFilter
from .models import Product, ProductCategory
from .serializers import ProductCategorySerializer, ProductListSerializer, ProductDetailSerializer


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategory.objects.filter(is_active=True)
    serializer_class = ProductCategorySerializer
    pagination_class = None
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'name']
    ordering = ['order']


class ProductFilter(FilterSet):
    category_id = NumberFilter(field_name='category', label='Categoría')
    price_min = NumberFilter(field_name='price', lookup_expr='gte', label='Precio mínimo')
    price_max = NumberFilter(field_name='price', lookup_expr='lte', label='Precio máximo')
    brand = CharFilter(field_name='brand', lookup_expr='icontains', label='Marca')

    class Meta:
        model = Product
        fields = ['category_id', 'is_active', 'is_on_sale', 'price_min', 'price_max', 'brand']


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'brand', 'model', 'description']
    ordering_fields = ['name', 'price', 'created_at', 'stock_quantity']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
