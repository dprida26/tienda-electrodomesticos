# Documentación API REST - Fase 2a

## Base URL

```
http://localhost:8000/api/v1/
```

## Endpoints

### 1. Categorías de Productos

#### GET `/api/v1/categories/`

Lista todas las categorías activas.

**Parámetros de query:**
- `ordering`: `order`, `name`, `-order`, `-name` (ordenamiento)
- `search`: buscar por nombre

**Ejemplo:**
```bash
curl "http://localhost:8000/api/v1/categories/"
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "code": "refrigerator",
    "name": "Refrigerador",
    "description": "",
    "order": 1,
    "is_active": true,
    "product_count": 5
  },
  {
    "id": 2,
    "code": "oven",
    "name": "Horno",
    "description": "",
    "order": 2,
    "is_active": true,
    "product_count": 3
  }
]
```

---

#### GET `/api/v1/categories/{id}/`

Obtener detalle de una categoría específica.

**Ejemplo:**
```bash
curl "http://localhost:8000/api/v1/categories/1/"
```

**Respuesta:**
```json
{
  "id": 1,
  "code": "refrigerator",
  "name": "Refrigerador",
  "description": "Electrodomésticos para conservación de alimentos",
  "order": 1,
  "is_active": true,
  "product_count": 5
}
```

---

### 2. Productos

#### GET `/api/v1/products/`

Lista todos los productos activos con paginación.

**Parámetros de query:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `page` | int | Número de página (default: 1) |
| `search` | string | Buscar en: nombre, marca, modelo, descripción |
| `category_id` | int | Filtrar por categoría (ID) |
| `price_min` | decimal | Precio mínimo |
| `price_max` | decimal | Precio máximo |
| `brand` | string | Filtrar por marca (parcial, case-insensitive) |
| `is_active` | bool | Filtrar por estado activo |
| `ordering` | string | `name`, `price`, `created_at`, `stock_quantity` con `-` para descendente |

**Ejemplos:**

```bash
# Todos los productos (página 1)
curl "http://localhost:8000/api/v1/products/"

# Buscar "refrigerador"
curl "http://localhost:8000/api/v1/products/?search=refrigerador"

# Categoría 1, ordenar por precio descendente
curl "http://localhost:8000/api/v1/products/?category_id=1&ordering=-price"

# Precio entre 1000 y 5000
curl "http://localhost:8000/api/v1/products/?price_min=1000&price_max=5000"

# Marca "LG"
curl "http://localhost:8000/api/v1/products/?brand=LG"

# Combinado
curl "http://localhost:8000/api/v1/products/?category_id=1&price_min=1000&search=LG"
```

**Respuesta (listado):**
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/v1/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Refrigerador Samsung 500L",
      "category": 1,
      "category_name": "Refrigerador",
      "brand": "Samsung",
      "model": "RS25R5011SR",
      "price": "1500000.00",
      "stock_quantity": 5,
      "is_active": true,
      "first_image": "http://localhost:8000/media/products/samsung_fridge.jpg"
    }
  ]
}
```

---

#### GET `/api/v1/products/{id}/`

Obtener detalle completo de un producto.

**Ejemplo:**
```bash
curl "http://localhost:8000/api/v1/products/1/"
```

**Respuesta (detalle):**
```json
{
  "id": 1,
  "name": "Refrigerador Samsung 500L",
  "category": {
    "id": 1,
    "code": "refrigerator",
    "name": "Refrigerador",
    "description": "Electrodomésticos para conservación",
    "order": 1,
    "is_active": true,
    "product_count": 5
  },
  "brand": "Samsung",
  "model": "RS25R5011SR",
  "description": "Refrigerador de 500L con tecnología inverter...",
  "price": "1500000.00",
  "price_display": "Gs. 1.500.000,00",
  "stock_quantity": 5,
  "min_stock_quantity": 5,
  "is_active": true,
  "is_low_stock": false,
  "images": [
    {
      "id": 1,
      "image": "/media/products/samsung_fridge_1.jpg",
      "image_url": "http://localhost:8000/media/products/samsung_fridge_1.jpg",
      "order": 0
    },
    {
      "id": 2,
      "image": "/media/products/samsung_fridge_2.jpg",
      "image_url": "http://localhost:8000/media/products/samsung_fridge_2.jpg",
      "order": 1
    }
  ],
  "created_at": "2026-08-18T17:30:00Z",
  "updated_at": "2026-08-18T18:45:00Z"
}
```

---

## Características

### 📄 Paginación

- **Page size:** 20 items por página
- **Parámetro:** `?page=2`
- **Respuesta incluye:** `count`, `next`, `previous`, `results`

### 🔍 Búsqueda

Busca en: `name`, `brand`, `model`, `description`

```bash
curl "http://localhost:8000/api/v1/products/?search=samsung"
```

### 🏷️ Filtros

- **Por categoría:** `?category_id=1`
- **Por rango de precio:** `?price_min=1000&price_max=5000`
- **Por marca:** `?brand=LG`
- **Combinados:** `?category_id=1&price_min=1000&brand=Samsung`

### 📊 Ordenamiento

```bash
# Ascendente (A-Z, menor a mayor)
?ordering=name
?ordering=price
?ordering=created_at
?ordering=stock_quantity

