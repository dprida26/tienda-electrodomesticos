# Guía de Ejecución - Fase 2: API REST + Web Pública

## 📋 Requisitos Previos

### Backend (Django)
- Python 3.11+
- PostgreSQL 16+
- Docker y Docker Compose (opcional)

### Frontend (Next.js)
- Node.js 18+
- npm o yarn

---

## 🚀 Opción 1: Ejecución Rápida con Docker

### Backend Django

```bash
cd "Tienda electrodomesticos"

# Levantar servicios
docker-compose up

# En otra terminal, aplicar migraciones
docker-compose exec web python manage.py migrate

# Crear usuario admin (si es primera vez)
docker-compose exec web python manage.py createsuperuser
```

La app estará en:
- 🌐 **Web:** http://localhost:8000/
- 🔧 **Admin:** http://localhost:8000/admin/
- 🔌 **API:** http://localhost:8000/api/v1/

### Frontend Next.js

```bash
cd "tienda-web"

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev
```

Acceder a: **http://localhost:3000**

---

## 💻 Opción 2: Ejecución Local (Sin Docker)

### Backend Django

```bash
cd "Tienda electrodomesticos"

# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate
# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar BD (asegurar PostgreSQL esté corriendo)
# Editar .env con tu DATABASE_URL

# Ejecutar migraciones
python manage.py migrate

# Crear usuario admin
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

**API disponible en:** http://localhost:8000/api/v1/

### Frontend Next.js

```bash
cd "tienda-web"

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev
```

**Web disponible en:** http://localhost:3000

---

## 🧪 Probar la Integración

### 1. Verificar API desde Navegador

Visita en tu navegador:
```
http://localhost:8000/api/v1/categories/
http://localhost:8000/api/v1/products/
```

Deberías ver JSON con categorías y productos.

### 2. Verificar Conexión desde Next.js

```bash
# En la terminal de Next.js debería decir:
# ✓ Ready in XXXX ms
# ✓ Compiled successfully

# Visita http://localhost:3000
# Deberías ver productos en la página de inicio
```

### 3. Testear Endpoints

```bash
# Obtener categorías
curl http://localhost:8000/api/v1/categories/

# Obtener productos
curl http://localhost:8000/api/v1/products/

# Buscar "refrigerador"
curl "http://localhost:8000/api/v1/products/?search=refrigerador"

# Filtrar por categoría 1
curl "http://localhost:8000/api/v1/products/?category_id=1"
```

---

## 📝 Pasos para Agregar Productos

### Desde el Admin de Django

1. Ir a: **http://localhost:8000/admin**
2. Iniciar sesión con usuario admin
3. En **Inventario** → **Productos** → **Agregar Producto**
4. Completar:
   - Nombre
   - Categoría (seleccionar del dropdown)
   - Marca y Modelo
   - Descripción
   - Precio (sin separadores, ej: 1500000.00)
   - Stock
5. Guardar

### Agregar Imágenes

1. En el mismo formulario, abajo está **"Imágenes"**
2. Hacer clic en **"Agregar Imagen"**
3. Subir archivo (JPG, PNG)
4. Guardar

---

## 🌐 URLs Importantes

| Servicio | URL | Descripción |
|----------|-----|------------|
| API Django | http://localhost:8000/api/v1/ | REST API pública |
| Admin Django | http://localhost:8000/admin/ | Administración |
| Frontend | http://localhost:3000 | Página web pública |
| Inicio | http://localhost:3000/ | Hero + productos |
| Catálogo | http://localhost:3000/catalogo | Listado de productos |
| Producto | http://localhost:3000/productos/1 | Detalle (ID varía) |
| Contacto | http://localhost:3000/contacto | Formulario de contacto |

---

## 📱 Probar en Celular

### Si Django y Next.js están en localhost

Desde otro dispositivo en la red, abre:
```
http://TU_IP_LOCAL:3000
```

Para obtener tu IP local:
```bash
# Windows
ipconfig  # Buscar IPv4 Address

