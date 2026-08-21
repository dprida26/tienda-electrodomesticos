# 🎯 Próximos Pasos para Completar Deploy en Render

## Estado Actual ✅

- ✅ Código Django actualizado y listo para producción
- ✅ Base de Datos PostgreSQL configurada en Render
- ✅ Documentación completa creada
- ⏳ Web Service pendiente de crear

## Lo Que Falta ⏳

Solo necesitas configurar el **Web Service** en Render. Todo lo demás está automatizado.

---

## 📋 PASO A PASO (Toma 5 minutos)

### Paso 1: Conectar tu Repositorio GitHub a Render

Si aún no has conectado, haz esto:

1. **Crear repositorio en GitHub** (si no lo tienes):
   - Ve a [github.com/new](https://github.com/new)
   - Nombre: `tienda-electrodomesticos`
   - Descripción: `Sistema de gestión de tienda con API REST`
   - Elige "Public" o "Private"
   - Haz clic en "Create repository"

2. **Configurar remoto local**:
   ```powershell
   cd "c:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\Tienda electrodomesticos"
   
   # Agregar el remoto (reemplaza tu-usuario y tu-repo con los reales)
   git remote add origin https://github.com/tu-usuario/tienda-electrodomesticos.git
   
   # Cambiar rama principal a main (si GitHub lo requiere)
   git branch -M main
   
   # Push de todo el código
   git push -u origin main
   ```

3. **Verificar que funcionó**:
   ```powershell
   git remote -v
   # Debería mostrar:
   # origin  https://github.com/tu-usuario/tienda-electrodomesticos.git (fetch)
   # origin  https://github.com/tu-usuario/tienda-electrodomesticos.git (push)
   ```

### Paso 2: Crear el Web Service en Render

1. Ve a [https://dashboard.render.com](https://dashboard.render.com)
2. Haz clic en **"New +"** → **"Web Service"**
3. Selecciona **"Build and deploy from a Git repository"**
4. **Conecta GitHub** (si no lo has hecho)
5. Selecciona el repositorio: **`tienda-electrodomesticos`**
6. Rama: **`main`**

### Paso 3: Configurar el Web Service

Usa estos valores exactamente:

| Campo | Valor |
|-------|-------|
| Name | `tienda-electrodomesticos-api` |
| Environment | Python 3 |
| Build Command | `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput` |
| Start Command | `gunicorn config.wsgi:application` |
| Plan | Free |

### Paso 4: Generar SECRET_KEY Seguro

**Opción A: Script PowerShell (más fácil)**
```powershell
cd "c:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\Tienda electrodomesticos"
.\generate-secret-key.ps1
```
Se copiará automáticamente al portapapeles.

**Opción B: Comando directo**
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Opción C: Online**
Visita [djecrety.ir](https://djecrety.ir)

### Paso 5: Obtener DATABASE_URL

1. Ve a Render Dashboard
2. Ve a tu BD PostgreSQL: **`tienda-db`**
3. Busca sección **"Connections"**
4. Copia **"Internal Database URL"** (la que dice .internal)
5. Se verá así: `postgresql://tienda_user:password@tienda-db.c123abc.internal:5432/tienda_db`

### Paso 6: Agregar Variables de Entorno

En el formulario del Web Service, sección **"Environment"**, agrega estas 9 variables:

```
DEBUG=False
SECRET_KEY=<PEGA_TU_SECRET_KEY_AQUI>
PYTHON_VERSION=3.11
ALLOWED_HOSTS=*.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://*.onrender.com,http://localhost:3000,http://localhost:3001
DATABASE_URL=<PEGA_TU_DATABASE_URL_AQUI>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

**📌 Importante:**
- Reemplaza `<PEGA_TU_SECRET_KEY_AQUI>` con el valor que generaste
- Reemplaza `<PEGA_TU_DATABASE_URL_AQUI>` con la URL de tu BD

### Paso 7: Deploy

1. Haz clic en **"Create Web Service"** (parte inferior derecha)
2. **Espera 5-10 minutos** mientras Render hace el build
3. Ver progreso en **"Logs"**

### Paso 8: Verificar

Una vez que veas **"Live"** (en verde):

1. Haz clic en la URL azul que aparece en la parte superior
2. Deberías ver: **"Django REST Framework - API"**

---

## 📚 Documentos de Referencia

- **RENDER_SETUP_RAPIDO.md** — Guía completa paso a paso
- **RENDER_VARIABLES.md** — Detalles de cada variable de entorno
- **DEPLOY_RENDER.md** — Guía exhaustiva con troubleshooting
- **generate-secret-key.ps1** — Script para generar SECRET_KEY

---

## ⚡ Resumen Rápido

```
1. Conectar GitHub a Render
2. Crear Web Service
3. Generar SECRET_KEY
4. Obtener DATABASE_URL
5. Agregar 9 variables de entorno
6. Hacer Deploy
7. ¡Listo! ✨
```

---

## 🆘 Problemas Comunes

### "Authentication failed"
→ Verifica que tienes permisos en el repositorio de GitHub

### "Cannot connect to database"
→ Copia nuevamente la DATABASE_URL desde tu BD PostgreSQL

### "Build failed"
→ Revisa los Logs en Render. Probablemente falte una variable.

### "502 Bad Gateway"
→ El build falló. Ve a Logs y busca el error específico.

---

## ✨ Una Vez que Esté Deployado

- Tu API estará en: `https://tienda-electrodomesticos-api-xxxxx.onrender.com`
- Cada push a `main` en GitHub dispara un nuevo deploy automático
- Los logs se ven en tiempo real en el Dashboard

---

**¡Estás a 5 minutos de tener tu app en producción! 🚀**

¿Necesitas ayuda en algún paso? Abre los archivos de referencia en la carpeta del proyecto.
