# 🔌 Integración de API - Llamadas desde Otros Agentes

Este documento explica cómo otros agentes pueden llamar y ejecutar el Agente de Notificaciones desde una API REST.

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Iniciar el Servidor API](#iniciar-el-servidor-api)
3. [Endpoints REST](#endpoints-rest)
4. [Cliente SDK (TypeScript)](#cliente-sdk-typescript)
5. [Ejemplos de Uso](#ejemplos-de-uso)
6. [Webhooks y Callbacks](#webhooks-y-callbacks)
7. [Sistema de Eventos](#sistema-de-eventos)

## 🎯 Visión General

El agente ahora expone una **API REST** que permite:

✅ Generar reportes bajo demanda  
✅ Obtener correos y notificaciones de forma individual  
✅ Listar y descargar reportes generados  
✅ Recibir eventos de otros agentes  
✅ Notificar resultados vía webhooks  

### Arquitectura

```
┌─────────────────┐
│  Agente 1       │
│  (otro sistema) │
└────────┬────────┘
         │ HTTP POST
         ▼
┌──────────────────────────────────┐
│  API REST del Agente             │
│  (http://localhost:3000)         │
├──────────────────────────────────┤
│ • /api/v1/reports/generate       │
│ • /api/v1/emails                 │
│ • /api/v1/linkedin/notifications │
│ • /api/v1/events                 │
└──────────┬───────────────────────┘
           │
           ▼
    [Agent Core]
    [Services]
    [Reports]
```

## 🚀 Iniciar el Servidor API

El servidor API se inicia automáticamente al ejecutar el agente:

```bash
npm start
```

El servidor escuchará en `http://localhost:3000` por defecto.

Verificar que está activo:
```bash
curl http://localhost:3000/health
```

Respuesta esperada:
```json
{
  "status": "ok",
  "timestamp": "2026-04-17T10:30:00.000Z"
}
```

## 📡 Endpoints REST

### 1. Health Check

**GET** `/health`

Verificar que el servidor está activo.

```bash
curl http://localhost:3000/health
```

**Respuesta:**
```json
{
  "status": "ok",
  "timestamp": "2026-04-17T10:30:00.000Z"
}
```

---

### 2. Status del Agente

**GET** `/api/v1/status`

Obtener estado del agente y sus servicios.

```bash
curl http://localhost:3000/api/v1/status
```

**Respuesta:**
```json
{
  "status": "running",
  "version": "1.0.0",
  "services": {
    "gmail": "connected",
    "linkedin": "connected",
    "reports": "ready"
  },
  "timestamp": "2026-04-17T10:30:00.000Z"
}
```

---

### 3. Generar Reporte (Hoy)

**POST** `/api/v1/reports/generate`

Generar un reporte PDF con correos y notificaciones del día actual.

```bash
curl -X POST http://localhost:3000/api/v1/reports/generate
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Reporte generado exitosamente",
  "reportPath": "./reports/reporte-diario-2026-04-17.pdf",
  "timestamp": "2026-04-17T10:30:00.000Z"
}
```

---

### 4. Generar Reporte (Rango de Fechas)

**POST** `/api/v1/reports/generate-range`

Generar un reporte para un rango específico de fechas.

**Body:**
```json
{
  "startDate": "2026-04-01",
  "endDate": "2026-04-30"
}
```

```bash
curl -X POST http://localhost:3000/api/v1/reports/generate-range \
  -H "Content-Type: application/json" \
  -d '{
    "startDate": "2026-04-01",
    "endDate": "2026-04-30"
  }'
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Reporte generado exitosamente",
  "reportPath": "./reports/reporte-diario-2026-04-01_2026-04-30.pdf",
  "range": {
    "startDate": "2026-04-01",
    "endDate": "2026-04-30"
  },
  "timestamp": "2026-04-17T10:30:00.000Z"
}
```

---

### 5. Obtener Correos

**GET** `/api/v1/emails?days=1`

Obtener correos de los últimos N días (sin generar PDF).

**Parámetros:**
- `days` (opcional): número de días hacia atrás (default: 1)

```bash
curl "http://localhost:3000/api/v1/emails?days=7"
```

**Respuesta:**
```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "id": "msg123",
      "threadId": "th456",
      "sender": "cliente@example.com",
      "subject": "Nuevo proyecto",
      "snippet": "Te envío los detalles del proyecto...",
      "date": "2026-04-17T09:00:00.000Z",
      "isUnread": true
    }
  ],
  "timestamp": "2026-04-17T10:30:00.000Z"
}
```

---

### 6. Obtener Notificaciones LinkedIn

**GET** `/api/v1/linkedin/notifications?days=1`

Obtener notificaciones de LinkedIn de los últimos N días.

**Parámetros:**
- `days` (opcional): número de días hacia atrás (default: 1)

```bash
curl "http://localhost:3000/api/v1/linkedin/notifications?days=7"
```

**Respuesta:**
```json
{
  "success": true,
  "count": 3,
  "data": [
    {
      "id": "notif123",
      "type": "COMMENT",
      "actor": {
        "name": "Juan Pérez",
        "profileUrl": "https://linkedin.com/in/..."
      },
      "action": "comentó tu publicación",
      "description": "Excelente artículo, muy interesante",
      "timestamp": "2026-04-17T08:00:00.000Z",
      "url": "https://linkedin.com/feed/update/..."
    }
  ],
  "timestamp": "2026-04-17T10:30:00.000Z"
}
```

---

### 7. Listar Reportes Generados

**GET** `/api/v1/reports`

Listar todos los reportes PDF generados.

```bash
curl http://localhost:3000/api/v1/reports
```

**Respuesta:**
```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "filename": "reporte-diario-2026-04-17.pdf",
      "date": "2026-04-17T10:30:00.000Z",
      "path": "./reports/reporte-diario-2026-04-17.pdf"
    }
  ],
  "timestamp": "2026-04-17T10:30:00.000Z"
}
```

---

### 8. Descargar Reporte

**GET** `/api/v1/reports/:filename`

Descargar un archivo PDF específico.

```bash
curl -O http://localhost:3000/api/v1/reports/reporte-diario-2026-04-17.pdf
```

**Respuesta:** Archivo PDF binario

---

### 9. Generar con Callback (Webhook)

**POST** `/api/v1/reports/generate-with-callback`

Generar un reporte de forma asincrónica y notificar vía webhook cuando esté listo.

**Body:**
```json
{
  "webhookUrl": "https://tu-sistema.com/notifications/report",
  "agentId": "agent-1"
}
```

```bash
curl -X POST http://localhost:3000/api/v1/reports/generate-with-callback \
  -H "Content-Type: application/json" \
  -d '{
    "webhookUrl": "https://tu-sistema.com/notifications/report",
    "agentId": "agent-1"
  }'
```

**Respuesta inmediata:**
```json
{
  "success": true,
  "message": "Reporte se está generando. Se notificará al webhook cuando esté listo.",
  "taskId": "task_abc123",
  "timestamp": "2026-04-17T10:30:00.000Z"
}
```

**Callback (webhook) que recibirá:**
```json
{
  "status": "completed",
  "reportPath": "./reports/reporte-diario-2026-04-17.pdf",
  "agentId": "agent-1",
  "timestamp": "2026-04-17T10:31:00.000Z"
}
```

---

### 10. Recibir Eventos

**POST** `/api/v1/events`

Sistema de eventos para que otros agentes envíen instrucciones.

**Body:**
```json
{
  "type": "GENERATE_REPORT",
  "payload": {},
  "sourceAgent": "agent-2"
}
```

**Tipos de eventos:**
- `GENERATE_REPORT` - Generar reporte
- `GET_EMAILS` - Obtener correos
- `GET_LINKEDIN` - Obtener notificaciones LinkedIn

```bash
curl -X POST http://localhost:3000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "type": "GENERATE_REPORT",
    "payload": {},
    "sourceAgent": "agent-2"
  }'
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Reporte generado por evento",
  "reportPath": "./reports/reporte-diario-2026-04-17.pdf",
  "sourceAgent": "agent-2",
  "timestamp": "2026-04-17T10:30:00.000Z"
}
```

---

### 11. Documentación de API

**GET** `/api/docs`

Obtener documentación completa de la API en JSON.

```bash
curl http://localhost:3000/api/docs
```

---

## 💻 Cliente SDK (TypeScript)

Para facilitar el uso desde otros agentes TypeScript, se proporciona un cliente SDK:

```typescript
import { NotificationsAgentClient } from './sdk/client.js';

// Crear instancia del cliente
const client = new NotificationsAgentClient(
  'http://localhost:3000',
  'mi-agente'
);

// Verificar conexión
const isAlive = await client.health();
console.log('¿Agente disponible?', isAlive);

// Generar reporte
const result = await client.generateReport();
if (result.success) {
  console.log('Reporte en:', result.reportPath);
} else {
  console.error('Error:', result.error);
}

// Obtener correos
const emails = await client.getEmails(7); // últimos 7 días
console.log(`${emails.length} correos encontrados`);

// Obtener notificaciones LinkedIn
const notifications = await client.getLinkedInNotifications(7);
console.log(`${notifications.length} notificaciones LinkedIn`);
```

---

## 📚 Ejemplos de Uso

### Ejemplo 1: Agente que Genera Reportes Bajo Demanda

```typescript
import { NotificationsAgentClient } from './sdk/client.js';

const client = new NotificationsAgentClient('http://localhost:3000', 'reportes-agent');

async function requestDailyReport() {
  console.log('📊 Solicitando reporte diario...');
  const result = await client.generateReport();
  
  if (result.success) {
    console.log(`✅ Reporte listo: ${result.reportPath}`);
    return result.reportPath;
  } else {
    console.error(`❌ Error: ${result.error}`);
  }
}

requestDailyReport();
```

### Ejemplo 2: Agente que Obtiene Correos para Procesamiento

```typescript
import { NotificationsAgentClient } from './sdk/client.js';

const client = new NotificationsAgentClient('http://localhost:3000', 'email-processor');

async function processRecentEmails() {
  console.log('📧 Obteniendo correos recientes...');
  const emails = await client.getEmails(1); // últimas 24 horas
  
  for (const email of emails) {
    console.log(`De: ${email.sender}`);
    console.log(`Asunto: ${email.subject}`);
    console.log(`---`);
    
    // Tu lógica de procesamiento aquí
  }
}

processRecentEmails();
```

### Ejemplo 3: Agente que Envía Eventos

```typescript
import { NotificationsAgentClient } from './sdk/client.js';

const client = new NotificationsAgentClient('http://localhost:3000', 'orchestrator');

async function orchestrateNotifications() {
  // Evento 1: Generar reporte
  const reportResult = await client.requestGenerateReport();
  console.log('Reporte generado:', reportResult.reportPath);
  
  // Evento 2: Obtener correos
  const emailsResult = await client.requestGetEmails(7);
  console.log(`${emailsResult.count} correos en últimos 7 días`);
  
  // Evento 3: Obtener LinkedIn
  const linkedinResult = await client.requestGetLinkedIn(7);
  console.log(`${linkedinResult.count} notificaciones LinkedIn`);
}

orchestrateNotifications();
```

### Ejemplo 4: Agente que Monitorea el Estado

```typescript
import { NotificationsAgentClient } from './sdk/client.js';

const client = new NotificationsAgentClient('http://localhost:3000', 'monitor');

async function monitorAgent() {
  const status = await client.getStatus();
  
  console.log(`Estado: ${status.status}`);
  console.log(`Versión: ${status.version}`);
  console.log(`Servicios:`);
  console.log(`  - Gmail: ${status.services.gmail}`);
  console.log(`  - LinkedIn: ${status.services.linkedin}`);
  console.log(`  - Reportes: ${status.services.reports}`);
}

monitorAgent();
```

---

## 🔔 Webhooks y Callbacks

### Usar Webhooks para Notificaciones

El agente puede notificar a otros sistemas cuando se completa una tarea:

```typescript
// Desde otro agente
const client = new NotificationsAgentClient('http://localhost:3000', 'mi-agente');

await client.generateReportWithCallback(
  'https://mi-sistema.com/api/notifications/report-ready'
);

// Tu sistema recibirá un POST en ese webhook:
// {
//   "status": "completed",
//   "reportPath": "./reports/reporte-diario-2026-04-17.pdf",
//   "agentId": "mi-agente",
//   "timestamp": "2026-04-17T10:31:00.000Z"
// }
```

### Implementar un Webhook Receptor

```typescript
import express from 'express';

const app = express();
app.use(express.json());

app.post('/api/notifications/report-ready', (req, res) => {
  const { status, reportPath, agentId } = req.body;
  
  if (status === 'completed') {
    console.log(`✅ Reporte listo: ${reportPath}`);
    console.log(`Solicitado por: ${agentId}`);
    
    // Tu lógica aquí: procesar el reporte, enviarlo, etc.
  }
  
  res.json({ received: true });
});

app.listen(3001, () => {
  console.log('Webhook receptor en puerto 3001');
});
```

---

## 🎯 Sistema de Eventos

Otros agentes pueden enviar eventos específicos:

### GENERATE_REPORT

```typescript
await client.sendEvent({
  type: 'GENERATE_REPORT',
  payload: {},
  sourceAgent: 'agente-x'
});
```

### GET_EMAILS

```typescript
await client.sendEvent({
  type: 'GET_EMAILS',
  payload: { days: 7 },
  sourceAgent: 'agente-x'
});
```

### GET_LINKEDIN

```typescript
await client.sendEvent({
  type: 'GET_LINKEDIN',
  payload: { days: 7 },
  sourceAgent: 'agente-x'
});
```

---

## 🔒 Seguridad

### Recomendaciones

1. **Autenticación**: Considera agregar Bearer tokens
2. **Rate Limiting**: Protege endpoints públicos
3. **CORS**: Configura según sea necesario
4. **HTTPS**: Usa en producción
5. **Validación**: Todos los inputs se validan

### Agregar Autenticación (Extensión Futura)

```typescript
// Middleware de autenticación
app.use((req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No autorizado' });
  // Verificar token...
  next();
});
```

---

## 📊 Casos de Uso

### 1. Dashboard que Obtiene Datos en Vivo

```typescript
const emails = await client.getEmails(1);
const linkedin = await client.getLinkedInNotifications(1);

dashboardUI.render({
  emails: emails.length,
  linkedinNotifications: linkedin.length
});
```

### 2. Sistema de Alertas que Genera Reportes

```typescript
if (alertsTriggered) {
  const report = await client.generateReport();
  sendEmailWithAttachment(report.reportPath);
}
```

### 3. Orquestador que Coordina Múltiples Agentes

```typescript
// Este agente coordina otros
const notificationsData = await client.getEmails(7);
const processedData = await otherAgent.processData(notificationsData);
await thirdAgent.sendReport(processedData);
```

---

## 🚨 Manejo de Errores

```typescript
try {
  const result = await client.generateReport();
  
  if (!result.success) {
    console.error('Error del agente:', result.error);
  }
} catch (error) {
  console.error('Error de conexión:', error.message);
}
```

---

## 📝 Variables de Entorno

```env
# Para usar el cliente SDK
NOTIFICATIONS_AGENT_URL=http://localhost:3000
NOTIFICATIONS_AGENT_ID=mi-agente

# Para webhooks
WEBHOOK_SECRET=tu-secreto-opcional
```

---

## 🔗 Próximas Mejoras

- [ ] Autenticación con JWT
- [ ] Rate limiting por agente
- [ ] Webhooks con retry automático
- [ ] Soporte para GraphQL
- [ ] WebSocket para updates en tiempo real
- [ ] Sistema de colas para tareas pesadas

---

**¡Listo!** Otros agentes ya pueden llamar e interactuar con este agente. 🚀
