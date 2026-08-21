import axios from 'axios';
import { LinkedInNotification } from '../types/index.js';
import config from '../config/env.js';

export class LinkedInService {
  private accessToken: string;
  private baseUrl = 'https://api.linkedin.com/v2';

  constructor() {
    this.accessToken = config.LINKEDIN_ACCESS_TOKEN;
  }

  private getHeaders() {
    return {
      Authorization: `Bearer ${this.accessToken}`,
      'Content-Type': 'application/json',
    };
  }

  async getNotifications(): Promise<LinkedInNotification[]> {
    try {
      // Nota: LinkedIn no expone un endpoint público para notificaciones
      // Esta es una implementación alternativa que intenta obtener actividad reciente
      const response = await axios.get(
        `${this.baseUrl}/me/notification-settings`,
        {
          headers: this.getHeaders(),
        }
      );

      return [];
    } catch (error) {
      console.error('Error fetching LinkedIn notifications:', error);
      throw error;
    }
  }

  async getRecentActivity(
    startDate: Date,
    endDate: Date
  ): Promise<LinkedInNotification[]> {
    try {
      // LinkedIn REST API v2 tiene limitaciones para notificaciones
      // Alternativa: usar web scraping o acceso a través de Unofficial API
      // Por ahora retornamos un array vacío como placeholder

      console.log(
        `Fetching LinkedIn activity from ${startDate} to ${endDate}`
      );
      return [];
    } catch (error) {
      console.error('Error fetching LinkedIn activity:', error);
      throw error;
    }
  }

  async setAccessToken(token: string): Promise<void> {
    this.accessToken = token;
  }

  // Alternativa: usar Puppeteer para web scraping de notificaciones
  async getNotificationsViaScraping(): Promise<LinkedInNotification[]> {
    console.log(
      'LinkedIn web scraping not implemented yet. Please use the official API.'
    );
    return [];
  }
}
