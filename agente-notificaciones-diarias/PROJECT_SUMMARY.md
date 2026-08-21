# Resumen del Proyecto - Agente de Notificaciones Diarias

## 📋 Descripción General

El **Agente de Notificaciones Diarias** es una aplicación Node.js que automatiza la recopilación y síntesis de notificaciones de múltiples plataformas (Gmail y LinkedIn) en un reporte PDF diario.

**Objetivo Principal**: Mantener al usuario actualizado sobre sus comunicaciones e interacciones importantes sin necesidad de revisar múltiples plataformas manualmente.

## 🎯 Características Principales

### 1. **Integración con Gmail**
- ✅ Lectura de correos nuevos usando Google OAuth2
- ✅ Filtrado por rango de fechas
- ✅ Extracción de: asunto, remitente, contenido, fecha
- ✅ Manejo seguro de tokens

### 2. **Integración con LinkedIn**
- ✅ Obtención de notificaciones de actividad
- ✅ Captura de interacciones (comentarios, reacciones, conexiones)
- ✅ Integración con API oficial

### 3. **Generación de Reportes PDF**
- ✅ Documento estructurado con dos secciones (Correos y LinkedIn)
- ✅ Diseño profesional y legible
- ✅ Paginación automática
- ✅ Resúmenes concisos de cada elemento

### 4. **Automatización**
- ✅ Ejecución diaria a hora programada
- ✅ Uso de node-schedule para programación
- ✅ Mantenimiento de proceso activo

## 📁 Estructura del Proyecto

```
agente-notificaciones-diarias/
├── src/
│   ├── agent/                  # Lógica principal del agente
│   │   └── index.ts            # Orquestador de servicios
│   ├── config/
│   │   └── env.ts              # Configuración de variables de entorno
│   ├── services/
│   │   ├── gmail.service.ts     # Interacción con Gmail API
│   │   ├── linkedin.service.ts  # Interacción con LinkedIn API
│   │   └── report.service.ts    # Generación de reportes PDF
│   ├── scheduler/
│   │   └── daily-task.ts        # Programación de tareas diarias
│   ├── types/
│   │   └── index.ts             # Interfaces TypeScript
│   ├── utils/
│   │   └── logger.ts            # Sistema de logging
│   └── index.ts                 # Punto de entrada
├── reports/                     # Carpeta donde se guardan PDFs
├── .env.example                 # Variables de entorno (plantilla)
├── .gitignore                   # Archivos a ignorar en Git
├── package.json                 # Dependencias del proyecto
├── tsconfig.json                # Configuración TypeScript
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose para facilitar deployment
├── README.md                    # Documentación principal
├── SETUP.md                     # Guía paso a paso de setup
├── EXTENSION.md                 # Guía de extensión del proyecto
└── PROJECT_SUMMARY.md           # Este archivo
```

## 🔧 Stack Tecnológico

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Runtime | Node.js | 18+ |
| Lenguaje | TypeScript | 5.0+ |
| Gmail | googleapis | 118.0.0 |
| LinkedIn | axios | 1.6.0 |
| Reportes | pdfkit | 0.13.0 |
| Programación | node-schedule | 2.1.1 |
| Validación | zod | 3.22.4 |
| Build | TypeScript Compiler | 5.0+ |
| Dev | tsx | 4.0+ |

## 🚀 Quick Start

### 1. Instalación
```bash
cd agente-notificaciones-diarias
npm install
```

### 2. Configuración
```bash
cp .env.example .env
# Editar .env con credenciales de Google y LinkedIn
```

### 3. Ejecución
```bash
# Desarrollo (modo prueba)
npm run dev

# Producción
npm run build
npm start
```

## 📊 Flujo de Datos

