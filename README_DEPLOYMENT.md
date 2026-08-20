# 🏪 Tienda de Electrodomésticos - Sistema Completo

## 📱 Demo Disponible

**Frontend**: https://tienda-electrodomesticos-web.onrender.com  
**API**: https://tienda-electrodomesticos-api.onrender.com/api/v1  
**Admin**: https://tienda-electrodomesticos-api.onrender.com/admin  

---

## ✨ Características Implementadas

### 🛒 Catálogo de Productos
- ✅ Listado con búsqueda y filtros
- ✅ Imágenes responsivas (sin recortes)
- ✅ Información detallada por producto
- ✅ Stock en tiempo real
- ✅ Categorías dinámicas

### 💰 Sistema de Ofertas
- ✅ Descuentos con porcentaje automático
- ✅ **Fechas de inicio y fin de oferta** (NUEVO)
- ✅ Validación automática de ofertas vigentes
- ✅ Página dedicada de ofertas
- ✅ Badges de descuento visual

### 🛍️ Carrito y Compra
- ✅ Añadir/eliminar productos
- ✅ Calculadora de cuotas
- ✅ Opciones de pago (contado/cuotas)
- ✅ Múltiples opciones de financiamiento

### 📊 Gestión Administrativa
- ✅ Panel de admin Django
- ✅ Gestión de productos (alta, edición, baja)
- ✅ Movimientos de stock
- ✅ Gestión de ofertas con fechas
- ✅ Reportes de mora y bajo stock
- ✅ Gestión de clientes y créditos

### 🔌 API REST
- ✅ Endpoint productos con filtros
- ✅ Endpoint categorías
- ✅ Endpoint ofertas
- ✅ Documentación automática (Swagger)
- ✅ CORS habilitado

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────┐
│         Next.js Frontend (puerto 3000)      │
│  - Catálogo, ofertas, detalle de productos │
│  - Carrito y checkout                       │
│  - Responsive design con Tailwind CSS       │
└──────────────┬──────────────────────────────┘
               │
        API REST (http)
               │
┌──────────────▼──────────────────────────────┐
│      Django Backend (puerto 8000)           │
│  - Gestión de productos e inventario        │
│  - Sistema de créditos y cuotas             │
│  - Autenticación y permisos                 │
│  - Admin panel                              │
└──────────────┬──────────────────────────────┘
               │
        PostgreSQL connection
               │
