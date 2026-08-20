# 📚 Ejemplos de Integración

Ejemplos prácticos de cómo otros agentes pueden usar este agente.

## 1. Cliente REST Simple (cURL)

### Generar Reporte

```bash
curl -X POST http://localhost:3000/api/v1/reports/generate
```

### Obtener Correos

```bash
curl "http://localhost:3000/api/v1/emails?days=7"
```

### Obtener Notificaciones LinkedIn

```bash
curl "http://localhost:3000/api/v1/linkedin/notifications?days=7"
```

---

## 2. Cliente Node.js/JavaScript

### Usando Fetch API

```javascript
// file: client.js
const BASE_URL = 'http://localhost:3000/api/v1';

async function generateReport() {
  const response = await fetch(`${BASE_URL}/reports/generate`, {
    method: 'POST'
  });
  
  const data = await response.json();
  console.log('✅ Reporte generado:', data.reportPath);
}

async function getEmails(days = 7) {
  const response = await fetch(`${BASE_URL}/emails?days=${days}`);
  const data = await response.json();
  
  console.log(`📧 ${data.count} correos encontrados`);
  data.data.forEach(email => {
    console.log(`  - ${email.sender}: ${email.subject}`);
  });
}

async function getLinkedIn(days = 7) {
  const response = await fetch(`${BASE_URL}/linkedin/notifications?days=${days}`);
  const data = await response.json();
  
  console.log(`💼 ${data.count} notificaciones de LinkedIn`);
  data.data.forEach(notif => {
    console.log(`  - ${notif.actor.name}: ${notif.action}`);
  });
}

// Ejecutar
generateReport();
getEmails(7);
getLinkedIn(7);
```

### Usando el SDK Incluido

```typescript
// file: client.ts
import { NotificationsAgentClient } from './agente-notificaciones-diarias/src/sdk/client.js';

const client = new NotificationsAgentClient('http://localhost:3000', 'mi-agente');

async function main() {
  // Verificar conexión
  const isAlive = await client.health();
  if (!isAlive) {
    console.error('❌ El agente no está disponible');
    return;
  }

  // Generar reporte
  console.log('📊 Generando reporte...');
  const reportResult = await client.generateReport();
  if (reportResult.success) {
    console.log(`✅ Reporte: ${reportResult.reportPath}`);
  }

  // Obtener correos
  console.log('📧 Obteniendo correos...');
  const emails = await client.getEmails(7);
  console.log(`${emails.length} correos encontrados`);

  // Obtener LinkedIn
  console.log('💼 Obteniendo LinkedIn...');
  const notifications = await client.getLinkedInNotifications(7);
  console.log(`${notifications.length} notificaciones LinkedIn`);
}

main();
```

---

## 3. Python

### Cliente Python

```python
# file: client.py
import requests
import json
from datetime import datetime

class NotificationsAgentClient:
    def __init__(self, base_url='http://localhost:3000', agent_id='python-agent'):
        self.base_url = f'{base_url}/api/v1'
        self.agent_id = agent_id
        self.session = requests.Session()
    
    def generate_report(self):
        """Generar reporte PDF"""
        response = self.session.post(f'{self.base_url}/reports/generate')
        return response.json()
    
    def get_emails(self, days=1):
        """Obtener correos"""
        response = self.session.get(
            f'{self.base_url}/emails',
            params={'days': days}
        )
        return response.json()
    
    def get_linkedin(self, days=1):
        """Obtener notificaciones LinkedIn"""
        response = self.session.get(
            f'{self.base_url}/linkedin/notifications',
            params={'days': days}
        )
        return response.json()
    
    def send_event(self, event_type, payload=None):
        """Enviar evento"""
        response = self.session.post(
            f'{self.base_url}/events',
            json={
                'type': event_type,
                'payload': payload or {},
                'sourceAgent': self.agent_id
            }
        )
        return response.json()

# Uso
if __name__ == '__main__':
    client = NotificationsAgentClient(agent_id='python-processor')
    
    # Generar reporte
    print('📊 Generando reporte...')
    report = client.generate_report()
    if report['success']:
        print(f"✅ {report['reportPath']}")
    
    # Obtener correos
    print('📧 Obteniendo correos...')
    emails = client.get_emails(days=7)
    print(f"Encontrados: {emails['count']} correos")
    
    # Obtener LinkedIn
    print('💼 Obteniendo LinkedIn...')
    linkedin = client.get_linkedin(days=7)
    print(f"Encontradas: {linkedin['count']} notificaciones")
```

---

## 4. Sistema Completo: Agente Orquestador

### Caso: Dashboard que Recopila Datos de Múltiples Fuentes

