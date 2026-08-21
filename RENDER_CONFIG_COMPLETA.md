# 🎯 Configuración Completa para Render - LISTA PARA COPIAR Y PEGAR

## ✅ Datos Ya Preparados

Tu repositorio: `https://github.com/dprida26/tienda-electrodomesticos`

Tu base de datos está configurada.

---

## 🚀 PASO 1: Generar SECRET_KEY

Ejecuta este comando en PowerShell:

```powershell
cd "c:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\Tienda electrodomesticos"
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copia el resultado.** Se verá algo como:
```
django-insecure-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

## 🔧 PASO 2: Crear Web Service en Render

### 2.1 Ir a Render Dashboard

1. Ve a: https://dashboard.render.com
2. Haz clic en **"New +"** (esquina superior derecha)
3. Selecciona **"Web Service"**
4. Elige **"Build and deploy from a Git repository"**

### 2.2 Conectar Repositorio

1. Haz clic en **"Connect account"** (si no has conectado GitHub)
2. Autoriza Render en GitHub
3. Busca y selecciona: **`tienda-electrodomesticos`**
4. Elige rama: **`main`**

### 2.3 Configurar Servicio Web

Llena los campos con estos valores **exactos**:

```
Name: tienda-electrodomesticos-api
Environment: Python 3
Build Command: pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
Start Command: gunicorn config.wsgi:application
Plan: Free
```

---

## 🔐 PASO 3: Agregar Variables de Entorno

En la sección **"Environment"**, agrega estas 9 variables.

Para cada una:
1. Haz clic en **"Add Environment Variable"**
2. Copia el **Key** y el **Value**
3. Pega en los campos correspondientes
4. Haz clic en **"Add"**

### Variables a Agregar:

#### Variable 1
```
Key: DEBUG
Value: False
```

#### Variable 2
```
Key: SECRET_KEY
Value: <PEGA_EL_RESULTADO_DEL_PASO_1_AQUI>
```

Ejemplo (reemplaza con el tuyo):
```
Key: SECRET_KEY
Value: django-insecure-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

#### Variable 3
```
Key: PYTHON_VERSION
Value: 3.11
```

#### Variable 4
```
Key: ALLOWED_HOSTS
Value: *.onrender.com,localhost,127.0.0.1
```

#### Variable 5
```
Key: CORS_ALLOWED_ORIGINS
Value: https://*.onrender.com,http://localhost:3000,http://localhost:3001
```

#### Variable 6 (⭐ IMPORTANTE)
```
Key: DATABASE_URL
Value: postgresql://tienda_db_48e5_user:TgJXyAjuqjuUeQK5B9FgXc82P9w7rpMt@dpg-da3mkg0u01pc73butaeg-a/tienda_db_48e5
```

#### Variable 7
```
Key: SECURE_SSL_REDIRECT
Value: True
```

#### Variable 8
```
Key: SESSION_COOKIE_SECURE
Value: True
```

#### Variable 9
```
Key: CSRF_COOKIE_SECURE
Value: True
```

---

## ✨ PASO 4: Hacer Deploy

1. Revisa que todas las 9 variables estén agregadas
2. Haz clic en **"Create Web Service"** (parte inferior derecha)
3. **Espera 5-10 minutos** mientras Render construye la app
4. Mira el progreso en **"Logs"**

---

## ✅ PASO 5: Verificar que Funciona

Una vez que veas **"Live"** (en verde):

1. Haz clic en la **URL azul** que aparece en la parte superior
2. Deberías ver la interfaz de Django REST Framework
3. Navega a `/api/v1/` para ver los endpoints disponibles

---

## 📋 Checklist Final

- [ ] SECRET_KEY generado y copiado
- [ ] Hice clic en "New +" → "Web Service"
- [ ] Conecté mi repositorio GitHub
- [ ] Configuré Build Command
- [ ] Configuré Start Command
- [ ] Agregué las 9 variables de entorno
- [ ] Hice clic en "Create Web Service"
- [ ] El deploy completó (dice "Live")
- [ ] La URL funciona y veo la API

---

## 🆘 Problemas?

### "Build failed"
→ Revisa los Logs. Probablemente falta una variable.

### "Cannot connect to database"
→ La DATABASE_URL es: 
```
postgresql://tienda_db_48e5_user:TgJXyAjuqjuUeQK5B9FgXc82P9w7rpMt@dpg-da3mkg0u01pc73butaeg-a/tienda_db_48e5
```
Verifica que esté exacto sin espacios.

### "502 Bad Gateway"
→ El build falló. Mira los Logs en Render.

### "Application Error"
→ Espera 2-3 minutos, a veces tarda en iniciar.

---

## 🎉 ¡Listo!

Tu API estará en: `https://tienda-electrodomesticos-api-xxxxx.onrender.com`

¡Cada push a GitHub dispara un nuevo deploy automático! 🚀
