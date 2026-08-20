import path from 'path';
import dotenv from 'dotenv';

dotenv.config({ path: path.resolve(__dirname, '..', '.env') });

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Variable de entorno requerida: ${name}. Revisa tu archivo .env`);
  }
  return value;
}

export const config = {
  google: {
    clientId: requireEnv('GOOGLE_CLIENT_ID'),
    clientSecret: requireEnv('GOOGLE_CLIENT_SECRET'),
    refreshToken: requireEnv('GOOGLE_REFRESH_TOKEN'),
  },
  outputDir: process.env.OUTPUT_DIR || path.join('C:', 'Users', 'Administrador', 'Desktop', 'Informes de Correo'),
};
