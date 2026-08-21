# Agente de Notificaciones Diarias

Agente inteligente que lee automáticamente tus correos de Gmail y notificaciones de LinkedIn, compilando un informe PDF diario con resúmenes y descripciones.

## Características

- 📧 **Integración con Gmail**: Lee correos nuevos usando la API oficial
- 💼 **Integración con LinkedIn**: Captura notificaciones de actividad
- 📄 **Reportes en PDF**: Genera reportes formateados con dos secciones (Correos y LinkedIn)
- ⏰ **Ejecución automática**: Se ejecuta diariamente a la hora configurada
- 🔐 **Seguro**: Usa OAuth2 para autenticación

## Estructura del Proyecto

```
agente-notificaciones-diarias/
├── src/
│   ├── agent/              # Lógica principal del agente
│   ├── config/             # Configuración (variables de entorno)
│   ├── services/           # Servicios para Gmail, LinkedIn, reportes
│   ├── scheduler/          # Programación de tareas diarias
│   ├── types/              # Interfaces TypeScript
│   └── index.ts            # Punto de entrada
├── reports/                # Reportes PDF generados
├── .env.example            # Plantilla de variables de entorno
├── package.json
├── tsconfig.json
└── README.md
```

## Requisitos

- Node.js 18+
- npm o yarn
- Credenciales de Google Cloud (OAuth2)
- Token de acceso de LinkedIn API

## Instalación

```bash
# Clonar o descargar el proyecto
cd agente-notificaciones-diarias

# Instalar dependencias
npm install

# Crear archivo .env basado en .env.example
cp .env.example .env
```

## Configuración

### 1. Gmail OAuth2

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto
3. Habilita la API de Gmail
4. Crea credenciales OAuth2 (Desktop Application)
5. Descarga las credenciales como JSON
6. Completa `.env` con:
   - `GMAIL_CLIENT_ID`
   - `GMAIL_CLIENT_SECRET`
   - `GMAIL_REDIRECT_URI` (default: `http://localhost:3000/oauth/callback`)
   - `GMAIL_USER_EMAIL` (tu email de Gmail)

### 2. LinkedIn API

1. Ve a [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Crea una aplicación
3. Solicita acceso a la API de notificaciones (si está disponible)
4. Completa `.env` con:
   - `LINKEDIN_CLIENT_ID`
   - `LINKEDIN_CLIENT_SECRET`
   - `LINKEDIN_ACCESS_TOKEN`

### 3. Configuración General

```env
SCHEDULE_TIME=08:00              # Hora diaria de ejecución (HH:MM)
REPORT_OUTPUT_DIR=./reports      # Directorio donde guardar PDFs
NODE_ENV=production              # development o production
```

## Uso

### Desarrollo

```bash
# Ejecutar con modo desarrollo (generará un reporte de prueba)
DEV_MODE=true npm run dev

# O solo observar cambios
npm run dev
```

### Producción

```bash
# Compilar TypeScript
npm run build

# Ejecutar
npm start
```

### Generar reporte manualmente

Puedes modificar `src/index.ts` para agregar una ruta HTTP que genere reportes bajo demanda:

```typescript
// Ejemplo con Express
import express from 'express';

const app = express();
const agent = new Agent();

app.get('/api/generate-report', async (req, res) => {
  const reportPath = await agent.generateDailyReport();
  res.download(reportPath);
});

app.listen(3000);
```

## Estructura del Reporte PDF

El reporte generado tiene dos secciones principales:

### 📧 Sección de Correos
- Asunto del correo
- Remitente
- Fecha y hora
- Fragmento/resumen del contenido
- Cantidad total de correos nuevos

### 💼 Sección de LinkedIn
- Tipo de notificación (comentario, reacción, conexión, etc.)
- Persona que realizó la acción
- Fecha y hora
- Descripción de la acción
- Enlace a la notificación (si aplica)
- Cantidad total de notificaciones

## Limitaciones Conocidas

### LinkedIn
- La API v2 de LinkedIn tiene restricciones en cuanto a acceso a notificaciones
- Actualmente el agente solo captura notificaciones a través del endpoint disponible
- Para mejor funcionalidad, se podría implementar web scraping (ver `getNotificationsViaScraping()`)

### Gmail
- Solo lee correos con acceso a `gmail.readonly`
- No puede enviar correos ni modificar bandeja

## Variables de Entorno Disponibles

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `GMAIL_CLIENT_ID` | ID del cliente OAuth de Google | ✅ |
| `GMAIL_CLIENT_SECRET` | Secreto del cliente OAuth de Google | ✅ |
| `GMAIL_REDIRECT_URI` | URI de redirección OAuth | ✅ |
| `GMAIL_USER_EMAIL` | Tu email de Gmail | ✅ |
| `LINKEDIN_CLIENT_ID` | ID del cliente LinkedIn | ✅ |
| `LINKEDIN_CLIENT_SECRET` | Secreto del cliente LinkedIn | ✅ |
| `LINKEDIN_ACCESS_TOKEN` | Token de acceso LinkedIn | ✅ |
| `SCHEDULE_TIME` | Hora de ejecución (HH:MM) | ❌ (default: 08:00) |
| `REPORT_OUTPUT_DIR` | Directorio de reportes | ❌ (default: ./reports) |
| `NODE_ENV` | Ambiente (development/production) | ❌ |

## Próximas Mejoras

- [ ] Interfaz web para ver reportes generados
- [ ] Soporte para enviar reportes por email automáticamente
- [ ] Webhooks para integraciones con Slack/Teams
- [ ] Mejor soporte para notificaciones de LinkedIn (web scraping)
- [ ] Dashboard con estadísticas históricas
- [ ] Soporte multilingüe

## Troubleshooting

### Error: "Please visit [authUrl] and provide the authorization code"

Este error indica que Gmail necesita autenticación. Debes:
1. Visitar la URL proporcionada
2. Autorizar la aplicación
3. Copiar el código de autorización
4. Ejecutar: `agent.setGmailTokenFromCode(code)`

### Error: "ENOENT: no such file or directory, 'reports'"

La carpeta de reportes no existe. Se crea automáticamente o ejecuta:
```bash
mkdir reports
```

### Token de LinkedIn inválido

Verifica que:
1. El token no haya expirado
2. Las credenciales sean correctas
3. La aplicación tenga permisos suficientes

## Licencia

MIT

## Autor

Creado con ❤️ para automatizar la gestión de notificaciones diarias
