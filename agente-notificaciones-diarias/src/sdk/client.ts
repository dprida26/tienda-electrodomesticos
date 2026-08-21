import axios, { AxiosInstance } from 'axios';

export interface GenerateReportResponse {
  success: boolean;
  reportPath?: string;
  error?: string;
  timestamp: Date;
}

export interface EmailData {
  id: string;
  sender: string;
  subject: string;
  snippet: string;
  date: Date;
}

export interface LinkedInData {
  id: string;
  type: string;
  actor: { name: string };
  action: string;
  timestamp: Date;
  description: string;
}

export interface EventPayload {
  type: 'GENERATE_REPORT' | 'GET_EMAILS' | 'GET_LINKEDIN';
  payload?: Record<string, unknown>;
  sourceAgent: string;
}

/**
 * Cliente SDK para interactuar con el Agente de Notificaciones Diarias
 * Permite que otros agentes invoquen funcionalidades
 */
export class NotificationsAgentClient {
  private client: AxiosInstance;
  private baseUrl: string;
  private agentId: string;

  constructor(baseUrl: string = 'http://localhost:3000', agentId: string = 'unknown-agent') {
    this.baseUrl = baseUrl;
    this.agentId = agentId;

    this.client = axios.create({
      baseURL: `${baseUrl}/api/v1`,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Verificar que el servidor está activo
   */
  async health(): Promise<boolean> {
    try {
      const response = await this.client.get('/health');
      return response.data.status === 'ok';
    } catch {
      return false;
    }
  }

  /**
   * Obtener estado del agente
   */
  async getStatus(): Promise<any> {
    const response = await this.client.get('/status');
    return response.data;
  }

  /**
   * Generar reporte bajo demanda
   */
  async generateReport(): Promise<GenerateReportResponse> {
    try {
      const response = await this.client.post('/reports/generate');
      return {
        success: true,
        reportPath: response.data.reportPath,
        timestamp: new Date(response.data.timestamp),
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || error.message,
        timestamp: new Date(),
      };
    }
  }

  /**
   * Generar reporte para un rango de fechas específico
   */
  async generateReportForRange(startDate: Date, endDate: Date): Promise<GenerateReportResponse> {
    try {
      const response = await this.client.post('/reports/generate-range', {
        startDate: startDate.toISOString(),
        endDate: endDate.toISOString(),
      });
      return {
        success: true,
        reportPath: response.data.reportPath,
        timestamp: new Date(response.data.timestamp),
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || error.message,
        timestamp: new Date(),
      };
    }
  }

  /**
   * Generar reporte y notificar vía webhook cuando esté listo
   */
  async generateReportWithCallback(webhookUrl: string): Promise<{ success: boolean; taskId: string }> {
    try {
      const response = await this.client.post('/reports/generate-with-callback', {
        webhookUrl,
        agentId: this.agentId,
      });
      return {
        success: true,
        taskId: response.data.taskId,
      };
    } catch (error: any) {
      throw new Error(error.response?.data?.error || error.message);
    }
  }

  /**
   * Obtener correos de los últimos N días
   */
  async getEmails(days: number = 1): Promise<EmailData[]> {
    try {
      const response = await this.client.get('/emails', {
        params: { days },
      });
      return response.data.data || [];
    } catch (error: any) {
      console.error('Error obteniendo correos:', error.message);
      return [];
    }
  }

  /**
   * Obtener notificaciones de LinkedIn de los últimos N días
   */
  async getLinkedInNotifications(days: number = 1): Promise<LinkedInData[]> {
    try {
      const response = await this.client.get('/linkedin/notifications', {
        params: { days },
      });
      return response.data.data || [];
    } catch (error: any) {
      console.error('Error obteniendo notificaciones LinkedIn:', error.message);
      return [];
    }
  }

  /**
   * Listar todos los reportes generados
   */
  async listReports(): Promise<Array<{ filename: string; date: Date; path: string }>> {
    try {
      const response = await this.client.get('/reports');
      return (response.data.data || []).map((report: any) => ({
        ...report,
        date: new Date(report.date),
      }));
    } catch (error: any) {
      console.error('Error listando reportes:', error.message);
      return [];
    }
  }

  /**
   * Descargar un reporte específico
   */
  async downloadReport(filename: string): Promise<Buffer> {
    try {
      const response = await this.client.get(`/reports/${filename}`, {
        responseType: 'arraybuffer',
      });
      return Buffer.from(response.data);
    } catch (error: any) {
      throw new Error(`Error descargando reporte: ${error.message}`);
    }
  }

  /**
   * Enviar evento al agente
   */
  async sendEvent(payload: EventPayload): Promise<any> {
    try {
      const response = await this.client.post('/events', {
        ...payload,
        sourceAgent: this.agentId,
      });
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.error || error.message);
    }
  }

  /**
   * Enviar evento GENERATE_REPORT
   */
  async requestGenerateReport(): Promise<any> {
    return this.sendEvent({
      type: 'GENERATE_REPORT',
      payload: {},
      sourceAgent: this.agentId,
    });
  }

  /**
   * Enviar evento GET_EMAILS
   */
  async requestGetEmails(days: number = 1): Promise<any> {
    return this.sendEvent({
      type: 'GET_EMAILS',
      payload: { days },
      sourceAgent: this.agentId,
    });
  }

  /**
   * Enviar evento GET_LINKEDIN
   */
  async requestGetLinkedIn(days: number = 1): Promise<any> {
    return this.sendEvent({
      type: 'GET_LINKEDIN',
      payload: { days },
      sourceAgent: this.agentId,
    });
  }

  /**
   * Obtener documentación de la API
   */
  async getApiDocs(): Promise<any> {
    try {
      const response = await this.client.get('/docs');
      return response.data;
    } catch (error: any) {
      console.error('Error obteniendo documentación:', error.message);
      return null;
    }
  }
}

// Exportar instancia singleton por defecto
export const createClient = (baseUrl?: string, agentId?: string) => {
  return new NotificationsAgentClient(baseUrl, agentId);
};
