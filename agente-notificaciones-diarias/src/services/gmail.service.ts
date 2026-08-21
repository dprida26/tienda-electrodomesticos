import { google } from 'googleapis';
import { EmailMessage } from '../types/index.js';
import config from '../config/env.js';
import fs from 'fs/promises';
import path from 'path';

const SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'];
const TOKEN_PATH = 'gmail-token.json';

export class GmailService {
  private oauth2Client;
  private gmail;

  constructor() {
    this.oauth2Client = new google.auth.OAuth2(
      config.GMAIL_CLIENT_ID,
      config.GMAIL_CLIENT_SECRET,
      config.GMAIL_REDIRECT_URI
    );
    this.gmail = google.gmail({ version: 'v1', auth: this.oauth2Client });
  }

  async authenticate(): Promise<void> {
    try {
      const token = await fs.readFile(TOKEN_PATH, 'utf-8');
      this.oauth2Client.setCredentials(JSON.parse(token));
    } catch (err) {
      await this.getNewToken();
    }
  }

  private async getNewToken(): Promise<void> {
    const authUrl = this.oauth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: SCOPES,
    });

    console.log('Authorize this app by visiting this url:', authUrl);
    // En producción, esto debería ser un callback HTTP
    // Por ahora, lanzamos un error pidiendo al usuario que lo haga manualmente
    throw new Error(
      `Please visit ${authUrl} and provide the authorization code`
    );
  }

  async setTokenFromCode(code: string): Promise<void> {
    const { tokens } = await this.oauth2Client.getToken(code);
    this.oauth2Client.setCredentials(tokens);
    await fs.writeFile(TOKEN_PATH, JSON.stringify(tokens, null, 2));
  }

  async getNewEmails(maxResults: number = 10): Promise<EmailMessage[]> {
    try {
      const response = await this.gmail.users.messages.list({
        userId: 'me',
        q: 'is:unread',
        maxResults,
      });

      if (!response.data.messages) {
        return [];
      }

      const messages: EmailMessage[] = [];

      for (const message of response.data.messages) {
        const fullMessage = await this.gmail.users.messages.get({
          userId: 'me',
          id: message.id!,
          format: 'full',
        });

        const headers = fullMessage.data.payload?.headers || [];
        const subject =
          headers.find((h) => h.name === 'Subject')?.value || 'Sin asunto';
        const sender =
          headers.find((h) => h.name === 'From')?.value || 'Desconocido';
        const date = new Date(
          headers.find((h) => h.name === 'Date')?.value || new Date()
        );

        let body = '';
        if (fullMessage.data.payload?.parts) {
          const textPart = fullMessage.data.payload.parts.find(
            (p) => p.mimeType === 'text/plain'
          );
          if (textPart?.body?.data) {
            body = Buffer.from(textPart.body.data, 'base64').toString('utf-8');
          }
        } else if (fullMessage.data.payload?.body?.data) {
          body = Buffer.from(fullMessage.data.payload.body.data, 'base64').toString(
            'utf-8'
          );
        }

        messages.push({
          id: message.id!,
          threadId: message.threadId!,
          sender,
          subject,
          snippet: fullMessage.data.snippet || '',
          body,
          date,
          labels: fullMessage.data.labelIds || [],
          isUnread: true,
        });
      }

      return messages;
    } catch (error) {
      console.error('Error fetching emails:', error);
      throw error;
    }
  }

  async getEmailsByDateRange(
    startDate: Date,
    endDate: Date,
    maxResults: number = 20
  ): Promise<EmailMessage[]> {
    try {
      const query = `after:${Math.floor(startDate.getTime() / 1000)} before:${Math.floor(endDate.getTime() / 1000)}`;

      const response = await this.gmail.users.messages.list({
        userId: 'me',
        q: query,
        maxResults,
      });

      if (!response.data.messages) {
        return [];
      }

      const messages: EmailMessage[] = [];

      for (const message of response.data.messages) {
        const fullMessage = await this.gmail.users.messages.get({
          userId: 'me',
          id: message.id!,
          format: 'full',
        });

        const headers = fullMessage.data.payload?.headers || [];
        const subject =
          headers.find((h) => h.name === 'Subject')?.value || 'Sin asunto';
        const sender =
          headers.find((h) => h.name === 'From')?.value || 'Desconocido';
        const date = new Date(
          headers.find((h) => h.name === 'Date')?.value || new Date()
        );

        let body = '';
        if (fullMessage.data.payload?.parts) {
          const textPart = fullMessage.data.payload.parts.find(
            (p) => p.mimeType === 'text/plain'
          );
          if (textPart?.body?.data) {
            body = Buffer.from(textPart.body.data, 'base64').toString('utf-8');
          }
        } else if (fullMessage.data.payload?.body?.data) {
          body = Buffer.from(fullMessage.data.payload.body.data, 'base64').toString(
            'utf-8'
          );
        }

        messages.push({
          id: message.id!,
          threadId: message.threadId!,
          sender,
          subject,
          snippet: fullMessage.data.snippet || '',
          body,
          date,
          labels: fullMessage.data.labelIds || [],
          isUnread: false,
        });
      }

      return messages;
    } catch (error) {
      console.error('Error fetching emails by date range:', error);
      throw error;
    }
  }
}
