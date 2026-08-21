# Guía de Publicación en Render.com

Esta guía te ayudará a publicar la aplicación Django en Render.com de forma segura y rápida.

## Requisitos Previos

1. Cuenta en [Render.com](https://render.com)
2. Repositorio Git (GitHub, GitLab o Gitea)
3. El código debe estar en la rama `main` o `master`

## Pasos para Deployar

### 1. Preparar el Repositorio

```bash
# Asegúrate de que todos los cambios estén commiteados
git status

# Haz un push a tu repositorio remoto
git push origin main
```

### 2. Crear un Nuevo Web Service en Render

1. Ve a [https://dashboard.render.com](https://dashboard.render.com)
2. Haz clic en **"New +"** → **"Web Service"**
3. Elige **"Build and deploy from a Git repository"**
4. Conecta tu cuenta de GitHub/GitLab
5. Selecciona el repositorio `Tienda-electrodomesticos`

### 3. Configurar el Web Service

En la página de configuración, llena los campos así:

| Campo | Valor |
|-------|-------|
| **Name** | `tienda-electrodomesticos-api` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput` |
| **Start Command** | `gunicorn config.wsgi:application` |
| **Plan** | Free (o Premium si lo deseas) |

### 4. Crear la Base de Datos PostgreSQL

1. Desde el dashboard, haz clic en **"New +"** → **"PostgreSQL"**
2. Llena los detalles:
   - **Name**: `tienda-db`
   - **Database**: `tienda_db`
   - **User**: `tienda_user`
   - **Plan**: Free (o Premium)
3. Haz clic en **"Create Database"**
4. Guarda la `Database URL` que te proporciona

### 5. Configurar Variables de Entorno

En el formulario del Web Service, en la sección **"Environment"**:

**Variables a Agregar:**

```
DEBUG=False
SECRET_KEY=<genera-una-nueva-clave-segura>
PYTHON_VERSION=3.11
ALLOWED_HOSTS=*.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://<tu-app>.onrender.com,http://localhost:3000
DATABASE_URL=<copia-la-URL-de-tu-base-de-datos>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

**Notas importantes:**

- El `SECRET_KEY` debe ser único y seguro. Puedes generarlo con:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- Reemplaza `<tu-app>` con el nombre de tu aplicación en Render
- La `DATABASE_URL` viene automáticamente de la BD PostgreSQL que creaste

### 6. Generar una Clave Segura

```bash
# En tu máquina local
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
# Copia el resultado y úsalo como SECRET_KEY
```

### 7. Deploy

1. Haz clic en **"Deploy"**
2. Render comenzará a:
   - Clonar el repositorio
   - Instalar dependencias (`pip install -r requirements.txt`)
   - Ejecutar migraciones (`python manage.py migrate`)
   - Recopilar archivos estáticos (`python manage.py collectstatic`)
   - Iniciar la aplicación con Gunicorn

### 8. Verificar el Deploy

1. Ve a los **"Logs"** para ver el progreso
2. Busca un mensaje como: `"Uvicorn running on http://0.0.0.0:10000"`
3. Una vez completado, tu app estará disponible en:
   ```
   https://<tu-app>.onrender.com
   ```

## Actualizar la Aplicación

Cada vez que hagas cambios:

```bash
# Haz commit
git add .
git commit -m "feat: tu cambio aquí"

# Push a main
git push origin main
```

Render detectará automáticamente los cambios y hará un nuevo deploy. Puedes ver el progreso en el dashboard.

## Troubleshooting

### El deploy falla con error de base de datos

**Problema:** `FATAL: no pg_hba.conf entry for...`

**Solución:**
1. Asegúrate de que la BD PostgreSQL está completamente creada (puede tomar minutos)
2. Verifica que el `DATABASE_URL` sea correcto en las variables de entorno
3. Espera 1-2 minutos antes de hacer un nuevo deploy

### Error: "ModuleNotFoundError: No module named 'whitenoise'"

**Solución:**
```bash
# Asegúrate de que requirements.txt tiene gunicorn y whitenoise
pip install -r requirements.txt
git add requirements.txt
git commit -m "chore: agregar whitenoise a requirements"
git push origin main
```

### La aplicación funciona pero 404 en rutas dinámicas

**Solución:** Configura el Web Service para permitir fallback a index.html:
- En Render, agrega a **Routes**: `/*` → `200`

### Archivos estáticos no cargan (CSS/JS)

**Problema:** WhiteNoise no está sirviendo archivos correctamente

**Solución:**
1. Asegúrate de que `STATIC_ROOT` está configurado en `settings.py`
2. El comando `python manage.py collectstatic --noinput` debe ejecutarse sin errores
3. Verifica los logs en Render

### Error de conexión con la base de datos en producción

**Problema:** `could not translate host name "..." to address`

**Solución:**
1. Verifica que el `DATABASE_URL` es correcto
2. Si usa otro proveedor de BD, asegúrate de que la contraseña no tiene caracteres especiales sin escapar
3. Usa URL encoding para caracteres especiales: `%40` para `@`, `%3A` para `:`, etc.

## Conectar a la Base de Datos desde Local (Opcional)

Para conectarte a la BD de Render desde tu máquina local:

```bash
# Instala psql
brew install postgresql  # macOS
sudo apt install postgresql-client  # Ubuntu

# Conecta usando la DATABASE_URL
psql "postgresql://user:pass@host:5432/dbname"
```

## Pasos Siguientes

1. ✅ Configura un dominio personalizado (opcional)
   - En Render Dashboard → Custom Domain
   - Apunta tus registros DNS a Render

2. ✅ Configura GitHub Actions para CI/CD (opcional)
   - Crea `.github/workflows/deploy.yml`
   - Ejecuta tests antes de deployar

3. ✅ Habilita monitoreo y logs
   - Render Dashboard → Logs
   - Configura alertas de errores

## Referencias Útiles

- [Documentación oficial de Render](https://render.com/docs)
- [Django en Render](https://render.com/docs/deploy-django)
- [PostgreSQL en Render](https://render.com/docs/databases)
- [Variables de entorno en Render](https://render.com/docs/environment-variables)

---

**¡Tu aplicación está lista para producción! 🚀**
