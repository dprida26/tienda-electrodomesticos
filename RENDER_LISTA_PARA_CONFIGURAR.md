# 🎯 RENDER - LISTA PARA CONFIGURAR (COPIAR Y PEGAR)

## ✨ Tu Configuración Está Lista

Todos los datos están preparados. Solo tienes que copiar y pegar en Render.

---

## 📋 DATOS DE TU PROYECTO

```
Repositorio GitHub: https://github.com/dprida26/tienda-electrodomesticos
Base de Datos: Configurada ✅
```

---

## 🚀 PASO 1: Abrir Render y Crear Web Service

1. Ve a: https://dashboard.render.com
2. Haz clic en **"New +"** 
3. Selecciona **"Web Service"**
4. Elige **"Build and deploy from a Git repository"**
5. Conecta GitHub (si no lo hiciste)
6. Selecciona: **`tienda-electrodomesticos`**
7. Rama: **`main`**

---

## 🔧 PASO 2: Configuración del Servicio Web

Copia y pega estos valores exactamente:

### Campo: Name
```
tienda-electrodomesticos-api
```

### Campo: Environment
```
Python 3
```

### Campo: Build Command
```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

### Campo: Start Command
```
gunicorn config.wsgi:application
```

### Campo: Plan
```
Free
```

---

## 🔐 PASO 3: Variables de Entorno (COPIAR Y PEGAR)

En la sección **"Environment"**, agrega estas 9 variables.

**Copia cada línea completa y pégala en Render:**

### Variable 1
```
DEBUG=False
```

### Variable 2 (⭐ SECRET_KEY GENERADO)
```
SECRET_KEY=&pbpyd%$)04q1q$m-92hu6cl1nu7*a1i6eh06fo(ozw6@oy0w_
```

### Variable 3
```
PYTHON_VERSION=3.11
```

### Variable 4
```
ALLOWED_HOSTS=*.onrender.com,localhost,127.0.0.1
```

### Variable 5
```
CORS_ALLOWED_ORIGINS=https://*.onrender.com,http://localhost:3000,http://localhost:3001
```

### Variable 6 (⭐ TU BASE DE DATOS)
```
DATABASE_URL=postgresql://tienda_db_48e5_user:TgJXyAjuqjuUeQK5B9FgXc82P9w7rpMt@dpg-da3mkg0u01pc73butaeg-a/tienda_db_48e5
```

### Variable 7
```
SECURE_SSL_REDIRECT=True
```

### Variable 8
```
SESSION_COOKIE_SECURE=True
```

### Variable 9
```
CSRF_COOKIE_SECURE=True
```

---

## ✅ PASO 4: Deploy

1. Revisa que todas las 9 variables estén
2. Haz clic en **"Create Web Service"**
3. Espera 5-10 minutos
4. Cuando veas **"Live"**, ¡listo! 🎉

---

## 🔗 URLs Finales

Una vez que termine el deploy, tu API estará en:

```
https://tienda-electrodomesticos-api-xxxxx.onrender.com
```

(El `xxxxx` lo asigna Render automáticamente)

---

## 📌 Notas Importantes

✅ El `SECRET_KEY` ya está generado y es único  
✅ El `DATABASE_URL` es el tuyo de PostgreSQL  
✅ Todo está configurado para HTTPS en producción  
✅ Cada push a GitHub hace deploy automático  

---

## 🆘 Si Algo Falla

**Build failed**: Revisa los Logs en Render  
**Cannot connect to database**: DATABASE_URL es correcto  
**502 Bad Gateway**: Espera 2-3 minutos más  

---

## ¿Necesitas más info?

- `RENDER_CONFIG_COMPLETA.md` — Guía detallada paso a paso
- `RENDER_VARIABLES.md` — Explicación de cada variable
- `RENDER_DEPLOYMENT_CHECKLIST.md` — Checklist completo

---

**¡Estás listo! Solo tienes que copiar y pegar. 🚀**
