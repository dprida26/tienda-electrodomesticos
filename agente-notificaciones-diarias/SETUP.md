# Guía de Setup - Agente de Notificaciones Diarias

## Paso 1: Clonar / Descargar el Proyecto

```bash
cd c:\Users\Administrador\Desktop\AMSA\Personal\Proyectos\ IA
```

## Paso 2: Instalar Dependencias

```bash
npm install
```

## Paso 3: Configurar Gmail OAuth2

### 3.1 Crear Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Haz clic en el selector de proyecto (arriba a la izquierda)
3. Haz clic en "NEW PROJECT"
4. Nombre: `Agente Notificaciones Diarias`
5. Haz clic en "CREATE"

### 3.2 Habilitar la API de Gmail

1. En la barra de búsqueda, busca "Gmail API"
2. Haz clic en "Gmail API"
3. Haz clic en "ENABLE"

### 3.3 Crear Credenciales OAuth2

1. Ve a [Credentials](https://console.cloud.google.com/apis/credentials)
2. Haz clic en "CREATE CREDENTIALS" → "OAuth client ID"
3. Si te pide crear una "OAuth consent screen":
   - Haz clic en "CONFIGURE CONSENT SCREEN"
   - Elige "External"
   - Completa:
     - **App name**: "Agente Notificaciones"
     - **User support email**: Tu email
     - **Developer contact**: Tu email
   - Haz clic en "SAVE AND CONTINUE"
   - En "Scopes": busca "Gmail API" y selecciona `gmail.readonly`
   - Completa los demás pasos
4. Vuelve a "Credentials" → "CREATE CREDENTIALS" → "OAuth client ID"
5. Application type: **Desktop application**
6. Nombre: `Agente Notificaciones`
7. Haz clic en "CREATE"

### 3.4 Descargar Credenciales

1. En Credentials, busca el OAuth 2.0 Client ID que acabas de crear
2. Haz clic en el ícono de descarga
3. Se descargará un archivo JSON con los datos

### 3.5 Completar .env

De las credenciales descargadas, extrae:
- `client_id` → `GMAIL_CLIENT_ID`
- `client_secret` → `GMAIL_CLIENT_SECRET`
- `redirect_uris[0]` → `GMAIL_REDIRECT_URI`

Tu `.env` debe tener:
```env
GMAIL_CLIENT_ID=xxxxx.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-xxxxx
GMAIL_REDIRECT_URI=http://localhost:3000/oauth/callback
GMAIL_USER_EMAIL=tuEmail@gmail.com
```

## Paso 4: Configurar LinkedIn API

### 4.1 Crear Aplicación en LinkedIn

1. Ve a [LinkedIn Developers](https://www.linkedin.com/developers/apps/)
2. Haz clic en "Create app"
3. Completa:
   - **App name**: "Agente Notificaciones Diarias"
   - **LinkedIn Page**: Crea una página si no tienes
   - **App logo**: Carga una imagen (opcional)
   - Acepta términos
4. Haz clic en "Create app"

### 4.2 Obtener Credenciales

1. Ve a tu aplicación creada
2. Haz clic en "Auth"
3. Copia:
   - **Client ID** → `LINKEDIN_CLIENT_ID`
   - **Client secret** → `LINKEDIN_CLIENT_SECRET`

### 4.3 Generar Access Token

Para obtener un access token:

1. Ve a [LinkedIn API Testing Console](https://www.linkedin.com/developers/tools/oauth/token-generator)
2. Selecciona tu aplicación
3. Selecciona permisos necesarios (al menos `r_basic`)
4. Haz clic en "Request access token"
5. Copia el token generado → `LINKEDIN_ACCESS_TOKEN`

**Nota**: Los access tokens de LinkedIn expiran. Necesitarás renovarlos periódicamente.

### 4.4 Actualizar .env

```env
LINKEDIN_CLIENT_ID=xxxxx
LINKEDIN_CLIENT_SECRET=xxxxx
LINKEDIN_ACCESS_TOKEN=AQV...
```

## Paso 5: Completar Configuración General

```env
SCHEDULE_TIME=08:00
REPORT_OUTPUT_DIR=./reports
NODE_ENV=development
```

## Paso 6: Probar la Instalación

```bash
# Modo desarrollo (generará un reporte de prueba)
npm run dev
```

Deberías ver:
```
🚀 Iniciando Agente de Notificaciones Diarias
✅ Gmail autenticado
✅ Planificador iniciado
🧪 Modo desarrollo: generando reporte de prueba...
📊 Generando reporte para...
✅ PDF generado en: ./reports/reporte-diario-2026-04-17.pdf
```

## Paso 7: Ejecutar en Producción

```bash
# Compilar TypeScript
npm run build

# Ejecutar el agente
npm start
```

El agente ahora se ejecutará:
- Diariamente a la hora configurada (08:00)
- Generará un PDF en la carpeta `reports/`
- Continuará ejecutándose hasta que lo detengas (Ctrl+C)

## Solución de Problemas

### Error: "Please visit [authUrl] and provide the authorization code"

Gmail necesita autorización interactiva:
1. Abre la URL en tu navegador
2. Autoriza la aplicación
3. Copia el código de autorización
4. Modifica `src/index.ts` para aceptar el código manualmente

### Error: "ENOENT: no such file or directory"

Las carpetas no existen. Crea manualmente:
```bash
mkdir reports
```

### Error: "Token inválido" en LinkedIn

Los tokens de LinkedIn expiran después de 60 días. Debes:
1. Ir a [LinkedIn Token Generator](https://www.linkedin.com/developers/tools/oauth/token-generator)
2. Generar un nuevo token
3. Actualizar `.env` con el nuevo token

### Los reportes no se generan a la hora programada

Verifica:
1. `SCHEDULE_TIME` está en formato correcto (HH:MM en 24h)
2. El servidor Node.js sigue ejecutándose (`npm start`)
3. Revisa los logs para errores

## Próximos Pasos

1. **Automatizar con Task Scheduler (Windows)**:
   ```bash
   # Crear tarea programada que ejecute npm start
   ```

2. **Integrar con Gmail**: Envía automáticamente el reporte por email
   
3. **Dashboard Web**: Ver reportes históricos en una interfaz

4. **Notificaciones Slack**: Enviá un resumen a Slack diariamente

---

¿Necesitas ayuda? Revisa el [README.md](README.md) para más detalles.
