# Fase 2: API REST + Página Web Pública

## Estado Actual

✅ **Completado:**
- Implementación de `ProductCategory` como modelo dinámico
- Migraciones preparadas
- Admin de Django actualizado
- Documentación de uso

## Próximos Pasos

### Fase 2a: API REST con Django REST Framework

**Objetivo:** Exponer datos de productos, categorías e imágenes vía API REST

#### Paso 1: Instalar Django REST Framework

```bash
pip install djangorestframework
```

Agregar a `requirements.txt`:
```
djangorestframework==3.14.0
django-filter==23.3
```

Agregar a `INSTALLED_APPS` en `config/settings.py`:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'inventory',
    'credits',
]
```

#### Paso 2: Crear Serializers

Crear archivo `inventory/serializers.py`:

```python
from rest_framework import serializers
from .models import Product, ProductCategory, ProductImage

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'code', 'name', 'description', 'order')

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'order')

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'brand', 'model', 'description', 
                  'price', 'stock_quantity', 'is_active', 'images')
```

#### Paso 3: Crear ViewSets

Crear archivo `inventory/viewsets.py`:

```python
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer

class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategory.objects.filter(is_active=True)
    serializer_class = ProductCategorySerializer
    pagination_class = None

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'brand', 'model']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['name']
```

#### Paso 4: Crear URLs de API

Crear archivo `api/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.viewsets import ProductViewSet, ProductCategoryViewSet

router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
```

Actualizar `config/urls.py`:
```python
urlpatterns = [
    ...
    path('api/', include('api.urls')),
]
```

#### Paso 5: Probar API

```bash
python manage.py runserver

# Endpoints disponibles:
# GET  /api/v1/categories/
# GET  /api/v1/products/
# GET  /api/v1/products/?category=1
# GET  /api/v1/products/?search=refrigerador
# GET  /api/v1/products/?ordering=-price
```

---

### Fase 2b: Modelo SaleItemImage (para Fase 3)

Agregar modelo para almacenar fotos de artículos de venta:

```python
# En credits/models.py

class SaleItemImage(TimeStampedModel):
    sale_item = models.ForeignKey(CreditSaleItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='sale_items/%Y/%m/%d/')
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order',)
```

---

### Fase 2c: Next.js Web Pública (separa repositorio)

Stack: **Next.js 15 + TypeScript + Tailwind CSS**

**Estructura propuesta:**
```
tienda-web/
├── app/
│   ├── layout.tsx
│   ├── page.tsx              # Inicio
│   ├── catalogo/
│   │   ├── page.tsx          # Listado de productos
│   │   └── [id]/
│   │       └── page.tsx      # Detalle de producto
│   ├── contacto/
│   │   └── page.tsx          # Formulario de contacto
│   └── api/
│       └── products.ts       # Cliente API
├── components/
│   ├── ProductCard.tsx
│   ├── ProductGallery.tsx
│   ├── SearchBar.tsx
│   └── CategoryFilter.tsx
├── lib/
│   └── api.ts                # Funciones para llamar API Django
└── env.local
```

**Primeros endpoints que consumirá:**
- `GET /api/v1/categories/`
- `GET /api/v1/products/`
- `GET /api/v1/products/?category=1`
- `GET /api/v1/products/?search=...`

---

## Timeline Recomendado

| Fase | Tarea | Duración | Prioridad |
|------|-------|----------|-----------|
| 2a   | API REST | 1-2 días | 🔴 ALTA |
| 2b   | SaleItemImage | 1 día | 🟡 MEDIA |
| 2c   | Next.js web | 3-5 días | 🔴 ALTA |
| 3    | Generador contenido | 2-3 días | 🟡 MEDIA |

---

## Notas Técnicas

- **CORS:** Configurar `django-cors-headers` para permitir llamadas desde Next.js
- **Autenticación:** API pública (sin token requerido) para catálogo
- **Imágenes:** Servidas desde Django media files o S3 (configurable)
- **Caché:** Agregar `django-cachalot` para optimizar queries frecuentes
- **Paginación:** DRF paginación estándar (10-20 items por página)

---

## ¿Comenzamos con Fase 2a (API REST)?

Avísame cuando estés listo y comenzamos instalando DRF y creando los serializers.
