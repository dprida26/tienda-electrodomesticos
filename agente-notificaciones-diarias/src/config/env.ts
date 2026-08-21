import dotenv from 'dotenv';
import { z } from 'zod';

dotenv.config();

const envSchema = z.object({
  GMAIL_CLIENT_ID: z.string(),
  GMAIL_CLIENT_SECRET: z.string(),
  GMAIL_REDIRECT_URI: z.string().url(),
  LINKEDIN_CLIENT_ID: z.string(),
  LINKEDIN_CLIENT_SECRET: z.string(),
  LINKEDIN_ACCESS_TOKEN: z.string(),
  SCHEDULE_TIME: z.string().default('08:00'),
  REPORT_OUTPUT_DIR: z.string().default('./reports'),
  GMAIL_USER_EMAIL: z.string().email(),
  NODE_ENV: z.enum(['development', 'production']).default('development'),
});

const config = envSchema.parse(process.env);

export default config;
