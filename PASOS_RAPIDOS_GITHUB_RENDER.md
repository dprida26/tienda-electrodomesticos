# ⚡ Guía Rápida: GitHub + Render (10 minutos)

## Paso 1: Crear Repositorio en GitHub (2 min)

1. Ir a https://github.com/new
2. **Repository name**: `tienda-electrodomesticos`
3. **Description**: `Sistema de e-commerce con Django + Next.js`
4. **Visibility**: Public (para demostración)
5. **Click "Create repository"**

Copiar URL del repositorio (ej: `https://github.com/tu-usuario/tienda-electrodomesticos.git`)

---

## Paso 2: Pushear Código a GitHub (3 min)

Ejecutar en la terminal (en `c:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA`):

```bash
# Agregamos remoto (reemplazar con tu URL)
git remote add origin https://github.com/TU_USUARIO/tienda-electrodomesticos.git

# Pushear rama main
git branch -M main
git push -u origin main
```

**Listo!** ✅ Tu código ya está en GitHub

---

## Paso 3: Desplegar en Render.com (5 min)

### 3.1 Crear PostgreSQL Database

1. Ir a https://dashboard.render.com
2. **Click "+ New"** → **PostgreSQL**
3. **Name**: `tienda-db`
4. **Region**: Seleccionar región
5. **Click "Create Database"**
6. **Copiar `DATABASE_URL`** (lo necesitaremos)

### 3.2 Desplegar Backend (Django)

1. **Click "+ New"** → **Web Service**
2. **Conectar GitHub**: Buscar `tienda-electrodomesticos`
3. **Configuración**:
   - **Name**: `tienda-api`
   - **Region**: Igual que BD
   - **Branch**: `main`
   - **Root Directory**: `Tienda electrodomesticos`
   - **Environment**: Python 3.11
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py migrate
     ```
   - **Start Command**:
     ```
     gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
     ```

4. **Environment Variables** (Click "Add Environment Variable"):
   ```
   DEBUG=False
   SECRET_KEY=<generar con: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'>
   DATABASE_URL=<pegar la URL de PostgreSQL>
   ALLOWED_HOSTS=.onrender.com
   CORS_ALLOWED_ORIGINS=https://tienda-web.onrender.com
   ```

5. **Click "Create Web Service"**

### 3.3 Desplegar Frontend (Next.js)

1. **Click "+ New"** → **Web Service**
2. **Conectar GitHub**: Buscar `tienda-electrodomesticos`
3. **Configuración**:
   - **Name**: `tienda-web`
   - **Region**: Igual que BD y API
   - **Branch**: `main`
   - **Root Directory**: `tienda-frontend`
   - **Environment**: Node
   - **Build Command**: 
     ```
     npm install && npm run build
     ```
   - **Start Command**:
     ```
     npm run start
     ```

4. **Environment Variables** (Click "Add Environment Variable"):
   ```
   NEXT_PUBLIC_API_URL=https://tienda-api.onrender.com/api/v1
   NODE_ENV=production
   ```

5. **Click "Create Web Service"**

---

## Paso 4: Esperar Despliegue ⏳

- **PostgreSQL**: Inmediato (ya está listo)
- **Backend Django**: ~3 minutos (verás "Building..." → "Deploying..." → "Live")
- **Frontend Next.js**: ~3-4 minutos (igual que backend)

**Total**: ~5 minutos de espera

---

## Paso 5: Acceder a tu Demo 🎉

Una vez que ambos estén "Live" en Render:

- **Frontend**: https://tienda-web.onrender.com
- **Backend API**: https://tienda-api.onrender.com/api/v1
- **Admin Django**: https://tienda-api.onrender.com/admin

---

## Paso 6: Crear Usuario Admin (Opcional)

En Render dashboard, click en servicio `tienda-api`:

1. **Shell** (esquina superior derecha)
2. Ejecutar:
   ```bash
   python manage.py createsuperuser
   ```
3. Seguir prompts (usuario: admin, contraseña: la que prefieras)

Acceder a: https://tienda-api.onrender.com/admin

---

## ✅ Checklist Final

- [ ] Repositorio GitHub creado
- [ ] Código pusheado a GitHub
- [ ] PostgreSQL creada en Render
- [ ] Backend deployado (Live)
- [ ] Frontend deployado (Live)
- [ ] Testear https://tienda-web.onrender.com
- [ ] Testear https://tienda-api.onrender.com/api/v1/products/
- [ ] Usuario admin creado (opcional)

---

## 🚨 Si algo falla

### Backend dice "Build error"
1. Ir a Logs en Render
2. Ver error específico
3. Probablemente: faltan dependencias en `requirements.txt`
4. Solución: Agregar la dependencia faltante y hacer `git push`

### Frontend no carga productos
1. Verificar `NEXT_PUBLIC_API_URL` es correcto
2. Verificar `CORS_ALLOWED_ORIGINS` en backend
3. Limpiar caché del navegador (Ctrl+Shift+Supr)

### Base de datos vacía
En Render shell del backend:
```bash
python load_sample_data.py
```

---

## 💡 Tips Importantes

1. **No commitear `.env`** - Ya está en `.gitignore`
2. **Primero crear BD** - Antes de deployar backend
3. **Verificar URLs** - API_URL en frontend debe ser https (no http)
4. **Esperar a que esté Live** - No acceder mientras dice "Building"

---

## 📞 URLs Finales

Una vez deployado, tendrás:
- **Frontend**: https://tuname-tienda-web.onrender.com
- **Backend**: https://tuname-tienda-api.onrender.com
- **Admin**: https://tuname-tienda-api.onrender.com/admin

---

**¡Listo! Tu demo está en internet y lista para mostrar! 🚀**

Tiempo total estimado: **10-15 minutos**
