# Sistema de Gestión — Tienda de Electrodomésticos y Muebles

Sistema web para digitalizar la operación de una tienda: stock/inventario y gestión de créditos con cronograma de cuotas.

## Características

- **Gestión de Productos**: alta, edición, baja lógica, categorías, imágenes y stock.
- **Movimientos de Stock**: registro de entradas (compra), salidas (venta) y ajustes.
- **Gestión de Clientes**: datos de cliente y historial de créditos.
- **Ventas a Crédito**: creación automática de cronograma de cuotas (sin interés), registro de pagos.
- **Reportes**: bajo stock, mora (cuotas vencidas), vencimientos próximos (7 días).
- **Autenticación**: usuarios con roles (dueño, vendedor).
- **100% Web**: accesible desde cualquier dispositivo con navegador.

## Stack

- **Backend**: Django 4.2 + PostgreSQL
- **Frontend**: Server-rendered (Django templates + Bootstrap 5)
- **Despliegue**: Docker + PaaS (Railway, Render)

## Configuración Local

### Requisitos previos

- Docker y Docker Compose
- O Python 3.11+ + PostgreSQL 16+

### Opción 1: Con Docker Compose (recomendado)

```bash
# Copiar variables de entorno
cp .env.example .env

# Levantar servicios (Postgres + app web)
docker-compose up

# En otra terminal, ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear usuario admin
docker-compose exec web python manage.py createsuperuser
```

La app estará disponible en `http://localhost:8000`

### Opción 2: Desarrollo local (sin Docker)

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env con DATABASE_URL apuntando a tu Postgres
cp .env.example .env
# Editar .env: DATABASE_URL=postgresql://user:pass@localhost/tienda_db

# Ejecutar migraciones
python manage.py migrate

# Crear usuario admin
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

## Acceso

- **App web**: http://localhost:8000
- **Admin (Django)**: http://localhost:8000/admin

## Estructura del Proyecto

```
├── config/              # Configuración del proyecto Django
├── core/                # Aplicación base (templates, TimeStampedModel)
├── accounts/            # Usuarios y autenticación
├── inventory/           # Módulo de stock/productos
├── credits/             # Módulo de créditos/cuotas
├── reports/             # Reportes simples
├── templates/           # Templates HTML server-rendered
├── docker-compose.yml   # Orquestación de servicios
├── Dockerfile
├── requirements.txt
└── manage.py
```

## Flujos Principales

### 1. Alta de Producto

1. Ir a **Productos** → **Crear Producto**
2. Completar nombre, marca, modelo, precio, stock inicial
3. Guardar

### 2. Registrar Movimiento de Stock

1. Ir a **Movimientos Stock** → **Registrar Movimiento**
2. Seleccionar producto, tipo (entrada/salida/ajuste), cantidad y razón
3. Guardar → descuenta automáticamente del stock

### 3. Venta a Crédito

1. Crear cliente (si no existe): **Clientes** → **Crear Cliente**
2. Crear venta: **Ventas Crédito** → **Crear Venta**
3. Seleccionar cliente, monto total, cantidad de cuotas, fecha de inicio
4. Guardar → sistema genera automáticamente el cronograma (cuotas mensuales, ajuste de centavos en la última)

### 4. Registrar Pago de Cuota

1. Ver detalle de venta: **Ventas Crédito** → seleccionar venta
2. En la tabla de cuotas, hacer clic en **Pagar** en la cuota pendiente
3. Ingresar monto pagado y fecha
4. Guardar → cuota se marca como pagada automáticamente si el pago cubre el monto

### 5. Consultar Reportes

- **Bajo Stock**: **Reportes** → **Bajo Stock** — productos por debajo del mínimo
- **Mora**: **Reportes** → **Mora** — cuotas vencidas sin pagar
- **Próximos Vencimientos**: **Reportes** → **Vencimientos Próximos** — cuotas que vencen en los próximos 7 días

## Despliegue en Producción

### Railway

1. Hacer fork/push del repositorio a GitHub
2. Ir a [railway.app](https://railway.app), crear un nuevo proyecto
3. Conectar repositorio GitHub
4. Agregar servicio PostgreSQL administrado
5. Configurar variables de entorno en Railway: `DEBUG=False`, `SECRET_KEY`, `DATABASE_URL` (auto), `ALLOWED_HOSTS`
6. Deploy automático

### Render

1. Conectar repo a GitHub
2. Crear new Web Service en [render.com](https://render.com)
3. Seleccionar repo, rama `main`
4. Build command: `pip install -r requirements.txt && python manage.py migrate`
5. Start command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
6. Agregar PostgreSQL addon
7. Configurar env vars
8. Deploy

## Próximas Fases

- **Fase 2**: API REST con Django REST Framework para alimentar catálogo web público
- **Fase 3**: Generador de contenido para redes sociales usando datos del catálogo

## Licencia

Privada — sistema para uso interno de la tienda.