```
┌─────────────────────────────────────────────────────────┐
│              Agente de Notificaciones                     │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
   │   Gmail     │  │  LinkedIn    │  │  Scheduler   │
   │   Service   │  │  Service     │  │  (node-sch)  │
   └─────────────┘  └──────────────┘  └──────────────┘
        │                 │                    │
        └─────────────────┼────────────────────┘
                          ▼
            ┌─────────────────────────────┐
            │  Agent (Orquestador)        │
            │ - Recopila datos            │
            │ - Procesa información       │
            │ - Genera estructuras        │
            └─────────────────────────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │  Report Service             │
            │ - Genera PDF                │
            │ - Formatea datos            │
            │ - Guarda en disco           │
            └─────────────────────────────┘
                          │
                          ▼
            ┌─────────────────────────────┐
            │  ./reports/*.pdf            │
            │ Reportes generados diarios  │
            └─────────────────────────────┘
```

## 🔐 Seguridad

- **OAuth2**: Gmail usa Google OAuth2 (sin almacenar contraseñas)
- **Tokens**: Almacenados localmente en `gmail-token.json` (incluido en `.gitignore`)
- **Validación**: Zod para validación de variables de entorno
- **HTTPS**: Recomendado en producción

## 📈 Escalabilidad

El proyecto es fácilmente extensible para:
- ✅ Agregar más fuentes (Microsoft Teams, Slack, etc.)
- ✅ Envío automático de reportes (email, WhatsApp, Telegram)
- ✅ Dashboard web para ver reportes históricos
- ✅ Análisis y estadísticas
- ✅ Filtros personalizados por usuario

## 🧪 Testing

```bash
# Ejecutar tests
npm run test

# Tests específicos
npm run test:api

# Coverage
npm run test -- --coverage
```

## 📝 Logging

El proyecto incluye sistema de logging con colores:
- `ℹ` Info (azul)
- `⚠` Warning (amarillo)
- `✗` Error (rojo)
- `🐛` Debug (cyan)

## 🐳 Docker

### Construcción
```bash
docker build -t agente-notificaciones .
```

### Ejecución
```bash
docker run --env-file .env -v $(pwd)/reports:/app/reports agente-notificaciones
```

### Docker Compose
```bash
docker-compose up -d
```

## 📦 Variables de Entorno Requeridas

```env
# Gmail (obligatorio)
GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=
GMAIL_REDIRECT_URI=http://localhost:3000/oauth/callback
GMAIL_USER_EMAIL=

# LinkedIn (obligatorio)
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_ACCESS_TOKEN=

# Configuración (opcional)
SCHEDULE_TIME=08:00                    # Hora diaria
REPORT_OUTPUT_DIR=./reports           # Directorio de reportes
NODE_ENV=production                    # development/production
```

## 🔄 Ciclo de Vida

1. **08:00 AM** (hora programada): Se dispara la tarea diaria
2. **Gmail**: Obtiene correos de las últimas 24 horas
3. **LinkedIn**: Obtiene notificaciones de las últimas 24 horas
4. **Procesamiento**: Estructura los datos
5. **Generación**: Crea PDF con dos secciones
6. **Almacenamiento**: Guarda en `./reports/reporte-diario-YYYY-MM-DD.pdf`

## 📞 Soporte

Consulta:
- `README.md` - Documentación general
- `SETUP.md` - Guía de instalación paso a paso
- `EXTENSION.md` - Cómo extender el agente

## 🎓 Aprendizajes

Este proyecto demuestra:
- ✅ Integración con APIs OAuth2
- ✅ Manejo de TypeScript en backend
- ✅ Generación de documentos PDF
- ✅ Programación de tareas con node-schedule
- ✅ Validación con Zod
- ✅ Arquitectura modular y escalable
- ✅ Gestión de secretos

## 🚀 Próximas Mejoras

- [ ] Web scraping para LinkedIn (Puppeteer)
- [ ] Envío automático de reportes por email
- [ ] Dashboard web interactivo
- [ ] Estadísticas y análisis
- [ ] Notificaciones en Slack/Teams
- [ ] Base de datos para histórico
- [ ] Soporte multiidioma

## 📄 Licencia

MIT

---

**Creado**: Abril 2026
**Versión**: 1.0.0
**Mantenedor**: Tu nombre aquí

Para más información, consulta la documentación completa en los archivos .md del proyecto.
