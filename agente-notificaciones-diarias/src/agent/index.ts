import { GmailService } from '../services/gmail.service.js';
import { LinkedInService } from '../services/linkedin.service.js';
import { ReportService } from '../services/report.service.js';
import { DailyReport, ReportItem, EmailMessage, LinkedInNotification } from '../types/index.js';
import { createLogger } from '../utils/logger.js';
import fs from 'fs';
import path from 'path';
import config from '../config/env.js';

const logger = createLogger('Agent');

export class Agent {
  private gmailService: GmailService;
  private linkedInService: LinkedInService;
  private reportService: ReportService;

  constructor() {
    this.gmailService = new GmailService();
    this.linkedInService = new LinkedInService();
    this.reportService = new ReportService();
  }

  async initialize(): Promise<void> {
    logger.info('🔐 Autenticando servicios...');
    try {
      await this.gmailService.authenticate();
      logger.info('✅ Gmail autenticado');
    } catch (error) {
      logger.warn('⚠️ Gmail requiere autenticación manual:', error);
    }
  }

  async generateDailyReport(): Promise<string> {
    const now = new Date();
    const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const endOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);

    return this.generateReportForDateRange(startOfDay, endOfDay);
  }

  async generateReportForDateRange(startDate: Date, endDate: Date): Promise<string> {
    logger.info(`📊 Generando reporte para ${startDate.toDateString()} - ${endDate.toDateString()}`);

    // Obtener correos
    logger.info('📧 Obteniendo correos...');
    const emails = await this.gmailService.getEmailsByDateRange(startDate, endDate, 20);
    logger.info(`✅ ${emails.length} correo(s) encontrado(s)`);

    // Obtener notificaciones de LinkedIn
    logger.info('💼 Obteniendo notificaciones de LinkedIn...');
    const linkedinNotifications = await this.linkedInService.getRecentActivity(startDate, endDate);
    logger.info(`✅ ${linkedinNotifications.length} notificación(es) de LinkedIn`);

    // Construir items del reporte
    const emailItems: ReportItem[] = emails.map((email) => ({
      title: email.subject,
      summary: email.snippet || email.body.substring(0, 200),
      source: email.sender,
      timestamp: email.date,
    }));

    const linkedinItems: ReportItem[] = linkedinNotifications.map((notif) => ({
      title: notif.action,
      summary: notif.description,
      source: notif.actor.name,
      timestamp: notif.timestamp,
      url: notif.url,
    }));

    // Construir reporte
    const report: DailyReport = {
      generatedAt: new Date(),
      period: {
        startDate,
        endDate,
      },
      sections: {
        emails: {
          title: 'Correos',
          count: emailItems.length,
          items: emailItems,
        },
        linkedin: {
          title: 'LinkedIn',
          count: linkedinItems.length,
          items: linkedinItems,
        },
      },
    };

    // Generar PDF
    logger.info('📄 Generando PDF...');
    const reportPath = this.reportService.generatePDF(report);
    logger.info(`✅ PDF generado en: ${reportPath}`);

    return reportPath;
  }

  async getEmails(startDate: Date, endDate: Date): Promise<EmailMessage[]> {
    logger.info(`📧 Obteniendo correos de ${startDate.toDateString()} a ${endDate.toDateString()}`);
    return this.gmailService.getEmailsByDateRange(startDate, endDate, 50);
  }

  async getLinkedInNotifications(startDate: Date, endDate: Date): Promise<LinkedInNotification[]> {
    logger.info(`💼 Obteniendo notificaciones LinkedIn de ${startDate.toDateString()} a ${endDate.toDateString()}`);
    return this.linkedInService.getRecentActivity(startDate, endDate);
  }

  listGeneratedReports(): Array<{ filename: string; date: Date; path: string }> {
    try {
      const reportsDir = config.REPORT_OUTPUT_DIR;
      const files = fs.readdirSync(reportsDir);

      return files
        .filter((f) => f.endsWith('.pdf'))
        .map((filename) => {
          const filepath = path.join(reportsDir, filename);
          const stats = fs.statSync(filepath);
          return {
            filename,
            date: stats.mtime,
            path: filepath,
          };
        })
        .sort((a, b) => b.date.getTime() - a.date.getTime());
    } catch (error) {
      logger.error('Error listando reportes', error);
      return [];
    }
  }

  getReportPath(filename: string): string {
    const filepath = path.join(config.REPORT_OUTPUT_DIR, filename);

    // Validar que el archivo existe y está dentro del directorio permitido
    const realPath = path.resolve(filepath);
    const reportDir = path.resolve(config.REPORT_OUTPUT_DIR);

    if (!realPath.startsWith(reportDir)) {
      throw new Error('Acceso denegado: ruta inválida');
    }

    if (!fs.existsSync(realPath)) {
      throw new Error(`Reporte no encontrado: ${filename}`);
    }

    return realPath;
  }

  async setGmailTokenFromCode(code: string): Promise<void> {
    await this.gmailService.setTokenFromCode(code);
    logger.info('✅ Token de Gmail configurado');
  }

  async setLinkedInAccessToken(token: string): Promise<void> {
    await this.linkedInService.setAccessToken(token);
    logger.info('✅ Token de LinkedIn configurado');
  }
}