# Descendente (Z-A, mayor a menor)
?ordering=-name
?ordering=-price
?ordering=-created_at
?ordering=-stock_quantity
```

### 🖼️ Imágenes

- **Listado:** incluye `first_image` (primera imagen)
- **Detalle:** incluye arreglo `images` (todas las imágenes)
- **URLs:** absolutas (incluyen dominio), listas para consumir en frontend

### 💰 Precios

- **Campo `price`:** valor decimal (ej: 1500000.00)
- **Campo `price_display`:** formato Guaraní (ej: "Gs. 1.500.000,00")

---

## Ejemplos de Uso en Next.js / JavaScript

### Obtener todas las categorías

```javascript
const categories = await fetch(
  'http://localhost:8000/api/v1/categories/'
).then(r => r.json());

console.log(categories); // Array de categorías
```

### Buscar productos

```javascript
const searchQuery = 'samsung';
const products = await fetch(
  `http://localhost:8000/api/v1/products/?search=${searchQuery}`
).then(r => r.json());

console.log(products.results); // Array de productos
console.log(products.count);   // Total de resultados
```

### Filtrar por categoría y precio

```javascript
const filtered = await fetch(
  'http://localhost:8000/api/v1/products/?category_id=1&price_min=1000&price_max=5000'
).then(r => r.json());
```

### Obtener detalle de producto

```javascript
const product = await fetch(
  'http://localhost:8000/api/v1/products/1/'
).then(r => r.json());

console.log(product.name);      // "Refrigerador Samsung..."
console.log(product.images);    // Array con todas las imágenes
console.log(product.category);  // Objeto categoría completo
```

---

## Códigos de Estado HTTP

| Código | Significado |
|--------|------------|
| `200` | OK - Solicitud exitosa |
| `400` | Bad Request - Parámetros inválidos |
| `404` | Not Found - Recurso no encontrado |
| `500` | Server Error - Error del servidor |

---

## Headers

### Request

```
Content-Type: application/json
```

### Response

```
Content-Type: application/json
```

---

## CORS

API permitida desde:
- `http://localhost:3000` (Next.js dev)
- `http://localhost:8000` (Django dev)
- `http://127.0.0.1:3000` (IPv4)
- `http://127.0.0.1:8000` (IPv4)

Para agregar más orígenes, editar `CORS_ALLOWED_ORIGINS` en `config/settings.py`

---

## Testeo Rápido

### Con curl

```bash
# Categorías
curl http://localhost:8000/api/v1/categories/

# Productos
curl http://localhost:8000/api/v1/products/

# Producto específico
curl http://localhost:8000/api/v1/products/1/
```

### Con navegador

Simplemente visita:
- http://localhost:8000/api/v1/categories/
- http://localhost:8000/api/v1/products/
- http://localhost:8000/api/v1/products/1/

DRF moforma una interfaz HTML interactiva para explorar la API.

---

## Notas para Fase 3 (Generador de Contenido)

La API está optimizada para:
- ✅ Obtener datos de productos con imágenes
- ✅ Filtrar por categoría, precio, marca
- ✅ Buscar productos específicos
- ✅ URLs de imágenes absolutas para compartir en redes

Ideal para automatizar posts con datos reales de la tienda.
