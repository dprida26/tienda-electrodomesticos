# Cómo Ejecutar la API REST

## Prerequisitos

1. **Tener Django funcionando** - ver [README.md](README.md)
2. **Dependencias instaladas** - correr:
   ```bash
   pip install -r requirements.txt
   ```
3. **Migraciones aplicadas** - correr:
   ```bash
   python manage.py migrate
   ```

## Pasos para Ejecutar

### Opción 1: Con Docker (Recomendado)

```bash
# Desde la raíz del proyecto
docker-compose up
```

La API estará disponible en:
- **API:** http://localhost:8000/api/v1/
- **Django Admin:** http://localhost:8000/admin/
- **App Web:** http://localhost:8000/

### Opción 2: Desarrollo Local

```bash
# En una terminal, activar venv si lo usas:
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python manage.py runserver
```

La API estará en: http://localhost:8000/api/v1/

---

## Testear Endpoints

### Con Navegador (más fácil)

Simplemente visita en tu navegador:

```
http://localhost:8000/api/v1/categories/
http://localhost:8000/api/v1/products/
http://localhost:8000/api/v1/products/1/
```

**Bonus:** DRF te muestra una interfaz HTML interactiva para explorar la API.

### Con curl (línea de comandos)

```bash
# Obtener categorías
curl http://localhost:8000/api/v1/categories/

# Obtener productos
curl http://localhost:8000/api/v1/products/

# Buscar "refrigerador"
curl "http://localhost:8000/api/v1/products/?search=refrigerador"

# Filtrar por categoría 1, ordenar por precio
curl "http://localhost:8000/api/v1/products/?category_id=1&ordering=-price"

# Rango de precio
curl "http://localhost:8000/api/v1/products/?price_min=1000&price_max=5000"
```

### Con Postman

1. Descargar [Postman](https://www.postman.com/downloads/)
2. Crear nueva solicitud GET
3. Escribir URL: `http://localhost:8000/api/v1/products/`
4. Click en "Send"

---

## Parámetros Disponibles

### Búsqueda y Filtros

```bash
# Búsqueda de texto
?search=samsung

# Por categoría (ID)
?category_id=1

# Por rango de precio
?price_min=1000&price_max=5000

# Por marca
?brand=LG

# Estado activo
?is_active=true

# Combinados
?category_id=1&price_min=1000&search=samsung&ordering=-price
```

### Ordenamiento

```bash
# Ascendente
?ordering=name              # A-Z
?ordering=price             # menor a mayor
?ordering=created_at        # más antiguo primero

# Descendente (add -)
?ordering=-name             # Z-A
?ordering=-price            # mayor a menor
?ordering=-created_at       # más reciente primero
```

### Paginación

```bash
# Página 1 (default)
?page=1

# Página 2
?page=2

# (20 items por página)
```

---

## Ejemplos Prácticos

### 1. Listar todas las categorías

```
http://localhost:8000/api/v1/categories/
```

### 2. Buscar refrigeradores

```
http://localhost:8000/api/v1/products/?search=refrigerador
```

### 3. Productos Samsung ordenados por precio (mayor a menor)

```
http://localhost:8000/api/v1/products/?brand=Samsung&ordering=-price
```

### 4. Electrodomésticos entre 1,000,000 y 3,000,000 Gs.

```
http://localhost:8000/api/v1/products/?category_id=1&price_min=1000000&price_max=3000000
```

### 5. Obtener detalle completo de producto ID 1

```
http://localhost:8000/api/v1/products/1/
```

---

## Estructura de Respuesta

### Listado (ProductList)

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
      "first_image": "http://localhost:8000/media/products/...jpg"
    }
  ]
}
```

### Detalle (ProductDetail)

```json
{
  "id": 1,
  "name": "Refrigerador Samsung 500L",
  "category": {
    "id": 1,
    "code": "refrigerator",
    "name": "Refrigerador",
    "order": 1,
    "is_active": true,
    "product_count": 5
  },
  "brand": "Samsung",
  "model": "RS25R5011SR",
  "description": "Descripción del producto...",
  "price": "1500000.00",
  "price_display": "Gs. 1.500.000,00",
  "stock_quantity": 5,
  "is_active": true,
  "images": [
    {
      "id": 1,
      "image": "/media/products/...jpg",
      "image_url": "http://localhost:8000/media/products/...jpg",
      "order": 0
    }
  ],
  "created_at": "2026-08-18T17:30:00Z",
  "updated_at": "2026-08-18T18:45:00Z"
}
```

---

## Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'rest_framework'`

**Solución:** Instalar dependencias

```bash
pip install -r requirements.txt
```

### Error: `Connection refused` en `/api/v1/...`

**Solución:** Asegúrate que Django está corriendo:

```bash
# Ver si está en http://localhost:8000/
python manage.py runserver
```

### No hay productos en la API

**Solución:** Agrega productos desde el admin:

1. http://localhost:8000/admin/
2. Inventario → Productos → Agregar Producto
3. Completa el formulario y guarda

### Las imágenes no se ven

**Solución:** Asegúrate que:
1. El producto tiene imágenes subidas
2. La carpeta `media/` existe
3. Las URLs son absolutas (incluyen `http://localhost:8000/`)

---

## Siguiente Paso: Next.js Web

Ahora que la API está lista, puedes:

1. Crear proyecto Next.js: `npx create-next-app@latest`
2. Consumir endpoints desde el frontend
3. Ver [API_DOCS.md](API_DOCS.md) para ejemplos completos

---

## ¿Necesitas ayuda?

- Ver [API_DOCS.md](API_DOCS.md) para documentación completa
- Ver [FASE2_ROADMAP.md](FASE2_ROADMAP.md) para el plan general
- Revisar ejemplos en la consola del navegador (F12)
