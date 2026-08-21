# 📁 Estructura Completa del Proyecto

```
agente-notificaciones-diarias/
│
├── 📄 Archivos de Configuración
│   ├── package.json                 # Dependencias del proyecto
│   ├── tsconfig.json                # Configuración TypeScript
│   ├── .env.example                 # Plantilla de variables de entorno
│   ├── .gitignore                   # Archivos a ignorar en Git
│   ├── Dockerfile                   # Imagen Docker
│   └── docker-compose.yml           # Orquestación Docker
│
├── 📚 Documentación
│   ├── README.md                    # Documentación principal
│   ├── SETUP.md                     # Guía de instalación paso a paso
│   ├── QUICKSTART.md                # Inicio rápido (5 minutos)
│   ├── EXTENSION.md                 # Cómo extender el proyecto
│   ├── PROJECT_SUMMARY.md           # Resumen técnico del proyecto
│   └── PROJECT_STRUCTURE.md         # Este archivo
│
├── 📂 src/ (Código Fuente)
│   │
│   ├── 🤖 agent/
│   │   └── index.ts                 # Orquestador principal del agente
│   │                                 # - Coordina Gmail, LinkedIn, Reportes
│   │                                 # - Genera reportes diarios
│   │                                 # - Maneja autenticación
│   │
│   ├── ⚙️ config/
│   │   └── env.ts                   # Validación de variables de entorno
│   │                                 # - Usa Zod para validar
│   │                                 # - Exporta config tipado
│   │
│   ├── 🔌 services/
│   │   ├── gmail.service.ts         # Integración con Gmail API
│   │   │                             # - Autenticación OAuth2
│   │   │                             # - Lectura de correos
│   │   │                             # - Filtrado por fecha
│   │   │
│   │   ├── linkedin.service.ts      # Integración con LinkedIn API
│   │   │                             # - Obtención de notificaciones
│   │   │                             # - Actividad reciente
│   │   │
│   │   └── report.service.ts        # Generación de reportes PDF
│   │                                 # - Crea documentos PDF
│   │                                 # - Formatea datos
│   │                                 # - Estructura con secciones
│   │
│   ├── 📅 scheduler/
│   │   └── daily-task.ts            # Programación de tareas diarias
│   │                                 # - Usa node-schedule
│   │                                 # - Ejecuta a hora especificada
│   │
│   ├── 📝 types/
│   │   └── index.ts                 # Interfaces TypeScript
│   │                                 # - EmailMessage
│   │                                 # - LinkedInNotification
│   │                                 # - DailyReport
│   │                                 # - ReportSection
│   │
│   ├── 🔧 utils/
│   │   └── logger.ts                # Sistema de logging
│   │                                 # - Logger con colores
│   │                                 # - Información, advertencias, errores
│   │                                 # - Debug condicional
│   │
│   └── 🚀 index.ts                  # Punto de entrada
│                                     # - Inicializa agente
│                                     # - Inicia planificador
│                                     # - Maneja señales de cierre
│
├── 📂 reports/                      # Carpeta de reportes (generada)
│   └── reporte-diario-2026-04-17.pdf  # PDFs generados diariamente
│
└── 📂 dist/ (generada después de build)
    └── [Código JavaScript compilado]
```

## 📊 Relación entre Módulos

```
┌─────────────────────────────────────────────────────────────┐
│                      src/index.ts                           │
│                    (Punto de entrada)                       │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
    ┌────────────┐   ┌─────────────┐   ┌──────────────┐
    │  Agent     │   │  Scheduler  │   │  Logger      │
    │ (index.ts)│   │ (daily-task)│   │  (utils)     │
    └────────────┘   └─────────────┘   └──────────────┘
        │                   │
        │                   └──────────┐
        │                              │
        ▼                              ▼
    ┌────────────────────────────────────────┐
    │      Agent (agent/index.ts)            │
    │  - Coordina servicios                  │
    │  - Orquesta flujo diario               │
    └────────────────────────────────────────┘
        │
        ├──────────────┬──────────────┬──────────────┐
        │              │              │              │
        ▼              ▼              ▼              ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
    │  Gmail   │ │LinkedIN  │ │  Report  │ │  Types   │
    │ Service  │ │ Service  │ │ Service  │ │          │
    └──────────┘ └──────────┘ └──────────┘ └──────────┘
        │              │              │
        ▼              ▼              ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ Gmail    │ │ LinkedIn │ │   PDF    │
    │   API    │ │   API    │ │ (pdfkit) │
    └──────────┘ └──────────┘ └──────────┘
```

## 🔄 Flujo de Ejecución

