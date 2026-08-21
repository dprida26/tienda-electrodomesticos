import PDFDocument from 'pdfkit';
import fs from 'fs';
import path from 'path';
import { EmailMessage, EmailCategory } from './email';
import { config } from './config';

// Colores del tema
const COLORS = {
  primary: '#0F3460',
  accent: '#E94560',
  cardBg: '#F8F9FC',
  cardBorder: '#E2E6EE',
  textDark: '#1A1A2E',
  textMedium: '#4A4A68',
  textLight: '#8888A0',
  white: '#FFFFFF',
  attachBadge: '#E67E22',
  headerBg: '#0F3460',
};

const CATEGORY_CONFIG: Record<EmailCategory, { label: string; color: string }> = {
  personal: { label: 'Personal', color: '#3498DB' },
  trabajo: { label: 'Trabajo', color: '#2ECC71' },
  promocion: { label: 'Promocion', color: '#E67E22' },
  social: { label: 'Social', color: '#9B59B6' },
  educacion: { label: 'Educacion', color: '#1ABC9C' },
  otro: { label: 'Otro', color: '#95A5A6' },
};

const PAGE_WIDTH = 595.28; // A4
const PAGE_HEIGHT = 841.89;
const MARGIN_LEFT = 45;
const MARGIN_RIGHT = 45;
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT;
const FOOTER_HEIGHT = 45;
const CONTENT_BOTTOM = PAGE_HEIGHT - FOOTER_HEIGHT - 15;

let pageCount = 0;

