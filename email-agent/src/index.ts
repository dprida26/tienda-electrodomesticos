import { fetchTodayEmails } from './email';
import { generatePDF } from './pdf-generator';

async function main(): Promise<void> {
  console.log('=== Email Agent - Informe Diario ===');
  console.log(`Fecha: ${new Date().toLocaleDateString('es-PY')}\n`);

  try {
    console.log('Conectando con Microsoft 365...');
    const emails = await fetchTodayEmails();
    console.log(`Se encontraron ${emails.length} correo(s) del día.\n`);

    if (emails.length > 0) {
      console.log('Correos recibidos:');
      emails.forEach((email, i) => {
        console.log(`  ${i + 1}. [${email.fecha.toLocaleTimeString('es-PY', { hour: '2-digit', minute: '2-digit' })}] ${email.remitente} — ${email.asunto}`);
      });
      console.log('');
    }

    console.log('Generando informe PDF...');
    const outputPath = generatePDF(emails);
    console.log(`PDF generado exitosamente: ${outputPath}`);
  } catch (error) {
    if (error instanceof Error) {
      console.error(`Error: ${error.message}`);
    } else {
      console.error('Error desconocido:', error);
    }
    process.exit(1);
  }
}

main();
