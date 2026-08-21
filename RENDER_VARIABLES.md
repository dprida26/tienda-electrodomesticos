# 📝 Variables de Entorno para Render

Estas son las variables que necesitas configurar en Render Dashboard para que tu aplicación funcione.

## Ubicación en Render

1. Dashboard → Tu Web Service → "Environment"
2. Haz clic en "Add Environment Variable"
3. Llena cada una con los valores de abajo

## Variables Requeridas

### 1. DEBUG
```
Key: DEBUG
Value: False
```
*Nunca usar True en producción*

### 2. SECRET_KEY (⭐ IMPORTANTE)
```
Key: SECRET_KEY
Value: <GENERAR_ÚNICO>
```

**Cómo generar:**
```powershell
# En PowerShell desde la carpeta del proyecto
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

O ejecuta el script:
```powershell
.\generate-secret-key.ps1
```

**Ejemplo de valor:**
```
django-insecure-k#0$_9@#k*z#=_kj(9xp0=j&@+_5k$5a!_8c-o!-q=_9@#k*z
```

### 3. PYTHON_VERSION
```
Key: PYTHON_VERSION
Value: 3.11
```

### 4. ALLOWED_HOSTS
```
Key: ALLOWED_HOSTS
Value: *.onrender.com,localhost,127.0.0.1
```

*Render asignará automáticamente tu dominio `xxx.onrender.com`*

### 5. CORS_ALLOWED_ORIGINS
```
Key: CORS_ALLOWED_ORIGINS
Value: https://*.onrender.com,http://localhost:3000,http://localhost:3001
```

*Permite peticiones desde tu app web frontend*

### 6. DATABASE_URL (⭐ IMPORTANTE)
```
Key: DATABASE_URL
Value: postgresql://tienda_user:password@host:5432/tienda_db
```

**¿De dónde sacar?**
1. Ve a tu BD PostgreSQL en Render
2. Sección "Connections"
3. Copia "Internal Database URL"
4. Pégala aquí

**Ejemplo:**
```
postgresql://tienda_user:abc123xyz@tienda-db.c123abc.internal:5432/tienda_db
```

### 7. SECURE_SSL_REDIRECT
```
Key: SECURE_SSL_REDIRECT
Value: True
```

### 8. SESSION_COOKIE_SECURE
```
Key: SESSION_COOKIE_SECURE
Value: True
```

### 9. CSRF_COOKIE_SECURE
```
Key: CSRF_COOKIE_SECURE
Value: True
```

## Copiar Todo (Opción Fácil)

Si tu BD está lista, copia esto y reemplaza `DATABASE_URL`:

```
DEBUG=False
SECRET_KEY=<TU_SECRET_KEY_AQUI>
PYTHON_VERSION=3.11
ALLOWED_HOSTS=*.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://*.onrender.com,http://localhost:3000,http://localhost:3001
DATABASE_URL=<PEGA_TU_DATABASE_URL_AQUI>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Generar SECRET_KEY Único

### Opción 1: PowerShell (Recomendado)

```powershell
# Abre PowerShell en la carpeta del proyecto
cd "c:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\Tienda electrodomesticos"

# Genera la clave
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# O ejecuta el script
.\generate-secret-key.ps1
```

### Opción 2: Online (Rápido)
Visita [djecrety.ir](https://djecrety.ir) y genera una clave online.

### Opción 3: Manual
```powershell
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
>>> exit()
```

## Verificar DATABASE_URL

### Ubicación en Render

1. Dashboard → PostgreSQL (tienda-db)
2. Busca **"Connections"**
3. Selecciona **"Internal Database URL"** (no la externa)
4. Cópiala completa

### Estructura

```
postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE

Ejemplo:
postgresql://tienda_user:abc123xyz@tienda-db.c123abc.internal:5432/tienda_db
```

### Partes

| Parte | Ejemplo | Dónde | 
|-------|---------|-------|
| USERNAME | tienda_user | BD config (nunca cambiar) |
| PASSWORD | abc123xyz | BD config (generado por Render) |
| HOST | tienda-db.c123abc.internal | Render asigna |
| PORT | 5432 | Siempre 5432 para PostgreSQL |
| DATABASE | tienda_db | BD config (nunca cambiar) |

## Después de Configurar

1. ✅ Verifica que todas las 9 variables estén agregadas
2. ✅ Revisa que no hay typos
3. ✅ Haz clic en **"Save Changes"** (esquina inferior)
4. ✅ Tu Web Service se redesplegará automáticamente

## Troubleshooting

### ❌ Error: "Cannot connect to database"
→ Copiar de nuevo `DATABASE_URL` desde la BD (puede haber cambiado)

### ❌ Error: "Invalid SECRET_KEY"
→ Asegúrate de que `SECRET_KEY` no tenga espacios al inicio/final

### ❌ Error: "CORS not working"
→ Verifica que tu frontend URL está en `CORS_ALLOWED_ORIGINS`

### ❌ Aplicación carga pero da 403 CSRF
→ Revisa que `CSRF_COOKIE_SECURE=True` está configurado

---

**📚 Más info:** Consulta `RENDER_SETUP_RAPIDO.md` para los pasos completos.
