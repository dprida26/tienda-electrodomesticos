# ⚡ Quick Start - 5 Minutos

Sigue estos pasos para tener el agente funcionando en 5 minutos.

## 1️⃣ Instalar Dependencias (1 min)

```bash
cd agente-notificaciones-diarias
npm install
```

## 2️⃣ Configurar Variables de Entorno (2 min)

### Opción A: Copia rápida (mínimo absoluto)

```bash
cp .env.example .env
```

Luego edita `.env` con tus credenciales (ver abajo).

### Opción B: Paso a paso

Crea un archivo `.env` con:

```env
# Gmail (obligatorio - obtener de Google Cloud Console)
GMAIL_CLIENT_ID=your_id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-xxxxx
GMAIL_REDIRECT_URI=http://localhost:3000/oauth/callback
GMAIL_USER_EMAIL=tu_email@gmail.com

# LinkedIn (obligatorio - obtener de LinkedIn Developers)
LINKEDIN_CLIENT_ID=xxxxx
LINKEDIN_CLIENT_SECRET=xxxxx
LINKEDIN_ACCESS_TOKEN=AQV...

# Configuración (opcional)
SCHEDULE_TIME=08:00
REPORT_OUTPUT_DIR=./reports
NODE_ENV=development
```

## 3️⃣ Ejecutar (1 min)

### Modo Desarrollo (recomendado para probar)

```bash
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

### Modo Producción

```bash
npm run build
npm start
```

## ✅ ¡Listo!

Tu agente ahora:
- ✅ Lee tus correos de Gmail
- ✅ Lee tus notificaciones de LinkedIn
- ✅ Genera un PDF diario con ambos
- ✅ Se ejecuta automáticamente a las 08:00 AM

Los PDFs se guardan en `./reports/`

---

## 🔑 Obtener Credenciales (Paso a Paso)

### Gmail

1. Ve a https://console.cloud.google.com/
2. Crea un nuevo proyecto: "Agente Notificaciones"
3. Habilita "Gmail API"
4. Crea credenciales → "OAuth 2.0 Client ID" → Desktop
5. Descarga el JSON y copia:
   - `client_id` → `GMAIL_CLIENT_ID`
   - `client_secret` → `GMAIL_CLIENT_SECRET`

### LinkedIn

1. Ve a https://www.linkedin.com/developers/
2. Crea una aplicación
3. Ve a "Auth"
4. Copia `Client ID` y `Client Secret`
5. Para el token: [LinkedIn Token Generator](https://www.linkedin.com/developers/tools/oauth/token-generator)

---

## 🐛 Problemas Comunes

### "Token inválido"
→ Revisa que las credenciales estén correctas en `.env`

### "No se conecta a Gmail"
→ Necesitas autorizar OAuth manualmente (verás la URL en los logs)

### "Reportes no se generan"
→ Verifica que `GMAIL_USER_EMAIL` sea correcta

---

## 📚 Documentación Completa

- **Instalación detallada**: [SETUP.md](SETUP.md)
- **Características**: [README.md](README.md)
- **Extender el proyecto**: [EXTENSION.md](EXTENSION.md)
- **Resumen técnico**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

**¿Necesitas ayuda?** Consulta los logs en la terminal o revisa los archivos de documentación.
