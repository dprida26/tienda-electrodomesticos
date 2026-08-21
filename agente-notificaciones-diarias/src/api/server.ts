import express, { Express, Request, Response } from 'express';
import { Agent } from '../agent/index.js';
import { createLogger } from '../utils/logger.js';
import config from '../config/env.js';

const logger = createLogger('API');

export class NotificationsServer {
  private app: Express;
  private agent: Agent;
  private port: number = 3000;

  constructor(agent: Agent) {
    this.app = express();
    this.agent = agent;
    this.setupMiddleware();
    this.setupRoutes();
  }

  private setupMiddleware(): void {
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));

    // Logging de requests
    this.app.use((req, res, next) => {
      logger.info(`${req.method} ${req.path}`);
      next();
    });
  }

  private setupRoutes(): void {
    // Health check
    this.app.get('/health', (req: Request, res: Response) => {
      res.json({ status: 'ok', timestamp: new Date() });
    });

    // Generar reporte bajo demanda
    this.app.post('/api/v1/reports/generate', async (req: Request, res: Response) => {
      try {
        logger.info('Generando reporte bajo demanda');
        const reportPath = await this.agent.generateDailyReport();
        res.json({
          success: true,
          message: 'Reporte generado exitosamente',
          reportPath,
          timestamp: new Date(),
        });
      } catch (error) {
        logger.error('Error generando reporte', error);
        res.status(500).json({
          success: false,
          error: String(error),
          timestamp: new Date(),
        });
      }
    });

    // Generar reporte para un rango de fechas específico
    this.app.post('/api/v1/reports/generate-range', async (req: Request, res: Response) => {
      try {
        const { startDate, endDate } = req.body;

        if (!startDate || !endDate) {
          return res.status(400).json({
            success: false,
            error: 'startDate y endDate son requeridos',
          });
        }

        logger.info(`Generando reporte para rango: ${startDate} - ${endDate}`);
        const reportPath = await this.agent.generateReportForDateRange(
          new Date(startDate),
          new Date(endDate)
        );

        res.json({
          success: true,
          message: 'Reporte generado exitosamente',
          reportPath,
          range: { startDate, endDate },
          timestamp: new Date(),
        });
      } catch (error) {
        logger.error('Error generando reporte', error);
        res.status(500).json({
          success: false,
          error: String(error),
          timestamp: new Date(),
        });
      }
    });

    // Obtener solo correos
    this.app.get('/api/v1/emails', async (req: Request, res: Response) => {
      try {
        const { days = 1 } = req.query;
        const endDate = new Date();
        const startDate = new Date(endDate.getTime() - parseInt(days as string) * 24 * 60 * 60 * 1000);

        logger.info(`Obteniendo correos de los últimos ${days} día(s)`);
        const emails = await this.agent.getEmails(startDate, endDate);

        res.json({
          success: true,
          count: emails.length,
          data: emails,
          timestamp: new Date(),
        });
      } catch (error) {
        logger.error('Error obteniendo correos', error);
        res.status(500).json({
          success: false,
          error: String(error),
          timestamp: new Date(),
        });
      }
    });

    // Obtener solo notificaciones de LinkedIn
    this.app.get('/api/v1/linkedin/notifications', async (req: Request, res: Response) => {
      try {
        const { days = 1 } = req.query;
        const endDate = new Date();
        const startDate = new Date(endDate.getTime() - parseInt(days as string) * 24 * 60 * 60 * 1000);

        logger.info(`Obteniendo notificaciones LinkedIn de los últimos ${days} día(s)`);
        const notifications = await this.agent.getLinkedInNotifications(startDate, endDate);

        res.json({
          success: true,
          count: notifications.length,
          data: notifications,
          timestamp: new Date(),
        });
      } catch (error) {
        logger.error('Error obteniendo notificaciones LinkedIn', error);
        res.status(500).json({
          success: false,
          error: String(error),
          timestamp: new Date(),
        });
      }
    });

    // Listar reportes generados
    this.app.get('/api/v1/reports', (req: Request, res: Response) => {
      try {
        const reports = this.agent.listGeneratedReports();
        res.json({
          success: true,
          count: reports.length,
          data: reports,
          timestamp: new Date(),
        });
      } catch (error) {
        logger.error('Error listando reportes', error);
        res.status(500).json({
          success: false,
          error: String(error),
          timestamp: new Date(),
        });
      }
    });

    // Descargar reporte específico
    this.app.get('/api/v1/reports/:filename', (req: Request, res: Response) => {
      try {
        const { filename } = req.params;
        const filepath = this.agent.getReportPath(filename);

        logger.info(`Descargando reporte: ${filename}`);
        res.download(filepath);
      } catch (error) {
        logger.error('Error descargando reporte', error);
        res.status(500).json({
          success: false,
          error: String(error),
          timestamp: new Date(),
        });
      }
    });

    // Ejecutar tarea con notificación de webhook
    this.app.post('/api/v1/reports/generate-with-callback', async (req: Request, res: Response) => {
      try {
        const { webhookUrl, agentId } = req.body;

        if (!webhookUrl) {
          return res.status(400).json({
            success: false,
            error: 'webhookUrl es requerido',
          });
        }

        logger.info(`Generando reporte con callback a ${webhookUrl}`);

        // Generar reporte de forma asincrónica
        this.agent.generateDailyReport().then((reportPath) => {
          // Notificar al webhook
          this.notifyWebhook(webhookUrl, {
            status: 'completed',
            reportPath,
            agentId,
            timestamp: new Date(),
          });
        }).catch((error) => {
          // Notificar error
          this.notifyWebhook(webhookUrl, {
            status: 'error',
            error: String(error),
            agentId,
            timestamp: new Date(),
          });
        });

        res.json({
          success: true,
          message: 'Reporte se está generando. Se notificará al webhook cuando esté listo.',
          taskId: Math.random().toString(36).substr(2, 9),
          timestamp: new Date(),
        });
      } catch (error) {
        logger.error('Error generando reporte con callback', error);
        res.status(500).json({
          success: false,
          error: String(error),
          timestamp: new Date(),
        });
      }
    });

    // Status del agente
    this.app.get('/api/v1/status', (req: Request, res: Response) => {
      res.json({
        status: 'running',
        version: '1.0.0',
        services: {
          gmail: 'connected',
          linkedin: 'connected',
          reports: 'ready',
        },
        timestamp: new Date(),
      });
    });

    // Endpoint para que otros agentes envíen eventos
    this.app.post('/api/v1/events', async (req: Request, res: Response) => {
      try {
        const { type, payload, sourceAgent } = req.body;

        logger.info(`Evento recibido de ${sourceAgent}: ${type}`);

        if (type === 'GENERATE_REPORT') {
          const reportPath = await this.agent.generateDailyReport();
          res.json({
            success: true,
            message: 'Reporte generado por evento',
            reportPath,
            sourceAgent,
            timestamp: new Date(),
          });
        } else if (type === 'GET_EMAILS') {
          const { days = 1 } = payload;
          const endDate = new Date();
          const startDate = new Date(endDate.getTime() - days * 24 * 60 * 60 * 1000);
          const emails = await this.agent.getEmails(startDate, endDate);

          res.json({
            success: true,
            count: emails.length,
            data: emails,
            sourceAgent,
            timestamp: new Date(),
          });
        } else if (type === 'GET_LINKEDIN') {
          const { days = 1 } = payload;
          const endDate = new Date();
          const startDate = new Date(endDate.getTime() - days * 24 * 60 * 60 * 1000);
          const notifications = await this.agent.getLinkedInNotifications(startDate, endDate);

          res.json({
            success: true,
            count: notifications.length,
            data: notifications,
            sourceAgent,
            timestamp: new Date(),
          });
        } else {
          res.status(400).json({
            success: false,
            error: `Tipo de evento desconocido: ${type}`,
            timestamp: new Date(),
          });
        }
      } catch (error) {
        logger.error('Error procesando evento', error);
        res.status(500).json({
          success: false,
          error: String(error),
          timestamp: new Date(),
        });
      }
    });

    // Documentación de API
    this.app.get('/api/docs', (req: Request, res: Response) => {
      res.json(this.getApiDocumentation());
    });
  }

  private async notifyWebhook(url: string, payload: unknown): Promise<void> {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        logger.info(`Webhook notificado exitosamente: ${url}`);
      } else {
        logger.warn(`Webhook respondió con status ${response.status}: ${url}`);
      }
    } catch (error) {
      logger.error(`Error notificando webhook ${url}`, error);
    }
  }

  private getApiDocumentation() {
    return {
      title: 'Agente de Notificaciones Diarias - API',
      version: '1.0.0',
      baseUrl: 'http://localhost:3000/api/v1',
      endpoints: [
        {
          path: '/health',
          method: 'GET',
          description: 'Verificar que el servidor está activo',
          response: { status: 'ok', timestamp: '2026-04-17T...' },
        },
        {
          path: '/status',
          method: 'GET',
          description: 'Obtener estado del agente',
          response: {
            status: 'running',
            version: '1.0.0',
            services: { gmail: 'connected', linkedin: 'connected' },
          },
        },
        {
          path: '/reports/generate',
          method: 'POST',
          description: 'Generar reporte diario bajo demanda',
          response: { success: true, reportPath: '...', timestamp: '2026-04-17T...' },
        },
        {
          path: '/reports/generate-range',
          method: 'POST',
          body: { startDate: '2026-04-01', endDate: '2026-04-30' },
          description: 'Generar reporte para un rango de fechas',
          response: { success: true, reportPath: '...', range: {} },
        },
        {
          path: '/emails',
          method: 'GET',
          query: { days: 1 },
          description: 'Obtener correos de los últimos N días',
          response: { success: true, count: 5, data: [] },
        },
        {
          path: '/linkedin/notifications',
          method: 'GET',
          query: { days: 1 },
          description: 'Obtener notificaciones de LinkedIn de los últimos N días',
          response: { success: true, count: 3, data: [] },
        },
        {
          path: '/reports',
          method: 'GET',
          description: 'Listar todos los reportes generados',
          response: { success: true, count: 10, data: [] },
        },
        {
          path: '/reports/:filename',
          method: 'GET',
          description: 'Descargar un reporte específico',
          response: 'PDF binary file',
        },
        {
          path: '/reports/generate-with-callback',
          method: 'POST',
          body: { webhookUrl: 'https://...', agentId: 'agent-1' },
          description: 'Generar reporte y notificar via webhook',
          response: { success: true, taskId: '...', timestamp: '2026-04-17T...' },
        },
        {
          path: '/events',
          method: 'POST',
          body: { type: 'GENERATE_REPORT', payload: {}, sourceAgent: 'agent-2' },
          description: 'Recibir eventos de otros agentes',
          eventTypes: ['GENERATE_REPORT', 'GET_EMAILS', 'GET_LINKEDIN'],
          response: { success: true, message: '...', timestamp: '2026-04-17T...' },
        },
      ],
    };
  }

  start(): void {
    this.app.listen(this.port, () => {
      logger.info(`🚀 Servidor API escuchando en http://localhost:${this.port}`);
      logger.info(`📖 Documentación en http://localhost:${this.port}/api/docs`);
    });
  }

  getApp(): Express {
    return this.app;
  }
}
