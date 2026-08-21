import { google } from 'googleapis';
import { config } from './config';

export type EmailCategory = 'personal' | 'trabajo' | 'promocion' | 'social' | 'educacion' | 'otro';

export interface EmailMessage {
  id: string;
  asunto: string;
  remitente: string;
  emailRemitente: string;
  fecha: Date;
  cuerpo: string;
  tieneAdjuntos: boolean;
  categoria: EmailCategory;
}

function sanitizeSubject(subject: string): string {
  return subject
    // Eliminar emojis y símbolos que Helvetica no puede renderizar
    .replace(/[\u{1F000}-\u{1FFFF}]/gu, '')
    .replace(/[\u{2600}-\u{27BF}]/gu, '')
    .replace(/[\u{FE00}-\u{FE0F}]/gu, '')
    .replace(/[\u{E0000}-\u{E007F}]/gu, '')
    .replace(/[\u{1F900}-\u{1F9FF}]/gu, '')
    .replace(/[\u{2300}-\u{23FF}]/gu, '')
    .replace(/[\u{2B00}-\u{2BFF}]/gu, '')
    // Limpiar caracteres de control y basura
    .replace(/[\u0000-\u001F\u007F-\u009F]/g, '')
    .replace(/[\u00D8-\u00DD]=/g, '')
    .replace(/\s{2,}/g, ' ')
    .trim();
}

function categorizeEmail(from: string, subject: string): EmailCategory {
  const email = from.toLowerCase();
  const subj = subject.toLowerCase();

  // Educación / cursos
  if (/coursera|udemy|edx|platzi|domestika|skillshare|linkedin\.com.*learning/i.test(email) ||
      /curso|learn|skill|certif/i.test(subj)) {
    return 'educacion';
  }

  // Social / redes
  if (/linkedin|facebook|twitter|instagram|tiktok|reddit/i.test(email) ||
      /búsqueda|conexion|seguidor|invitaci/i.test(subj)) {
    return 'social';
  }

  // Promociones / marketing
  if (/no-?re(ply|sponder)|newsletter|promo|market|info@|comunicaciones@|news@/i.test(email) ||
      /descuento|oferta|gratis|sale|%\s*menos|duplica|millas|premium/i.test(subj)) {
    return 'promocion';
  }

  // Trabajo
  if (/jira|slack|github|gitlab|bitbucket|asana|trello|notion/i.test(email) ||
      /deploy|sprint|release|standup|reunión|meeting/i.test(subj)) {
    return 'trabajo';
  }

  return 'otro';
}

function createGmailClient() {
  const oauth2Client = new google.auth.OAuth2(
    config.google.clientId,
    config.google.clientSecret,
  );

  oauth2Client.setCredentials({
    refresh_token: config.google.refreshToken,
  });

  return google.gmail({ version: 'v1', auth: oauth2Client });
}