```typescript
// file: orchestrator-agent.ts
import { NotificationsAgentClient } from './agente-notificaciones-diarias/src/sdk/client.js';
import express from 'express';

const app = express();
const notificationsClient = new NotificationsAgentClient('http://localhost:3000', 'orchestrator');

// Endpoint que recopila todo
app.get('/api/dashboard', async (req, res) => {
  try {
    // Obtener datos en paralelo
    const [emails, linkedin, status] = await Promise.all([
      notificationsClient.getEmails(1),
      notificationsClient.getLinkedInNotifications(1),
      notificationsClient.getStatus()
    ]);

    res.json({
      timestamp: new Date(),
      agentStatus: status,
      notifications: {
        emails: {
          count: emails.length,
          recent: emails.slice(0, 5)
        },
        linkedin: {
          count: linkedin.length,
          recent: linkedin.slice(0, 5)
        }
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3001, () => {
  console.log('Dashboard en http://localhost:3001/api/dashboard');
});
```

---

## 5. Webhook Receptor

### Agente que Recibe Callbacks

```typescript
// file: webhook-receiver.ts
import express from 'express';
import fs from 'fs';

const app = express();
app.use(express.json());

// Endpoint que recibe reportes generados
app.post('/api/notifications/report-ready', async (req, res) => {
  const { status, reportPath, agentId, timestamp } = req.body;

  console.log(`\n📬 Webhook recibido:`);
  console.log(`   Estado: ${status}`);
  console.log(`   Reporte: ${reportPath}`);
  console.log(`   Agente: ${agentId}`);
  console.log(`   Hora: ${timestamp}`);

  if (status === 'completed') {
    // Procesar el reporte
    console.log('✅ Reporte completado, procesando...');
    
    // Aquí puedes:
    // - Descargarlo
    // - Procesarlo
    // - Enviarlo por email
    // - Guardarlo en base de datos
    // etc.
  }

  res.json({ received: true, processed: true });
});

// Endpoint que recibe errores
app.post('/api/notifications/report-error', (req, res) => {
  const { status, error, agentId, timestamp } = req.body;

  console.error(`\n❌ Error en reporte:`);
  console.error(`   Error: ${error}`);
  console.error(`   Agente: ${agentId}`);
  console.error(`   Hora: ${timestamp}`);

  res.json({ received: true });
});

app.listen(3002, () => {
  console.log('🔔 Webhook receiver en puerto 3002');
});
```

### Usar con Callback

```typescript
// Desde otro lado, solicitar reporte con callback
const client = new NotificationsAgentClient('http://localhost:3000', 'task-runner');

await client.generateReportWithCallback(
  'http://localhost:3002/api/notifications/report-ready'
);

console.log('📤 Reporte solicitado. Se notificará cuando esté listo.');
```

---

## 6. Worker/Cron Job

### Agente que Genera Reportes Periódicamente

```typescript
// file: worker.ts
import { NotificationsAgentClient } from './agente-notificaciones-diarias/src/sdk/client.js';
import schedule from 'node-schedule';

const client = new NotificationsAgentClient('http://localhost:3000', 'worker-agent');

// Generar reporte cada día a las 9:00 AM
schedule.scheduleJob('0 9 * * *', async () => {
  console.log('⏰ Ejecutando generación de reportes...');
  
  try {
    const result = await client.generateReport();
    if (result.success) {
      console.log(`✅ Reporte generado: ${result.reportPath}`);
      
      // Enviar email, guardar en DB, etc.
    }
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
});

console.log('🔄 Worker iniciado. Reportes diarios a las 9:00 AM');
```

---

## 7. Sistema de Alertas

### Agente que Alerta sobre Correos Importantes

```typescript
// file: alert-agent.ts
import { NotificationsAgentClient } from './agente-notificaciones-diarias/src/sdk/client.js';
import nodemailer from 'nodemailer';

const client = new NotificationsAgentClient('http://localhost:3000', 'alert-agent');

// Configurar transporte de email
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.ALERT_EMAIL,
    pass: process.env.ALERT_PASSWORD
  }
});

async function checkForImportantEmails() {
  try {
    // Obtener correos de hoy
    const emails = await client.getEmails(1);

    // Filtrar por remitentes importantes
    const importantEmails = emails.filter(email =>
      email.sender.includes('boss@') ||
      email.sender.includes('ceo@') ||
      email.subject.includes('URGENTE')
    );

    if (importantEmails.length > 0) {
      // Enviar alerta
      await transporter.sendMail({
        from: process.env.ALERT_EMAIL,
        to: process.env.ALERT_TO,
        subject: `🚨 ${importantEmails.length} correo(s) importante(s)`,
        html: `
          <h2>Correos importantes recibidos:</h2>
          <ul>
            ${importantEmails.map(e => 
              `<li><strong>${e.sender}</strong>: ${e.subject}</li>`
            ).join('')}
          </ul>
        `
      });

      console.log(`✅ Alertas enviadas para ${importantEmails.length} correos`);
    }
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

// Ejecutar cada 30 minutos
setInterval(checkForImportantEmails, 30 * 60 * 1000);
console.log('🚨 Sistema de alertas activo');
```

