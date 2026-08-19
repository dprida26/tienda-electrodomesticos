# Guía de Migraciones - ProductCategory

## Cambios Realizados (Commit: 9a0a12f)

### Nuevo Modelo: `ProductCategory`

Se ha creado un nuevo modelo `ProductCategory` para gestionar categorías de manera dinámica sin necesidad de escribir código o ejecutar migraciones cada vez que se agrega una categoría.

**Beneficios:**
- ✅ Agregar/editar categorías desde el admin de Django
- ✅ Sin dependencia de migraciones para nuevas categorías
- ✅ Preparado para API REST y web pública (Fase 2)
- ✅ Mejor para generador de contenido (Fase 3)

### Cambios en la Base de Datos

1. **Nueva tabla:** `inventory_productcategory`
2. **Columna actualizada en `inventory_product`:**
   - `category` cambió de `VARCHAR(50)` con opciones fijas a `BIGINT` (ForeignKey)

### Migraciones a Ejecutar

```bash
# Si estás usando Docker:
docker-compose exec web python manage.py migrate

# Si estás en desarrollo local:
python manage.py migrate
```

**Las migraciones harán:**
1. Crear tabla `ProductCategory`
2. Alterar columna `category` en `Product`
3. Crear 8 categorías iniciales automáticamente:
   - Refrigerador
   - Horno
   - Lavadora
   - Secadora
   - Lava Platos
   - Microondas
   - Muebles
   - Otro

## Cómo Agregar Nuevas Categorías

### Opción 1: Desde el Admin de Django (Recomendado)

1. Ir a http://localhost:8000/admin
2. Buscar **Categorías de Productos** en el menú
3. Hacer clic en **Agregar Categoría**
4. Llenar:
   - **Código:** `air_conditioner` (sin espacios, en minúsculas)
   - **Nombre:** `Aire Acondicionado`
   - **Descripción:** (opcional)
   - **Orden:** número para ordenar en listas
   - **Activo:** marcar para que aparezca en filtros

### Opción 2: Desde línea de comandos (Django shell)

```bash
python manage.py shell

>>> from inventory.models import ProductCategory
>>> ProductCategory.objects.create(
...     code='air_conditioner',
...     name='Aire Acondicionado',
...     order=9,
...     is_active=True
... )
```

## Cambios en Código de Usuario

**Anteriormente (CharField con choices):**
```python
product.category  # Retornaba: 'refrigerator'
product.get_category_display()  # Retornaba: 'Refrigerador'
```

**Ahora (ForeignKey):**
```python
product.category  # Retorna objeto ProductCategory
product.category.name  # Retorna: 'Refrigerador'
product.category.code  # Retorna: 'refrigerator'
```

## Rollback (Deshacer Migraciones)

Si necesitas deshacer los cambios:

```bash
# Deshacer todas las migraciones de inventory
python manage.py migrate inventory zero

# O deshacer solo hasta la migración 0001_initial
python manage.py migrate inventory 0001_initial
```

## Notas Importantes

- ⚠️ **No eliminar categorías usadas:** Está protegido por `on_delete=PROTECT`, no se pueden eliminar categorías que tienen productos
- ⚠️ **Códigos únicos:** El campo `code` es único, no puede haber dos categorías con el mismo código
- ✅ Todas las categorías iniciales se crean automáticamente
- ✅ Compatible con el admin de Django
- ✅ Preparado para API REST (Fase 2)

## Verificación

Después de ejecutar las migraciones, verifica en el admin:

1. http://localhost:8000/admin/inventory/productcategory/
2. Deberías ver 8 categorías listadas
3. Puedes editar orden o estado sin afectar la BD de producción
