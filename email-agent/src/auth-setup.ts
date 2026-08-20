import { google } from 'googleapis';
import http from 'http';
import url from 'url';
import dotenv from 'dotenv';
import path from 'path';

dotenv.config({ path: path.resolve(__dirname, '..', '.env') });

const CLIENT_ID = process.env.GOOGLE_CLIENT_ID;
const CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET;

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error('Error: Debes configurar GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET en el archivo .env');
  process.exit(1);
}

const REDIRECT_URI = 'http://localhost:3456/callback';
const SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'];

async function authenticate(): Promise<void> {
  console.log('=== Autenticación con Google Gmail ===\n');

  const oauth2Client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);

  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
    prompt: 'consent',
  });

  console.log('1. Se abrirá una ventana en tu navegador (o copiá el link).');
  console.log('2. Iniciá sesión con tu cuenta de Gmail.');
  console.log('3. Autorizá el acceso de lectura a tu correo.\n');
  console.log(`Abrí este enlace en tu navegador:\n\n${authUrl}\n`);
  console.log('Esperando autorización...\n');

  // Servidor temporal para capturar el código de autorización
  const code = await new Promise<string>((resolve, reject) => {
    const server = http.createServer(async (req, res) => {
      const parsedUrl = url.parse(req.url || '', true);

      if (parsedUrl.pathname === '/callback') {
        const authCode = parsedUrl.query.code as string;
        const error = parsedUrl.query.error as string;

        if (error) {
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          res.end('<h1>Autorización denegada</h1><p>Podés cerrar esta ventana.</p>');
          server.close();
          reject(new Error(`Autorización denegada: ${error}`));
          return;
        }

        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end('<h1>Autorización exitosa</h1><p>Podés cerrar esta ventana y volver a la terminal.</p>');
        server.close();
        resolve(authCode);
      }
    });

    server.listen(3456, () => {
      // Intentar abrir el navegador automáticamente
      const { exec } = require('child_process');
      exec(`start "" "${authUrl}"`);
    });
  });

  // Intercambiar código por tokens
  const { tokens } = await oauth2Client.getToken(code);

  console.log('Autenticación exitosa!\n');
  console.log('='.repeat(60));
  console.log('IMPORTANTE: Copiá el siguiente valor y pegálo en tu .env');
  console.log('='.repeat(60));
  console.log(`\nGOOGLE_REFRESH_TOKEN=${tokens.refresh_token}\n`);
  console.log('='.repeat(60));

  // Verificar acceso al buzón
  oauth2Client.setCredentials(tokens);
  const gmail = google.gmail({ version: 'v1', auth: oauth2Client });

  const profile = await gmail.users.getProfile({ userId: 'me' });
  console.log(`\nBuzón verificado: ${profile.data.emailAddress}`);
  console.log(`Total de mensajes: ${profile.data.messagesTotal}`);
  console.log('\nConfiguración completada. Ya podés ejecutar: npm run dev');
}

authenticate().catch((error) => {
  console.error('Error:', error instanceof Error ? error.message : error);
  process.exit(1);
});
