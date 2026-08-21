# 📋 Checklist de Deployment en Render.com

## ✅ Preparación Completada

Todo está listo para publicar tu aplicación Django en Render.com. Aquí está lo que se ha configurado:

### Archivos Creados/Modificados

- ✅ **render.yaml** — Configuración de deploy automatizado con Render
- ✅ **DEPLOY_RENDER.md** — Guía completa paso a paso
- ✅ **requirements.txt** — Agregados gunicorn y whitenoise
- ✅ **config/settings.py** — Configuración para PostgreSQL y producción
- ✅ **.env.production.example** — Template de variables de entorno

## 🚀 Próximos Pasos

### Paso 1: Preparar tu Repositorio Git

Si aún no has pusheado a un repositorio remoto (GitHub, GitLab, Gitea):

```bash
# Desde la carpeta del proyecto
cd "c:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\Tienda electrodomesticos"

# Ver el status
git status

# Hacer push a tu rama main
git push origin main
```

**💡 Tip:** Si no tienes un repositorio remoto, crea uno en [GitHub](https://github.com):
1. Crea un nuevo repositorio (sin inicializar)
2. Sigue las instrucciones para agregar el remoto:
   ```bash
   git remote add origin https://github.com/tu-usuario/tu-repo.git
   git branch -M main
   git push -u origin main
   ```

### Paso 2: Acceder a Render.com

1. Ve a [https://render.com](https://render.com)
2. Crea una cuenta (o inicia sesión si ya tienes)
3. Ve al [Dashboard](https://dashboard.render.com)

### Paso 3: Crear Web Service

1. Haz clic en **"New +"** → **"Web Service"**
2. Selecciona **"Build and deploy from a Git repository"**
3. Conecta tu cuenta de GitHub/GitLab
4. Elige el repositorio donde está tu código

### Paso 4: Configurar el Servicio

**Nombre del servicio:**
```
tienda-electrodomesticos-api
```

**Rama:** `main`

**Build Command (debería completarse automáticamente):**
```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

**Start Command (debería completarse automáticamente):**
```
gunicorn config.wsgi:application
```

**Plan:** Elige "Free" para empezar

### Paso 5: Crear Base de Datos PostgreSQL

1. Desde el Dashboard, haz clic en **"New +"** → **"PostgreSQL"**
2. Llena los datos:
   - **Name:** `tienda-db`
   - **Database:** `tienda_db`
   - **User:** `tienda_user`
   - **Plan:** Free
3. Haz clic en **"Create Database"**
4. **¡IMPORTANTE!** Copia la `Database URL` (necesitarás en el siguiente paso)

### Paso 6: Configurar Variables de Entorno

En el Web Service que creaste, en la sección **"Environment"**:

**Agrega estas variables:**

```
DEBUG=False
SECRET_KEY=<GENERA_UNA_NUEVA_SEGURA>
PYTHON_VERSION=3.11
ALLOWED_HOSTS=*.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://<tu-app-name>.onrender.com,http://localhost:3000
DATABASE_URL=<PEGA_LA_URL_DE_LA_BD_POSTGRESQL>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

**¿Cómo generar `SECRET_KEY`?**

Opción 1 - En PowerShell:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Opción 2 - Online (rápido):
Usa un generador online como [djecrety.ir](https://djecrety.ir)

**¿De dónde saco `<tu-app-name>`?**

Es el nombre que Render asigna a tu Web Service. Por ejemplo: `tienda-electrodomesticos-api-a1b2c.onrender.com`

### Paso 7: Deploy

1. Revisa todas las configuraciones
2. Haz clic en el botón **"Deploy"** (parte superior derecha)
3. **Espera 5-10 minutos** mientras Render hace el build
4. Mira los **Logs** para seguir el progreso

### Paso 8: Verificar que Funciona

Una vez que el deploy termine (verás "Live"):

1. Copia la URL que Render genera (ej: `https://tienda-electrodomesticos-api-a1b2c.onrender.com`)
2. Abre en el navegador:
   ```
   https://tienda-electrodomesticos-api-a1b2c.onrender.com/api/v1/
   ```
3. Deberías ver la interfaz de Django REST Framework

## 🔧 Si Algo Sale Mal

### Error: "Build failed"

**Causa más común:** Variables de entorno faltantes

**Solución:**
1. Ve a los logs del deploy
2. Busca qué variable falta
3. Agrega la variable en la sección "Environment"
4. Haz clic en **"Manual Deploy"** → **"Deploy Latest"**

### Error: "Application Error"

**Causa:** La BD no está lista o `DATABASE_URL` es incorrecto

**Solución:**
1. Espera 2-3 minutos a que la BD se inicialice completamente
2. Verifica que `DATABASE_URL` sea correcto (cópialo nuevamente desde la BD)
3. Haz un nuevo deploy

### Error: "Cannot connect to database"

**Causa:** La BD necesita más tiempo para iniciarse

**Solución:**
1. Espera 3-5 minutos
2. Ve a la BD PostgreSQL en Render
3. Verifica que el status sea "Available" (no "Creating")
4. Haz un nuevo deploy del Web Service

### Los logs dicen "ModuleNotFoundError"

**Solución:**
1. Verifica que `requirements.txt` está en la raíz del proyecto
2. Asegúrate de haber hecho commit de `requirements.txt`
3. Haz un nuevo push y deploy

## 📚 Documentación Útil

- **Guía completa:** Abre `DEPLOY_RENDER.md` en este proyecto
- **Dashboard de Render:** https://dashboard.render.com
- **Docs de Render:** https://render.com/docs

## ✨ Próximos Pasos Opcionales

Una vez que esté deployado:

1. **Dominio personalizado** — Usa tu propio dominio en lugar de `onrender.com`
2. **CI/CD con GitHub Actions** — Tests automáticos antes de cada deploy
3. **Monitoreo** — Configura alertas de errores
4. **Backups** — Configura backups automáticos de la BD

## 🎯 Resumen Rápido

```
1. Push a GitHub ✅
2. Crear Web Service en Render
3. Crear BD PostgreSQL en Render
4. Agregar variables de entorno
5. Hacer deploy
6. ¡Listo! 🚀
```

---

**¿Necesitas ayuda?** Consulta `DEPLOY_RENDER.md` para más detalles o la [documentación de Render](https://render.com/docs).