function formatDate(date: Date): string {
  return date.toLocaleDateString('es-PY', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

function formatTime(date: Date): string {
  return date.toLocaleTimeString('es-PY', {
    hour: '2-digit',
    minute: '2-digit',
  });
}

function sanitizeFilename(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `Informe_Correo_${year}-${month}-${day}.pdf`;
}

function drawFooter(doc: PDFKit.PDFDocument, pageNum: number): void {
  const footerY = PAGE_HEIGHT - FOOTER_HEIGHT;

  // Línea separadora
  doc.save();
  doc
    .strokeColor('#DDE0E8')
    .lineWidth(0.5)
    .moveTo(MARGIN_LEFT, footerY)
    .lineTo(PAGE_WIDTH - MARGIN_RIGHT, footerY)
    .stroke();

  doc
    .fontSize(7)
    .font('Helvetica')
    .fillColor(COLORS.textLight)
    .text(
      `Generado por Email Agent  -  ${new Date().toLocaleString('es-PY')}`,
      MARGIN_LEFT,
      footerY + 10,
      { width: CONTENT_WIDTH / 2, align: 'left' },
    );

  doc
    .fontSize(7)
    .font('Helvetica')
    .fillColor(COLORS.textLight)
    .text(
      `Pagina ${pageNum}`,
      PAGE_WIDTH / 2,
      footerY + 10,
      { width: CONTENT_WIDTH / 2, align: 'right' },
    );

  doc.restore();
}

function drawHeader(doc: PDFKit.PDFDocument, today: Date): void {
  doc.save();
  doc.rect(0, 0, PAGE_WIDTH, 100).fill(COLORS.headerBg);

  doc
    .fontSize(26)
    .font('Helvetica-Bold')
    .fillColor(COLORS.white)
    .text('INFORME DIARIO DE CORREO', MARGIN_LEFT, 22, {
      width: CONTENT_WIDTH,
      align: 'center',
    });

  // Línea decorativa
  const lineY = 55;
  const lineWidth = 60;
  const centerX = PAGE_WIDTH / 2;
  doc
    .strokeColor('#AAC4E8')
    .lineWidth(1)
    .moveTo(centerX - lineWidth, lineY)
    .lineTo(centerX + lineWidth, lineY)
    .stroke();

  doc
    .fontSize(11)
    .font('Helvetica')
    .fillColor('#AAC4E8')
    .text(formatDate(today), MARGIN_LEFT, 62, {
      width: CONTENT_WIDTH,
      align: 'center',
    });

  doc.restore();
  doc.y = 115;
}

function drawSummaryBar(doc: PDFKit.PDFDocument, emails: EmailMessage[]): void {
  const barY = doc.y;

  // Contar categorías
  const categoryCounts = new Map<EmailCategory, number>();
  for (const email of emails) {
    categoryCounts.set(email.categoria, (categoryCounts.get(email.categoria) || 0) + 1);
  }

  const barHeight = 40;

  // Fondo
  doc.save();
  doc.roundedRect(MARGIN_LEFT, barY, CONTENT_WIDTH, barHeight, 6).fill('#EEF0F5');

  // Total de correos
  doc
    .fontSize(13)
    .font('Helvetica-Bold')
    .fillColor(COLORS.primary)
    .text(`${emails.length}`, MARGIN_LEFT + 15, barY + 12, { continued: true })
    .font('Helvetica')
    .fontSize(11)
    .fillColor(COLORS.textMedium)
    .text(` correo${emails.length !== 1 ? 's' : ''} recibido${emails.length !== 1 ? 's' : ''}`);

  // Badges de categorías a la derecha
  let badgeX = PAGE_WIDTH - MARGIN_RIGHT - 12;
  const sortedCategories = [...categoryCounts.entries()].sort((a, b) => b[1] - a[1]);

  for (const [cat, count] of sortedCategories) {
    const cfg = CATEGORY_CONFIG[cat];
    const label = `${cfg.label} ${count}`;
    doc.font('Helvetica').fontSize(7);
    const textW = doc.widthOfString(label);
    const badgeW = textW + 10;
    badgeX -= badgeW + 5;

    doc.roundedRect(badgeX, barY + 12, badgeW, 16, 3).fill(cfg.color);
    doc
      .fontSize(7)
      .font('Helvetica-Bold')
      .fillColor(COLORS.white)
      .text(label, badgeX, barY + 16, { width: badgeW, align: 'center' });
  }

  doc.restore();
  doc.y = barY + barHeight + 15;
}

function drawCategoryBadge(doc: PDFKit.PDFDocument, category: EmailCategory, x: number, y: number): number {
  const cfg = CATEGORY_CONFIG[category];
  doc.font('Helvetica-Bold').fontSize(7);
  const textW = doc.widthOfString(cfg.label);
  const badgeW = textW + 10;
  const badgeH = 13;

  doc.save();
  doc.roundedRect(x, y, badgeW, badgeH, 3).fill(cfg.color);
  doc
    .fontSize(7)
    .font('Helvetica-Bold')
    .fillColor(COLORS.white)
    .text(cfg.label, x, y + 3, { width: badgeW, align: 'center' });
  doc.restore();

  return badgeW;
}

function drawEmailCard(doc: PDFKit.PDFDocument, email: EmailMessage, index: number): void {
  const cardPadding = 14;
  const cardX = MARGIN_LEFT;
  const innerWidth = CONTENT_WIDTH - cardPadding * 2;

  // Medir altura del contenido
  doc.font('Helvetica-Bold').fontSize(11);
  const subjectHeight = doc.heightOfString(`${index + 1}.  ${email.asunto}`, {
    width: innerWidth - 60, // dejar espacio para badge de categoría
  });

  doc.font('Helvetica').fontSize(9);
  const bodyHeight = doc.heightOfString(email.cuerpo, {
    width: innerWidth - 10,
  });

  const metaHeight = 28;
  const totalCardHeight = cardPadding + subjectHeight + 6 + metaHeight + 6 + bodyHeight + cardPadding + 4;

  // Si no cabe, saltar de página
  if (doc.y + totalCardHeight > CONTENT_BOTTOM) {
    drawFooter(doc, pageCount);
    doc.addPage();
    pageCount++;
    doc.y = 45;
  }

  const cardY = doc.y;

  // Fondo de la tarjeta
  doc.save();
  doc.roundedRect(cardX, cardY, CONTENT_WIDTH, totalCardHeight, 6).fill(COLORS.cardBg);

  // Borde izquierdo con color de categoría
  const catColor = CATEGORY_CONFIG[email.categoria].color;
  doc.rect(cardX, cardY + 3, 4, totalCardHeight - 6).fill(catColor);

  doc.restore();

  // --- Contenido ---
  let currentY = cardY + cardPadding;

  // Número + Asunto
  doc
    .fontSize(11)
    .font('Helvetica-Bold')
    .fillColor(COLORS.textDark)
    .text(`${index + 1}.  ${email.asunto}`, cardX + cardPadding + 6, currentY, {
      width: innerWidth - 60,
    });

  // Badge de categoría (alineado a la derecha del asunto)
  drawCategoryBadge(
    doc,
    email.categoria,
    cardX + CONTENT_WIDTH - cardPadding - 55,
    currentY + 1,
  );

  currentY = doc.y + 6;

  // Remitente
  doc
    .fontSize(9)
    .font('Helvetica-Bold')
    .fillColor(COLORS.textMedium)
    .text('De: ', cardX + cardPadding + 6, currentY, { continued: true })
    .font('Helvetica')
    .text(`${email.remitente}  `, { continued: true })
    .fontSize(8)
    .fillColor(COLORS.textLight)
    .text(`<${email.emailRemitente}>`);

  currentY = doc.y + 2;

  // Hora + badge de adjuntos
  doc
    .fontSize(9)
    .font('Helvetica')
    .fillColor(COLORS.textLight)
    .text(formatTime(email.fecha), cardX + cardPadding + 6, currentY, { continued: true });

  if (email.tieneAdjuntos) {
    doc
      .font('Helvetica-Bold')
      .fillColor(COLORS.attachBadge)
      .text('   Adjuntos', { continued: false });
  } else {
    doc.text('', { continued: false });
  }

  currentY = doc.y + 6;

  // Separador interno
  doc.save();
  doc
    .strokeColor('#DDE0E8')
    .lineWidth(0.5)
    .moveTo(cardX + cardPadding + 6, currentY)
    .lineTo(cardX + CONTENT_WIDTH - cardPadding, currentY)
    .stroke();
  doc.restore();

  currentY += 6;

  // Cuerpo del correo
  doc
    .fontSize(9)
    .font('Helvetica')
    .fillColor(COLORS.textMedium)
    .text(email.cuerpo, cardX + cardPadding + 10, currentY, {
      width: innerWidth - 10,
      lineGap: 2,
    });

  doc.y = cardY + totalCardHeight + 10;
}

export function generatePDF(emails: EmailMessage[]): string {
  const today = new Date();
  const filename = sanitizeFilename(today);
  const outputPath = path.join(config.outputDir, filename);

  if (!fs.existsSync(config.outputDir)) {
    fs.mkdirSync(config.outputDir, { recursive: true });
  }

  pageCount = 1;

  const doc = new PDFDocument({
    size: 'A4',
    margins: { top: 0, bottom: FOOTER_HEIGHT, left: MARGIN_LEFT, right: MARGIN_RIGHT },
    info: {
      Title: `Informe de Correo - ${formatDate(today)}`,
      Author: 'Email Agent',
      Subject: 'Resumen diario de correos electronicos',
    },
  });

  const stream = fs.createWriteStream(outputPath);
  doc.pipe(stream);

  // Encabezado
  drawHeader(doc, today);

  // Barra de resumen con categorías
  if (emails.length === 0) {
    drawSummaryBar(doc, []);
    doc
      .fontSize(13)
      .font('Helvetica')
      .fillColor(COLORS.textLight)
      .text('No se recibieron correos el dia de hoy.', MARGIN_LEFT, doc.y + 20, {
        width: CONTENT_WIDTH,
        align: 'center',
      });
  } else {
    drawSummaryBar(doc, emails);

    emails.forEach((email, index) => {
      drawEmailCard(doc, email, index);
    });
  }

  // Footer de la última página
  drawFooter(doc, pageCount);

  doc.end();

  return outputPath;
}