# Linux/Mac
ifconfig  # Buscar inet
```

**Nota:** Django debe permitir esa IP en `ALLOWED_HOSTS` en `config/settings.py`

---

## 🔧 Troubleshooting

### Error: "Cannot connect to API"

```bash
# 1. Verificar Django está corriendo
curl http://localhost:8000/

# 2. Verificar API está disponible
curl http://localhost:8000/api/v1/categories/

# 3. Revisar .env.local en Next.js
cat tienda-web/.env.local
# Debería tener: NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Error: "Database connection refused"

```bash
# 1. Verificar PostgreSQL está corriendo
# Docker:
docker ps | grep postgres

# Local: asegurar PostgreSQL está iniciado
```

### Error: "Module not found" en Next.js

```bash
cd tienda-web
rm -rf node_modules package-lock.json
npm install
```

### Productos no aparecen en web

```bash
# 1. Revisar admin Django
http://localhost:8000/admin/inventory/product/

# 2. Agregar producto si no hay
# 3. Verificar que sea "is_active = True"

# 4. En navegador, ir a:
http://localhost:3000/catalogo
```

---

## 📊 Estructura de Datos

### Categorías
```json
{
  "id": 1,
  "code": "refrigerator",
  "name": "Refrigerador",
  "product_count": 5
}
```

### Productos (Listado)
```json
{
  "id": 1,
  "name": "Refrigerador Samsung 500L",
  "category_name": "Refrigerador",
  "brand": "Samsung",
  "price": "1500000.00",
  "price_display": "Gs. 1.500.000,00",
  "stock_quantity": 5,
  "first_image": "http://..."
}
```

### Productos (Detalle)
```json
{
  "id": 1,
  "name": "...",
  "description": "...",
  "price": "1500000.00",
  "price_display": "Gs. 1.500.000,00",
  "category": {...},
  "images": [
    {
      "id": 1,
      "image_url": "http://localhost:8000/media/products/..."
    }
  ]
}
```

---

## 🚢 Deployment (Producción)

### Backend - Railway o Render

1. Hacer push del repo a GitHub
2. Conectar en [railway.app](https://railway.app) o [render.com](https://render.com)
3. Agregar PostgreSQL addon
4. Configurar variables de entorno:
   ```
   DEBUG=False
   SECRET_KEY=<generar>
   DATABASE_URL=<auto>
   ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
   ```

### Frontend - Vercel

1. Hacer push del repo `/tienda-web` a GitHub
2. Conectar en [vercel.com](https://vercel.com)
3. Configurar variable de entorno:
   ```
   NEXT_PUBLIC_API_URL=https://tu-api.railway.app/api/v1
   ```
4. Deploy automático

---

## 📚 Documentación Completa

- **API:** Ver [API_DOCS.md](Tienda%20electrodomesticos/API_DOCS.md)
- **Ejecución API:** Ver [EJECUTAR_API.md](Tienda%20electrodomesticos/EJECUTAR_API.md)
- **Migraciones:** Ver [MIGRACIONES.md](Tienda%20electrodomesticos/MIGRACIONES.md)
- **Roadmap:** Ver [FASE2_ROADMAP.md](Tienda%20electrodomesticos/FASE2_ROADMAP.md)
- **Frontend:** Ver [README_TIENDA.md](tienda-web/README_TIENDA.md)

---

## ✅ Checklist de Verificación

- [ ] Django corriendo en http://localhost:8000/
- [ ] PostgreSQL conectado y migraciones aplicadas
- [ ] API disponible en http://localhost:8000/api/v1/
- [ ] Productos agregados en admin
- [ ] Next.js corriendo en http://localhost:3000
- [ ] Página inicio carga con productos
- [ ] Búsqueda y filtros funcionan
- [ ] Detalle de producto carga imágenes
- [ ] Formulario de contacto envía datos

---

## 🎯 Próximos Pasos

**Fase 3: Generador de Contenido**
- Automatizar posts para redes sociales
- Usar datos reales de la tienda
- Crear imágenes con texto dinámico

Ver: [FASE2_ROADMAP.md](Tienda%20electrodomesticos/FASE2_ROADMAP.md#fase-3-generador-de-contenido)

---

## 📞 Soporte

Revisa la documentación específica de cada servicio en sus respectivas carpetas o archivos README.
