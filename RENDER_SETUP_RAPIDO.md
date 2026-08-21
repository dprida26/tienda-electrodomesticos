# ⚡ Setup Rápido del Web Service en Render

Como ya tienes la BD PostgreSQL configurada, solo falta crear el Web Service. Sigue estos pasos exactos:

## 1️⃣ Conectar tu Repositorio a Render

1. Ve a [https://dashboard.render.com](https://dashboard.render.com)
2. Haz clic en **"New +"** (esquina superior derecha)
3. Selecciona **"Web Service"**
4. Elige **"Build and deploy from a Git repository"**
5. Conecta tu cuenta de GitHub (si no lo has hecho)
6. Selecciona el repositorio: **`Tienda-electrodomesticos`**
7. Elige la rama: **`main`** (o `master`)

## 2️⃣ Configurar el Web Service

En el formulario que aparece, llena así:

| Campo | Valor |
|-------|-------|
| **Name** | `tienda-electrodomesticos-api` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput` |
| **Start Command** | `gunicorn config.wsgi:application` |
| **Plan** | Free |

## 3️⃣ Variables de Entorno (Copiar y Pegar)

Desplázate hasta la sección **"Environment"** y agrega estas variables:

### Opción A: Copiar desde aquí

```
DEBUG=False
SECRET_KEY=django-insecure-abcdefghijklmnopqrstuvwxyz1234567890
PYTHON_VERSION=3.11
ALLOWED_HOSTS=*.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://*.onrender.com,http://localhost:3000,http://localhost:3001
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Opción B: Generar un SECRET_KEY único (RECOMENDADO)

1. Abre PowerShell en tu máquina
2. Ejecuta:
   ```powershell
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
3. Copia el resultado (ej: `django-insecure-k#0$_9@#...`)
4. Usa ese valor en `SECRET_KEY`

## 4️⃣ Conectar la Base de Datos

Aún en **"Environment"**, agrega:

```
DATABASE_URL=<PEGA_AQUI_LA_URL_DE_TU_BD>
```

**¿De dónde sacar la DATABASE_URL?**

1. Ve a tu BD PostgreSQL en Render (en el Dashboard)
2. Busca la sección **"Connections"**
3. Copia la **"Internal Database URL"** (no la externa)
4. Pégala en la variable `DATABASE_URL` del Web Service

**Se ve así:**
```
DATABASE_URL=postgresql://tienda_user:password123@tienda-db.c123abc.internal:5432/tienda_db
```

## 5️⃣ Deploy

1. Revisa que todo esté correcto
2. Haz clic en **"Create Web Service"** (esquina inferior derecha)
3. Espera 5-10 minutos mientras Render hace el build

## 6️⃣ Verificar que Funciona

1. En el Dashboard, busca tu Web Service
2. Espera a que el estado sea **"Live"** (verde)
3. Haz clic en la URL azul que aparece en la esquina superior derecha
4. Deberías ver la interfaz de Django REST Framework

## ✅ Checklist Final

- [ ] Web Service creado con el nombre correcto
- [ ] Build Command copiado exactamente
- [ ] Start Command: `gunicorn config.wsgi:application`
- [ ] SECRET_KEY configurado (único y seguro)
- [ ] DATABASE_URL pegado desde la BD PostgreSQL
- [ ] ALLOWED_HOSTS y CORS_ALLOWED_ORIGINS configurados
- [ ] Variables de seguridad en True
- [ ] Deploy completado sin errores

## 🆘 Si Algo Falla

### "Error: Module not found"
→ Revisa que `requirements.txt` esté en la raíz del proyecto

### "Cannot connect to database"
→ Espera 2-3 minutos a que la BD se inicialice completamente, luego redeploy

### "Application Error"
→ Abre los Logs del Web Service y busca el error específico

### "502 Bad Gateway"
→ El build probablemente falló. Revisa los Logs en Render Dashboard

---

**¡Una vez que esté Live, tu app estará en producción! 🚀**