function stripHtml(html: string): string {
  return html
    // Eliminar bloques no visibles (incluyendo noscript, title, meta)
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<head[^>]*>[\s\S]*?<\/head>/gi, '')
    .replace(/<noscript[^>]*>[\s\S]*?<\/noscript>/gi, '')
    .replace(/<title[^>]*>[\s\S]*?<\/title>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    // Eliminar bloques CSS inline que a veces quedan fuera de <style>
    .replace(/[a-z\s,.*#:>{}\[\]]+\{[^}]*\}/gi, '')
    // Eliminar declaraciones CSS sueltas (font-family, font-size, etc.)
    .replace(/[\w-]+\s*:\s*[^;{}<>]{1,60}\s*!important\s*;?/gi, '')
    // Eliminar imágenes y referencias CID
    .replace(/<img[^>]*>/gi, '')
    .replace(/\[cid:[^\]]*\]/gi, '')
    // Convertir saltos de línea HTML
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n')
    .replace(/<\/div>/gi, '\n')
    .replace(/<\/tr>/gi, '\n')
    .replace(/<\/li>/gi, '\n')
    .replace(/<\/h[1-6]>/gi, '\n')
    // Eliminar todas las etiquetas HTML restantes
    .replace(/<[^>]+>/g, '')
    // Decodificar entidades HTML comunes
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&rsquo;/g, "'")
    .replace(/&lsquo;/g, "'")
    .replace(/&rdquo;/g, '"')
    .replace(/&ldquo;/g, '"')
    .replace(/&ndash;/g, '-')
    .replace(/&mdash;/g, '--')
    .replace(/&hellip;/g, '...')
    .replace(/&copy;/g, '(c)')
    .replace(/&reg;/g, '(R)')
    .replace(/&#\d+;/g, '')
    .replace(/&\w+;/g, '')
    // Limpiar caracteres no imprimibles y basura Unicode
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '')
    .replace(/[\u007F-\u009F]/g, '')
    .replace(/[\u00AD\u00D0\u00F0]/g, '')
    .replace(/[\u200B-\u200F\u2028-\u202F\u205F-\u206F\uFEFF]/g, '')
    .replace(/\uFFFD/g, '')
    // Eliminar emojis y símbolos Unicode extendidos
    .replace(/[\u{1F000}-\u{1FFFF}]/gu, '')
    .replace(/[\u{2600}-\u{27BF}]/gu, '')
    .replace(/[\u{FE00}-\u{FE0F}]/gu, '')
    // Eliminar secuencias de caracteres no-ASCII repetitivos (basura de encoding)
    .replace(/(?:[\u0080-\u00FF]{2,}\s*){3,}/g, '')
    // Eliminar URLs largas sueltas (no dentro de texto legible)
    .replace(/https?:\/\/\S{80,}/g, '[enlace]')
    // Limpiar espacios y saltos excesivos
    .replace(/[ \t]+/g, ' ')
    .replace(/\n[ \t]+/g, '\n')
    .replace(/[ \t]+\n/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function cleanBody(text: string, maxLength: number = 250): string {
  const lines = text.split('\n')
    .map(l => l.trim())
    .filter(l => l.length > 3)
    .filter(l => !/^https?:\/\//.test(l))           // Solo URLs
    .filter(l => !/^[=-]{3,}$/.test(l))             // Líneas decorativas
    .filter(l => !/[{}]/.test(l))                    // Líneas con CSS/código
    .filter(l => !/:\s*\w+.*!important/.test(l))     // Declaraciones CSS sueltas
    .filter(l => !/^(body|table|td|th|div|span|img|font|sup)\b/i.test(l)) // Selectores CSS
    .filter(l => {
      // Filtrar líneas con demasiados caracteres no-ASCII (basura de encoding)
      const nonAscii = (l.match(/[^\x20-\x7E\u00C0-\u024F]/g) || []).length;
      return nonAscii < l.length * 0.4;
    })
    .slice(0, 6);

  let result = lines.join(' ');

  if (result.length > maxLength) {
    result = result.substring(0, maxLength);
    const lastSpace = result.lastIndexOf(' ');
    result = (lastSpace > 0 ? result.substring(0, lastSpace) : result) + '...';
  }

  return result || '(Sin contenido legible)';
}

function getHeader(headers: { name?: string | null; value?: string | null }[], name: string): string {
  const header = headers.find(h => h.name?.toLowerCase() === name.toLowerCase());
  return header?.value || '';
}

function parseFrom(from: string): { name: string; email: string } {
  const match = from.match(/^(.+?)\s*<(.+?)>$/);
  if (match) {
    return { name: match[1].replace(/"/g, '').trim(), email: match[2] };
  }
  return { name: from, email: from };
}

function decodeBase64Url(data: string): string {
  const base64 = data.replace(/-/g, '+').replace(/_/g, '/');
  return Buffer.from(base64, 'base64').toString('utf-8');
}

function extractBody(payload: any): string {
  // Si el mensaje tiene body directo (texto plano)
  if (payload.mimeType === 'text/plain' && payload.body?.data) {
    return decodeBase64Url(payload.body.data);
  }

  // Si es HTML directo
  if (payload.mimeType === 'text/html' && payload.body?.data) {
    return stripHtml(decodeBase64Url(payload.body.data));
  }

  // Si tiene partes (multipart)
  if (payload.parts) {
    // Primero buscar text/plain
    const textPart = payload.parts.find((p: any) => p.mimeType === 'text/plain');
    if (textPart?.body?.data) {
      return decodeBase64Url(textPart.body.data);
    }

    // Luego buscar text/html
    const htmlPart = payload.parts.find((p: any) => p.mimeType === 'text/html');
    if (htmlPart?.body?.data) {
      return stripHtml(decodeBase64Url(htmlPart.body.data));
    }

    // Buscar recursivamente en partes anidadas (multipart/alternative dentro de multipart/mixed)
    for (const part of payload.parts) {
      if (part.parts) {
        const nested = extractBody(part);
        if (nested) return nested;
      }
    }
  }

  return '';
}

export async function fetchTodayEmails(): Promise<EmailMessage[]> {
  const gmail = createGmailClient();

  // Construir query para correos de hoy
  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth() + 1;
  const day = today.getDate();
  const query = `in:inbox after:${year}/${month}/${day - 1} before:${year}/${month}/${day + 1}`;

  // Listar IDs de mensajes
  const listResponse = await gmail.users.messages.list({
    userId: 'me',
    q: query,
    maxResults: 100,
  });

  const messageIds = listResponse.data.messages || [];

  if (messageIds.length === 0) {
    return [];
  }

  // Obtener detalle de cada mensaje
  const emails: EmailMessage[] = [];

  for (const msg of messageIds) {
    const detail = await gmail.users.messages.get({
      userId: 'me',
      id: msg.id!,
      format: 'full',
    });

    const headers = detail.data.payload?.headers || [];
    const subject = getHeader(headers, 'Subject');
    const from = getHeader(headers, 'From');
    const date = getHeader(headers, 'Date');
    const parsed = parseFrom(from);

    const bodyRaw = extractBody(detail.data.payload);
    const hasAttachments = detail.data.payload?.parts?.some(
      (p: any) => p.filename && p.filename.length > 0
    ) || false;

    // Verificar que el correo sea realmente de hoy
    const emailDate = new Date(date);
    const todayStart = new Date(today);
    todayStart.setHours(0, 0, 0, 0);
    const todayEnd = new Date(today);
    todayEnd.setHours(23, 59, 59, 999);

    if (emailDate >= todayStart && emailDate <= todayEnd) {
      const cleanSubject = sanitizeSubject(subject) || '(Sin asunto)';
      emails.push({
        id: msg.id!,
        asunto: cleanSubject,
        remitente: parsed.name,
        emailRemitente: parsed.email,
        fecha: emailDate,
        cuerpo: cleanBody(bodyRaw),
        tieneAdjuntos: hasAttachments,
        categoria: categorizeEmail(from, cleanSubject),
      });
    }
  }

  // Ordenar por fecha descendente
  emails.sort((a, b) => b.fecha.getTime() - a.fecha.getTime());

  return emails;
}