```
1. npm start
   └─> src/index.ts (punto de entrada)
       ├─> Crea instancia de Agent
       ├─> Crea instancia de DailyTaskScheduler
       ├─> scheduler.start()
       │   └─> Programa task para 08:00 AM (SCHEDULE_TIME)
       └─> Mantiene proceso activo (proceso.on('SIGINT'))

2. A las 08:00 AM (o según SCHEDULE_TIME)
   └─> DailyTaskScheduler.runDailyTask()
       └─> Agent.generateDailyReport()
           ├─> gmailService.getEmailsByDateRange(startDate, endDate)
           │   ├─> Autentica con OAuth2
           │   ├─> Consulta Gmail API
           │   └─> Retorna array de EmailMessage[]
           │
           ├─> linkedinService.getRecentActivity(startDate, endDate)
           │   ├─> Autentica con token de acceso
           │   ├─> Consulta LinkedIn API
           │   └─> Retorna array de LinkedInNotification[]
           │
           ├─> Estructura datos en DailyReport
           │   ├─> Crea ReportSection para emails
           │   ├─> Crea ReportSection para linkedin
           │   └─> Combina en un solo objeto
           │
           ├─> reportService.generatePDF(report)
           │   ├─> Crea documento PDF
           │   ├─> Agrega encabezado y fecha
           │   ├─> Agrega sección de correos
           │   ├─> Agrega sección de LinkedIn
           │   ├─> Guarda en ./reports/reporte-diario-YYYY-MM-DD.pdf
           │   └─> Retorna ruta del archivo
           │
           └─> Retorna ruta del PDF generado

3. El PDF se guarda en ./reports/
   └─> Disponible para:
       ├─> Descargar manualmente
       ├─> Enviar por email (extensión)
       ├─> Subir a cloud (extensión)
       └─> Integrar con dashboard (extensión)
```

## 📦 Dependencias Principales

```json
{
  "runtime": {
    "node": "18+",
    "npm": "9+"
  },
  "dependencies": {
    "axios": "API HTTP client",
    "dotenv": "Cargar variables de entorno",
    "googleapis": "Cliente de Google APIs",
    "node-schedule": "Programación de tareas",
    "pdfkit": "Generación de PDFs",
    "puppeteer": "Web scraping (opcional)",
    "zod": "Validación de esquemas"
  },
  "devDependencies": {
    "@types/node": "Tipos TypeScript para Node",
    "@typescript-eslint/*": "Linting TypeScript",
    "jest": "Testing",
    "ts-jest": "Jest con TypeScript",
    "tsx": "Ejecutar TypeScript directamente",
    "typescript": "Compilador TypeScript"
  }
}
```

## 🔑 Variables de Entorno

| Variable | Archivo | Descripción |
|----------|---------|-------------|
| `GMAIL_CLIENT_ID` | .env | ID del cliente OAuth de Google |
| `GMAIL_CLIENT_SECRET` | .env | Secreto del cliente OAuth de Google |
| `GMAIL_REDIRECT_URI` | .env | URI de redirección OAuth |
| `GMAIL_USER_EMAIL` | .env | Email de Gmail del usuario |
| `LINKEDIN_CLIENT_ID` | .env | ID del cliente LinkedIn |
| `LINKEDIN_CLIENT_SECRET` | .env | Secreto del cliente LinkedIn |
| `LINKEDIN_ACCESS_TOKEN` | .env | Token de acceso LinkedIn |
| `SCHEDULE_TIME` | .env | Hora de ejecución (HH:MM) |
| `REPORT_OUTPUT_DIR` | .env | Directorio de reportes |
| `NODE_ENV` | .env | development o production |
| `DEBUG` | .env | true para logs debug |

## 📋 Tipos de Datos Principales

```typescript
// Correo de Gmail
interface EmailMessage {
  id: string
  threadId: string
  sender: string
  subject: string
  snippet: string
  body: string
  date: Date
  labels: string[]
  isUnread: boolean
}

// Notificación de LinkedIn
interface LinkedInNotification {
  id: string
  type: string
  actor: { name: string; profileUrl?: string }
  action: string
  timestamp: Date
  description: string
  url?: string
}

// Reporte diario completo
interface DailyReport {
  generatedAt: Date
  period: { startDate: Date; endDate: Date }
  sections: {
    emails: ReportSection
    linkedin: ReportSection
  }
}

// Sección del reporte
interface ReportSection {
  title: string
  count: number
  items: ReportItem[]
}

// Item individual en el reporte
interface ReportItem {
  title: string
  summary: string
  source: string
  timestamp: Date
  url?: string
}
```

## 🎯 Próximos Pasos

1. **Instalación**: Seguir [SETUP.md](SETUP.md)
2. **Configuración**: Completar `.env` con credenciales
3. **Prueba**: Ejecutar con `npm run dev`
4. **Extensiones**: Ver [EXTENSION.md](EXTENSION.md)

---

**Versión**: 1.0.0  
**Última actualización**: Abril 2026