┌──────────────▼──────────────────────────────┐
│    PostgreSQL Database                      │
│  - Productos, categorías, imágenes         │
│  - Créditos, cuotas, pagos                 │
│  - Ofertas con fechas                      │
└─────────────────────────────────────────────┘
```

---

## 🚀 Stack Tecnológico

### Frontend
- **Framework**: Next.js 15
- **Styling**: Tailwind CSS
- **Estado**: React Hooks
- **HTTP**: Axios
- **Icons**: Lucide React

### Backend
- **Framework**: Django 4.2
- **API**: Django REST Framework
- **ORM**: Django ORM (Prisma-like)
- **Base de Datos**: PostgreSQL 16
- **Autenticación**: Token-based (JWT)
- **CORS**: django-cors-headers

### Despliegue
- **Hosting**: Render.com (frontend + backend)
- **Base de Datos**: PostgreSQL managed en Render
- **Dominio**: .onrender.com (personalizable)
- **SSL/HTTPS**: Automático

---

## 📂 Estructura del Proyecto

```
tienda-electrodomesticos/
│
├── tienda-frontend/                    # Next.js App
│   ├── src/
│   │   ├── app/                        # Rutas (App Router)
│   │   │   ├── page.jsx                # Home con catálogo
│   │   │   ├── productos/              # Listado de productos
│   │   │   ├── productos/[id]/         # Detalle de producto
│   │   │   ├── ofertas/                # Página de ofertas
│   │   │   └── categorias/             # Filtrado por categoría
│   │   ├── components/                 # Componentes reutilizables
│   │   │   ├── ProductCard.jsx         # Tarjeta de producto
│   │   │   ├── ProductGrid.jsx         # Grid de productos
│   │   │   ├── Header.jsx              # Navegación
│   │   │   └── Hero.jsx                # Banner principal
│   │   └── services/
│   │       └── api.js                  # Llamadas a API
│   ├── package.json
│   ├── .env.local                      # Variables de entorno
│   └── next.config.js
│
├── Tienda electrodomesticos/           # Django App
│   ├── config/                         # Configuración
│   │   ├── settings.py                 # Configuración Django
│   │   ├── urls.py                     # Rutas principales
│   │   └── wsgi.py                     # WSGI para Gunicorn
│   ├── inventory/                      # Módulo de productos
│   │   ├── models.py                   # Modelos (Product, Category, etc)
│   │   ├── views.py                    # Vistas
│   │   ├── viewsets.py                 # ViewSets de API
│   │   ├── serializers.py              # Serializers
│   │   ├── forms.py                    # Formularios
│   │   └── migrations/                 # Migraciones BD
│   ├── credits/                        # Módulo de créditos
│   │   ├── models.py                   # Modelos de crédito
│   │   └── views.py
│   ├── reports/                        # Reportes
│   ├── templates/                      # Templates admin
│   ├── manage.py
│   ├── requirements.txt                # Dependencias Python
│   ├── .env                            # Variables (no commitear)
│   └── db.sqlite3                      # BD local (no usar en prod)
│
├── DEPLOYMENT_RENDER.md                # Guía de despliegue
└── README.md
```

---

## 🎯 Modelo de Datos Principal

### Product
```python
- id, name, brand, model, description
- price (precio normal)
- sale_price (precio en oferta)
- is_on_sale (booleano)
- offer_start_date (nuevo)
- offer_end_date (nuevo)
- is_offer_active (calculado automáticamente)
- discount_percentage (calculado automáticamente)
- stock_quantity, min_stock_quantity
- installment_interest_rate, installment_options
- category (FK)
- created_at, updated_at
```

### ProductCategory
```python
- id, code, name, description
- order (para ordenamiento)
- is_active
```

### ProductImage
```python
- id, product (FK), image, order
```

### Oferta (Lógica)
Una oferta es **VIGENTE** si:
- ✅ `is_on_sale = true`
- ✅ Fecha actual >= `offer_start_date`
- ✅ Fecha actual <= `offer_end_date`

---

## 🔐 Variables de Entorno

### Backend (Django)
```env
DEBUG=False                                    # Producción
SECRET_KEY=django-insecure-xxx                # Generar nuevo
DATABASE_URL=postgresql://user:pass@host:5432/db
ALLOWED_HOSTS=.onrender.com
CORS_ALLOWED_ORIGINS=https://frontend-url.com
```

### Frontend (Next.js)
```env
NEXT_PUBLIC_API_URL=https://backend-url.com/api/v1
```

---

## 📥 Despliegue Rápido (Render)

### 1. Preparar GitHub
```bash
git init
git add .
git commit -m "Initial: Tienda electrodomésticos completa"
git branch -M main
git remote add origin https://github.com/username/tienda-electrodomesticos.git
git push -u origin main
```

### 2. Desplegar en Render
1. Ir a [render.com](https://render.com)
2. Crear Web Service Django
3. Crear PostgreSQL Database
4. Crear Web Service Next.js
5. Configurar variables de entorno

**Tiempo total**: ~5 minutos

### 3. Acceder
- Frontend: https://tienda-electrodomesticos-web.onrender.com
- API: https://tienda-electrodomesticos-api.onrender.com/api/v1
- Admin: https://tienda-electrodomesticos-api.onrender.com/admin

---

## 🧪 Prueba Local

### Backend
```bash
cd "Tienda electrodomesticos"
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

### Frontend
```bash
cd tienda-frontend
npm install
npm run dev  # http://localhost:3000
```

---

## 📊 API Endpoints Principales

```
GET  /api/v1/products/                 # Listado productos
GET  /api/v1/products/?is_on_sale=true # Solo ofertas
GET  /api/v1/products/{id}/            # Detalle producto
GET  /api/v1/categories/               # Categorías
GET  /api/v1/products/?category=xxx    # Filtrar por categoría
```

---

## 🎨 Screenshots

| Pantalla | Descripción |
|----------|-------------|
| **Home** | Catálogo principal con ofertas destacadas |
| **Producto** | Detalle con imágenes, precio, cuotas |
| **Ofertas** | Página dedicada a productos en descuento |
| **Admin** | Panel Django para gestionar todo |

---

## 📞 Soporte

- **Issues**: Crear issue en GitHub
- **Documentación**: Ver `DEPLOYMENT_RENDER.md`
- **Contacto**: Via WhatsApp (integrado en footer)

---

## 📄 Licencia

Privada - Uso interno de la tienda

---

**Versión**: 1.0.0  
**Última actualización**: 2026-08-20  
**Estado**: ✅ Listo para producción
