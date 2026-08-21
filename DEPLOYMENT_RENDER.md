# 🚀 Guía de Despliegue en Render.com

## 📋 Resumen del Proyecto

**Tienda de Electrodomésticos** - Sistema completo de e-commerce con:
- ✅ Backend: Django REST API
- ✅ Frontend: Next.js con Tailwind CSS
- ✅ Base de Datos: PostgreSQL
- ✅ Ofertas con fechas de inicio/fin
- ✅ Gestión de productos, stock e imágenes

---

## 🔧 Preparación Previa

### 1. Crear repositorio GitHub

```bash
# En la raíz del proyecto (donde están tienda-frontend y Tienda electrodomesticos)
git init
git add .
git commit -m "Initial commit: Tienda electrodomésticos completa"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/tienda-electrodomesticos.git
git push -u origin main
```

### 2. Estructura esperada en GitHub

```
tienda-electrodomesticos/
├── tienda-frontend/          # Next.js frontend
│   ├── package.json
│   ├── next.config.js
│   ├── .env.local (no commit)
│   └── src/
├── Tienda electrodomesticos/ # Django backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   └── .env (no commit)
└── README.md
```

---

## 🎯 Pasos de Despliegue en Render

### Paso 1: Crear Web Service para Django Backend

1. **Ir a [render.com](https://render.com)**
2. **Crear nuevo "Web Service"**
3. **Conectar GitHub** y seleccionar el repositorio

**Configuración:**
- **Name**: `tienda-electrodomesticos-api`
- **Environment**: `Python 3.11`
- **Region**: Seleccionar región más cercana (ej: N. Virginia)
- **Branch**: `main`
- **Root Directory**: `Tienda electrodomesticos`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt && python manage.py migrate
  ```
- **Start Command**:
  ```bash
  gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
  ```

**Environment Variables** (Add):
```
DEBUG=False
SECRET_KEY=django-insecure-your-random-secret-key-here
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DBNAME
ALLOWED_HOSTS=tienda-electrodomesticos-api.onrender.com,*.onrender.com
CORS_ALLOWED_ORIGINS=https://tienda-electrodomesticos-web.onrender.com
```

**Instance Type**: Free (para demostración)

### Paso 2: Crear PostgreSQL Database

1. **En Render dashboard, click "New"** → **PostgreSQL**
2. **Configuración**:
   - **Name**: `tienda-electrodomesticos-db`
   - **Region**: Misma que Django
   - **PostgreSQL Version**: 16

3. **Copiar `DATABASE_URL`** y pegarlo en las variables de Django

### Paso 3: Crear Web Service para Next.js Frontend

1. **Crear nuevo "Web Service"**
2. **Conectar GitHub** (mismo repositorio)

**Configuración:**
- **Name**: `tienda-electrodomesticos-web`
- **Environment**: `Node`
- **Region**: Misma que el backend
- **Branch**: `main`
- **Root Directory**: `tienda-frontend`
- **Build Command**:
  ```bash
  npm install && npm run build
  ```
- **Start Command**:
  ```bash
  npm run start
  ```

**Environment Variables** (Add):
```
NEXT_PUBLIC_API_URL=https://tienda-electrodomesticos-api.onrender.com/api/v1
NODE_ENV=production
```

**Instance Type**: Free

### Paso 4: Esperar Deploy

- Django tardará ~2 minutos
- Next.js tardará ~3 minutos
- Una vez "Live", tendrás URLs como:
  - API: `https://tienda-electrodomesticos-api.onrender.com`
  - Web: `https://tienda-electrodomesticos-web.onrender.com`

---

## 📦 Instalación de Dependencias

### Backend (Django)

Asegurar que `requirements.txt` incluya:

```
Django==4.2
djangorestframework==3.14.0
django-cors-headers==4.3.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
python-decouple==3.8
Pillow==10.0.0
```

### Frontend (Next.js)

El `package.json` ya está configurado. Dependencies principales:
- next@15.0.0
- react@18.3.0
- axios
- tailwindcss
- lucide-react

---

## 🔒 Variables de Entorno Importantes

### Backend (.env - NO COMMITEAR)
```
DEBUG=False
SECRET_KEY=<generar con Python>
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=.onrender.com
CORS_ALLOWED_ORIGINS=https://tienda-electrodomesticos-web.onrender.com
```

**Generar SECRET_KEY seguro:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Frontend (.env.local - NO COMMITEAR)
```
NEXT_PUBLIC_API_URL=https://tienda-electrodomesticos-api.onrender.com/api/v1
```

---

## ✅ Verificación Post-Deploy

1. **API Health Check**
   ```bash
   curl https://tienda-electrodomesticos-api.onrender.com/api/v1/products/
   ```

2. **Frontend Acceso**
   - Abrir: https://tienda-electrodomesticos-web.onrender.com
   - Verificar que se cargan productos
   - Verificar que se muestran ofertas

3. **Admin Django**
   - URL: https://tienda-electrodomesticos-api.onrender.com/admin
   - Usuario: `admin` / contraseña: la que creaste localmente

---

## 🐛 Troubleshooting

### "ModuleNotFoundError" en Django

→ Ejecutar en Render shell:
```bash
pip install -r requirements.txt
python manage.py migrate
```

### "CORS error" en Next.js

→ Verificar `CORS_ALLOWED_ORIGINS` en Django settings

### Imágenes no cargan

→ Usar AWS S3 o Cloudinary (opcional pero recomendado):
```bash
pip install django-storages boto3
```

### Base de datos vacía

→ Ejecutar seed en Render shell:
```bash
python load_sample_data.py
```

---

## 📊 Monitoreo

En Render dashboard:
- **Logs**: Verificar errores en tiempo real
- **Metrics**: CPU, memoria, request count
- **Events**: Historial de deploys

---

## 🎬 Mejoras Futuras

1. **CDN para imágenes**: Cloudinary o AWS S3
2. **Caché con Redis**: Mejorar rendimiento
3. **CI/CD avanzado**: Tests automáticos antes de deploy
4. **Dominio personalizado**: Comprar dominio y configurar DNS
5. **SSL/HTTPS**: Render incluye automáticamente

---

## 📞 Soporte

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/
- **Next.js Deployment**: https://nextjs.org/docs/deployment

---

**¡Listo para producción!** 🎉
