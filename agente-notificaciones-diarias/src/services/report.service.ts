import PDFDocument from 'pdfkit';
import fs from 'fs';
import path from 'path';
import { DailyReport, ReportSection } from '../types/index.js';
import config from '../config/env.js';

export class ReportService {
  private outputDir: string;

  constructor() {
    this.outputDir = config.REPORT_OUTPUT_DIR;
    this.ensureOutputDir();
  }

  private ensureOutputDir(): void {
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
  }

  generatePDF(report: DailyReport): string {
    const filename = `reporte-diario-${this.getFormattedDate(report.generatedAt)}.pdf`;
    const filepath = path.join(this.outputDir, filename);

    const doc = new PDFDocument({
      margin: 40,
      size: 'A4',
    });

    doc.pipe(fs.createWriteStream(filepath));

    // Encabezado
    doc.fontSize(24).font('Helvetica-Bold').text('REPORTE DIARIO DE NOTIFICACIONES', {
      align: 'center',
    });

    doc
      .fontSize(12)
      .font('Helvetica')
      .text(
        `Generado: ${this.formatDate(report.generatedAt)}`,
        { align: 'center' }
      );

    doc
      .fontSize(10)
      .text(
        `Período: ${this.formatDate(report.period.startDate)} - ${this.formatDate(report.period.endDate)}`,
        { align: 'center' }
      );

    doc.moveDown(2);

    // Tabla de contenidos
    doc
      .fontSize(14)
      .font('Helvetica-Bold')
      .text('TABLA DE CONTENIDOS', { underline: true });
    doc.moveDown(0.5);

    doc
      .fontSize(11)
      .font('Helvetica')
      .text(`1. Correos (${report.sections.emails.count} nuevos)`)
      .text(`2. LinkedIn (${report.sections.linkedin.count} notificaciones)`);

    doc.moveDown(2);

    // Sección de Correos
    this.addSection(doc, report.sections.emails, 'Correos');
    doc.addPage();

    // Sección de LinkedIn
    this.addSection(doc, report.sections.linkedin, 'LinkedIn');

    doc.end();

    return filepath;
  }

  private addSection(
    doc: PDFKit.PDFDocument,
    section: ReportSection,
    title: string
  ): void {
    doc
      .fontSize(16)
      .font('Helvetica-Bold')
      .text(`${title}`, { underline: true });

    doc
      .fontSize(11)
      .font('Helvetica')
      .text(`Total: ${section.count} elemento(s)`, { color: '#666666' });

    doc.moveDown(1);

    section.items.forEach((item, index) => {
      doc
        .fontSize(11)
        .font('Helvetica-Bold')
        .text(`${index + 1}. ${item.title}`, { color: '#0066CC' });

      doc
        .fontSize(10)
        .font('Helvetica')
        .text(`De: ${item.source}`)
        .text(`Fecha: ${this.formatDate(item.timestamp)}`);

      doc
        .fontSize(10)
        .font('Helvetica')
        .text(`Resumen: ${item.summary}`, { align: 'left', width: 500 });

      if (item.url) {
        doc.fontSize(9).text(`URL: ${item.url}`, { color: '#0066CC' });
      }

      doc.moveDown(1);

      // Línea separadora
      doc
        .moveTo(40, doc.y)
        .lineTo(555, doc.y)
        .stroke('#CCCCCC');

      doc.moveDown(1);

      // Verificar si necesitamos una nueva página
      if (doc.y > 700) {
        doc.addPage();
      }
    });
  }

  private formatDate(date: Date): string {
    return new Intl.DateTimeFormat('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  }

  private getFormattedDate(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  getReportPath(date: Date): string {
    const filename = `reporte-diario-${this.getFormattedDate(date)}.pdf`;
    return path.join(this.outputDir, filename);
  }
}
