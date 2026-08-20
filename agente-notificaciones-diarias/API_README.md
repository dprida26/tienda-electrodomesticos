# 🔌 API REST - Integración Entre Agentes

## ¿Qué es Nuevo?

Se ha agregado una **API REST completa** que permite que otros agentes llamen y ejecuten funcionalidades del Agente de Notificaciones Diarias.

### Antes (Solo ejecución local)
```
Tu Agente → Genera reportes → Guarda PDFs
```

### Ahora (Con API)
```
Tu Agente
    ↑
    │ HTTP REST
    │
Otros Agentes ←→ API REST ←→ [Servicios: Gmail, LinkedIn, Reports]
    │
    ├─ Agente de Reportes
    ├─ Agente de Alertas
    ├─ Dashboard Web
    ├─ Worker/Cron Jobs
    └─ Sistemas Externos
```

## 🎯 Características Nuevas

✅ **API REST con 11 endpoints**
✅ **Cliente SDK TypeScript**
✅ **Sistema de eventos entre agentes**
✅ **Webhooks y callbacks asincronos**
✅ **Documentación automática en `/api/docs`**

## 🚀 Cómo Funciona

### 1. El Servidor API Se Inicia Automáticamente

```bash
npm start
```

Se ejecuta en `http://localhost:3000`

### 2. Otros Agentes Pueden Llamarlo

```typescript
import { NotificationsAgentClient } from './sdk/client.js';

const client = new NotificationsAgentClient('http://localhost:3000', 'mi-agente');

// Generar reporte
const result = await client.generateReport();

// Obtener correos
const emails = await client.getEmails(7);

// Obtener LinkedIn
const notifications = await client.getLinkedInNotifications(7);
```

### 3. O Usar REST Directo

```bash
# Generar reporte
curl -X POST http://localhost:3000/api/v1/reports/generate

# Obtener correos
curl http://localhost:3000/api/v1/emails?days=7

# Obtener LinkedIn
curl http://localhost:3000/api/v1/linkedin/notifications?days=7
```

## 📡 11 Endpoints Disponibles

| # | Endpoint | Método | Descripción |
|---|----------|--------|-------------|
| 1 | `/health` | GET | Verificar que está activo |
| 2 | `/api/v1/status` | GET | Estado del agente |
| 3 | `/api/v1/reports/generate` | POST | Generar reporte de hoy |
| 4 | `/api/v1/reports/generate-range` | POST | Generar reporte (rango de fechas) |
| 5 | `/api/v1/emails` | GET | Obtener correos |
| 6 | `/api/v1/linkedin/notifications` | GET | Obtener LinkedIn |
| 7 | `/api/v1/reports` | GET | Listar reportes |
| 8 | `/api/v1/reports/:filename` | GET | Descargar reporte |
| 9 | `/api/v1/reports/generate-with-callback` | POST | Generar con webhook |
| 10 | `/api/v1/events` | POST | Recibir eventos |
| 11 | `/api/docs` | GET | Documentación API |

## 📚 Documentación Completa

Hay **3 archivos de documentación**:

1. **[API_INTEGRATION.md](API_INTEGRATION.md)** — Guía técnica completa
   - Todos los endpoints detallados
   - Ejemplos de request/response
   - Sistema de webhooks
   - Sistema de eventos

2. **[EXAMPLES.md](EXAMPLES.md)** — 10 ejemplos prácticos
   - Cliente REST con cURL
   - Cliente JavaScript/Node.js
   - Cliente Python
   - Orquestador de agentes
   - Webhook receptor
   - Worker/Cron jobs
   - Sistema de alertas
   - Dashboard React
   - Pipeline de procesamiento
   - Monitor de salud

3. **[src/sdk/client.ts](src/sdk/client.ts)** — SDK TypeScript
   - Cliente lista para usar
   - TypeScript con tipos completos
   - Manejo de errores

## 💡 Casos de Uso

### 1. Agente Orquestador
Un agente central que coordina llamadas a múltiples servicios:

```typescript
const client = new NotificationsAgentClient(...);

// Obtener datos de múltiples fuentes
const emails = await client.getEmails(7);
const linkedin = await client.getLinkedInNotifications(7);

// Procesar y combinar
const report = combineData(emails, linkedin);
```

### 2. Webhook para Notificaciones
Ejecutar algo cuando se complete un reporte:

```typescript
await client.generateReportWithCallback('https://mi-sistema.com/webhook');

// Tu sistema recibe POST cuando está listo
```

### 3. Worker/Cron Job
Generar reportes periódicamente:

```typescript
// Cada día a las 9 AM
schedule.scheduleJob('0 9 * * *', async () => {
  const result = await client.generateReport();
});
```

### 4. Dashboard Web
Mostrar datos en tiempo real:

```typescript
// React component que obtiene datos
const emails = await client.getEmails(1);
const linkedin = await client.getLinkedInNotifications(1);
// Renderizar en UI
```

### 5. Sistema de Alertas
Alertar sobre correos importantes:

```typescript
const emails = await client.getEmails(1);
const important = emails.filter(e => e.subject.includes('URGENT'));
if (important.length > 0) {
  sendAlert(important);
}
```

## 🔄 Flujos de Integración

### Flujo 1: Llamada Directa (Síncrona)

```
Agente A
    │
    ├─→ HTTP POST /reports/generate
    │
    └─← JSON response con reportPath
```

### Flujo 2: Callback (Asíncrona)

```
Agente A
    │
    ├─→ HTTP POST /reports/generate-with-callback
    │   (con webhookUrl)
    │
    └─← taskId inmediatamente
         │
         └─→ Agente A espera webhook
             │
             ← POST a tu webhook cuando esté listo
```

### Flujo 3: Eventos (Pubsub)

```
Agente A          Agente B          Agente C
    │                 │                 │
    └────→ /events ←──┴─────→ /events ←─┘
           (GENERATE_REPORT)
```

## 🛠️ Archivos Nuevos/Modificados

### Nuevos Archivos
- ✅ `src/api/server.ts` — Servidor Express con todos los endpoints
- ✅ `src/sdk/client.ts` — Cliente TypeScript para otros agentes
- ✅ `API_INTEGRATION.md` — Documentación técnica
- ✅ `EXAMPLES.md` — 10 ejemplos prácticos
- ✅ `API_README.md` — Este archivo

### Archivos Modificados
- ✏️ `src/index.ts` — Ahora inicia el servidor API
- ✏️ `src/agent/index.ts` — Nuevos métodos para la API
- ✏️ `package.json` — Agregadas dependencias de Express

## 📋 Flujo de Inicialización

```
npm start
    ↓
1. Inicializar Agent (autenticación)
    ↓
2. Iniciar Servidor API en puerto 3000
    ↓
3. Iniciar Scheduler (reportes diarios)
    ↓
✅ Agente listo para recibir llamadas
```

## 🔐 Seguridad

- ✅ Validación de entrada (Zod)
- ✅ Manejo de errores robusto
- ✅ Validación de rutas (path traversal)
- ✅ Timeouts en requests
- ⏳ TODO: Agregar autenticación JWT
- ⏳ TODO: Rate limiting

## 📊 Variables de Entorno

Nuevas variables opcionales:

```env
# API
API_PORT=3000                  # Puerto del servidor (default: 3000)

# Existentes
SCHEDULE_TIME=08:00
REPORT_OUTPUT_DIR=./reports
NODE_ENV=production
```

## 🧪 Probar la API

### 1. Verificar que está activo

```bash
curl http://localhost:3000/health
# {"status":"ok","timestamp":"2026-04-17T..."}
```

### 2. Ver documentación

```bash
curl http://localhost:3000/api/docs | jq
```

### 3. Generar reporte

```bash
curl -X POST http://localhost:3000/api/v1/reports/generate
```

### 4. Obtener datos

```bash
curl "http://localhost:3000/api/v1/emails?days=7" | jq
```

## 📚 Próximos Pasos

1. **Lee [API_INTEGRATION.md](API_INTEGRATION.md)**
   - Guía técnica completa de cada endpoint

2. **Revisa [EXAMPLES.md](EXAMPLES.md)**
   - Ejemplos listos para copiar/pegar

3. **Usa el SDK**
   ```typescript
   import { NotificationsAgentClient } from './src/sdk/client.js';
   const client = new NotificationsAgentClient(...);
   ```

4. **Integra con tus agentes**
   - Orquestadores
   - Dashboards
   - Alertas
   - Workers
   - Etc.

## 🤝 Colaboración Entre Agentes

Ahora el ecosistema de agentes puede:

```
┌─────────────────────────────────────────────┐
│        Agente de Orquestación               │
│  (coordina todo el flujo)                   │
└──────────┬──────────────────────────────────┘
           │
    ┌──────┼──────┬──────────┐
    │      │      │          │
    ▼      ▼      ▼          ▼
 Gmail  LinkedIn Reports   Webhooks
 Agent   Agent    Agent     Agent
```

Cada agente puede:
- ✅ Llamar a otros agentes
- ✅ Enviar eventos
- ✅ Esperar webhooks
- ✅ Coordinar tareas

## 🎯 Resumen

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| Ejecución | Local solamente | Local + API REST |
| Llamadas desde otros | ❌ No posible | ✅ Posible |
| Eventos | ❌ No | ✅ Sí (10 tipos) |
| Webhooks | ❌ No | ✅ Sí (asincronía) |
| Integración | Manual | Automática |
| Documentación | Básica | Completa (3 docs) |
| Ejemplos | Ninguno | 10 ejemplos |

---

**¡Tu agente ahora es parte de un ecosistema de agentes colaborativos!** 🚀

Para más información:
- Documentación: [API_INTEGRATION.md](API_INTEGRATION.md)
- Ejemplos: [EXAMPLES.md](EXAMPLES.md)
- Cliente SDK: [src/sdk/client.ts](src/sdk/client.ts)
