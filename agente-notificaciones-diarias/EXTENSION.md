# Guía de Extensión - Agente de Notificaciones

Este documento explica cómo extender el agente con nuevas funcionalidades.

## 1. Agregar un Nuevo Servicio (ej: Slack)

### Paso 1: Crear el Servicio

```typescript
// src/services/slack.service.ts
import axios from 'axios';
import config from '../config/env.js';

export class SlackService {
  private webhookUrl: string;

  constructor() {
    this.webhookUrl = config.SLACK_WEBHOOK_URL;
  }

  async sendMessage(title: string, text: string): Promise<void> {
    const payload = {
      text: title,
      blocks: [
        {
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: text,
          },
        },
      ],
    };

    await axios.post(this.webhookUrl, payload);
  }

  async sendReportSummary(
    emailCount: number,
    linkedinCount: number
  ): Promise<void> {
    const text = `
📊 *Reporte Diario de Notificaciones*
📧 Correos nuevos: ${emailCount}
💼 Notificaciones LinkedIn: ${linkedinCount}
    `;

    await this.sendMessage('Resumen Diario', text);
  }
}
```

### Paso 2: Agregar Variable de Entorno

```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Paso 3: Integrar en el Agent

```typescript
// src/agent/index.ts
import { SlackService } from '../services/slack.service.js';

export class Agent {
  private slackService: SlackService;

  constructor() {
    // ...
    this.slackService = new SlackService();
  }

  async generateDailyReport(): Promise<string> {
    // ... código existente ...

    // Enviar resumen a Slack
    await this.slackService.sendReportSummary(
      report.sections.emails.count,
      report.sections.linkedin.count
    );

    return reportPath;
  }
}
```

## 2. Enviar Reporte por Email

```typescript
// src/services/email.service.ts
import nodemailer from 'nodemailer';
import config from '../config/env.js';
import fs from 'fs';

export class EmailService {
  private transporter;

  constructor() {
    this.transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: config.GMAIL_USER_EMAIL,
        pass: config.GMAIL_APP_PASSWORD, // Contraseña de aplicación
      },
    });
  }

  async sendReport(
    reportPath: string,
    recipient: string
  ): Promise<void> {
    const filename = reportPath.split('/').pop();

    await this.transporter.sendMail({
      from: config.GMAIL_USER_EMAIL,
      to: recipient,
      subject: `Reporte Diario de Notificaciones - ${new Date().toLocaleDateString()}`,
      html: `
        <h2>Reporte Diario de Notificaciones</h2>
        <p>Tu reporte de correos y notificaciones LinkedIn está listo.</p>
        <p>Fecha: ${new Date().toLocaleDateString()}</p>
      `,
      attachments: [
        {
          filename,
          path: reportPath,
        },
      ],
    });
  }
}
```

## 3. Crear un Dashboard Web

```typescript
// src/server/index.ts
import express from 'express';
import fs from 'fs';
import path from 'path';
import config from '../config/env.js';
import { Agent } from '../agent/index.js';

const app = express();
const agent = new Agent();

// Mostrar lista de reportes generados
app.get('/reports', (req, res) => {
  const files = fs.readdirSync(config.REPORT_OUTPUT_DIR);
  const reports = files
    .filter((f) => f.endsWith('.pdf'))
    .map((f) => ({
      name: f,
      path: `/reports/${f}`,
      date: fs.statSync(path.join(config.REPORT_OUTPUT_DIR, f)).mtime,
    }))
    .sort((a, b) => b.date.getTime() - a.date.getTime());

  res.json(reports);
});

// Descargar un reporte específico
app.get('/reports/:filename', (req, res) => {
  const filepath = path.join(config.REPORT_OUTPUT_DIR, req.params.filename);
  
  if (!fs.existsSync(filepath)) {
    return res.status(404).json({ error: 'Reporte no encontrado' });
  }

  res.download(filepath);
});

// Generar reporte bajo demanda
app.post('/generate', async (req, res) => {
  try {
    const reportPath = await agent.generateDailyReport();
    res.json({ success: true, path: reportPath });
  } catch (error) {
    res.status(500).json({ error: String(error) });
  }
});

app.listen(3000, () => {
  console.log('📊 Dashboard disponible en http://localhost:3000');
});
```

## 4. Agregar Soporte para Notificaciones de Teams

```typescript
// src/services/teams.service.ts
import axios from 'axios';
import config from '../config/env.js';

export class TeamsService {
  private webhookUrl: string;

  constructor() {
    this.webhookUrl = config.TEAMS_WEBHOOK_URL;
  }

  async sendReport(emailCount: number, linkedinCount: number): Promise<void> {
    const payload = {
      @type: 'MessageCard',
      @context: 'https://schema.org/extensions',
      summary: 'Reporte Diario de Notificaciones',
      themeColor: '0078D4',
      title: '📊 Reporte Diario de Notificaciones',
      sections: [
        {
          activityTitle: new Date().toLocaleDateString(),
          facts: [
            {
              name: '📧 Correos nuevos:',
              value: String(emailCount),
            },
            {
              name: '💼 Notificaciones LinkedIn:',
              value: String(linkedinCount),
            },
          ],
        },
      ],
    };

    await axios.post(this.webhookUrl, payload);
  }
}
```

## 5. Implementar Web Scraping para LinkedIn

```typescript
// src/services/linkedin-scraper.service.ts
import puppeteer from 'puppeteer';
import { LinkedInNotification } from '../types/index.js';

export class LinkedInScraperService {
  async getNotifications(
    email: string,
    password: string
  ): Promise<LinkedInNotification[]> {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    try {
      // Ir a LinkedIn
      await page.goto('https://www.linkedin.com/feed/');

      // Login (si es necesario)
      // ... código de login ...

      // Extraer notificaciones
      const notifications = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('[data-test-id="notification"]')).map((el) => ({
          title: el.querySelector('h3')?.textContent || '',
          description: el.querySelector('p')?.textContent || '',
          timestamp: new Date(),
        }));
      });

      return notifications;
    } finally {
      await browser.close();
    }
  }
}
```

## 6. Agregar Filtros y Búsqueda Avanzada

```typescript
// src/services/gmail.service.ts (extensión)
async getEmailsByFilter(filter: EmailFilter): Promise<EmailMessage[]> {
  const queries: string[] = [];

  if (filter.from) {
    queries.push(`from:${filter.from}`);
  }
  if (filter.subject) {
    queries.push(`subject:${filter.subject}`);
  }
  if (filter.labels) {
    queries.push(`label:${filter.labels.join(',')}`);
  }

  const q = queries.join(' ');
  // ... rest de la lógica ...
}

interface EmailFilter {
  from?: string;
  subject?: string;
  labels?: string[];
  startDate?: Date;
  endDate?: Date;
}
```

## 7. Testing

```typescript
// tests/agent.test.ts
import { Agent } from '../src/agent/index.js';

describe('Agent', () => {
  let agent: Agent;

  beforeEach(() => {
    agent = new Agent();
  });

  it('should generate a daily report', async () => {
    const reportPath = await agent.generateDailyReport();
    expect(reportPath).toBeDefined();
    expect(reportPath).toContain('reporte-diario');
  });
});
```

## 8. Configuración de CI/CD

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm install
      - run: npm run build
      - run: npm test
```

---

Estos ejemplos te muestran cómo:
- Agregar nuevos servicios integrados
- Enviar reportes por múltiples canales
- Crear interfaces web
- Implementar scraping
- Agregar filtros avanzados
- Implementar testing

¡Personaliza según tus necesidades!