---

## 8. Dashboard Web con React

### Frontend que Consume la API

```typescript
// file: components/NotificationsDashboard.tsx
import React, { useState, useEffect } from 'react';
import { NotificationsAgentClient } from '../sdk/client';

const client = new NotificationsAgentClient('http://localhost:3000', 'web-dashboard');

export function NotificationsDashboard() {
  const [emails, setEmails] = useState([]);
  const [linkedin, setLinkedIn] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    refreshData();
  }, []);

  const refreshData = async () => {
    setLoading(true);
    try {
      const [emailsData, linkedinData] = await Promise.all([
        client.getEmails(1),
        client.getLinkedInNotifications(1)
      ]);

      setEmails(emailsData);
      setLinkedIn(linkedinData);
    } finally {
      setLoading(false);
    }
  };

  const generateReport = async () => {
    setLoading(true);
    try {
      const result = await client.generateReport();
      if (result.success) {
        alert(`✅ Reporte: ${result.reportPath}`);
        // Descargar el reporte
        window.location.href = `/api/v1/reports/${result.reportPath.split('/').pop()}`;
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <h1>📊 Centro de Notificaciones</h1>

      <button onClick={generateReport} disabled={loading}>
        📄 Generar Reporte
      </button>

      <section>
        <h2>📧 Correos ({emails.length})</h2>
        <ul>
          {emails.map(email => (
            <li key={email.id}>
              <strong>{email.sender}</strong>: {email.subject}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>💼 LinkedIn ({linkedin.length})</h2>
        <ul>
          {linkedin.map(notif => (
            <li key={notif.id}>
              <strong>{notif.actor.name}</strong>: {notif.action}
            </li>
          ))}
        </ul>
      </section>

      <button onClick={refreshData} disabled={loading}>
        🔄 Actualizar
      </button>
    </div>
  );
}
```

---

## 9. Procesamiento de Datos (Pipeline)

### Agente que Procesa Correos

```typescript
// file: email-processor.ts
import { NotificationsAgentClient } from './sdk/client.js';

const client = new NotificationsAgentClient('http://localhost:3000', 'processor');

interface ProcessedEmail {
  from: string;
  subject: string;
  tags: string[];
  priority: 'high' | 'normal' | 'low';
}

async function processEmails(): Promise<ProcessedEmail[]> {
  // Obtener correos
  const emails = await client.getEmails(1);

  // Procesar y etiquetar
  return emails.map(email => {
    const isUrgent = email.subject.toLowerCase().includes('urgent');
    const isFromBoss = email.sender.includes('jefe') || email.sender.includes('boss');
    
    return {
      from: email.sender,
      subject: email.subject,
      tags: [
        isUrgent && 'urgent',
        isFromBoss && 'boss-email',
        email.subject.includes('proyecto') && 'project'
      ].filter(Boolean) as string[],
      priority: isUrgent || isFromBoss ? 'high' : 'normal'
    };
  });
}

// Ejecutar
processEmails().then(processed => {
  console.log('Correos procesados:');
  processed.forEach(email => {
    console.log(`[${email.priority.toUpperCase()}] ${email.from}`);
    console.log(`  ${email.subject}`);
    console.log(`  Tags: ${email.tags.join(', ')}`);
  });
});
```

---

## 10. Monitoreo de Salud

### Agente que Monitorea otros Agentes

```typescript
// file: health-monitor.ts
import { NotificationsAgentClient } from './sdk/client.js';

const client = new NotificationsAgentClient('http://localhost:3000', 'monitor');

async function monitorHealth() {
  try {
    const isAlive = await client.health();
    const status = await client.getStatus();

    console.log('📊 Estado del Agente de Notificaciones:');
    console.log(`   Activo: ${isAlive ? '✅' : '❌'}`);
    console.log(`   Versión: ${status.version}`);
    console.log(`   Gmail: ${status.services.gmail}`);
    console.log(`   LinkedIn: ${status.services.linkedin}`);
    console.log(`   Reportes: ${status.services.reports}`);

    // Alertar si algo no está bien
    if (!isAlive) {
      console.error('⚠️ ALERTA: El agente no está respondiendo');
    }
  } catch (error) {
    console.error('❌ Error verificando estado:', error.message);
  }
}

// Ejecutar cada 5 minutos
setInterval(monitorHealth, 5 * 60 * 1000);
monitorHealth();
```

---

**¡Estos ejemplos cubren la mayoría de casos de uso!** Adapta según tus necesidades. 🚀
