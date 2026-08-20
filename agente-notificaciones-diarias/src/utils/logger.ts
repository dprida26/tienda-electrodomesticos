type LogLevel = 'info' | 'warn' | 'error' | 'debug';

const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

export class Logger {
  private prefix: string;

  constructor(prefix: string) {
    this.prefix = prefix;
  }

  private log(level: LogLevel, message: string, data?: unknown): void {
    const timestamp = new Date().toISOString();
    const levelMap = {
      info: `${colors.blue}ℹ${colors.reset}`,
      warn: `${colors.yellow}⚠${colors.reset}`,
      error: `${colors.red}✗${colors.reset}`,
      debug: `${colors.cyan}🐛${colors.reset}`,
    };

    const logLine = `${timestamp} ${levelMap[level]} [${this.prefix}] ${message}`;
    console.log(logLine);

    if (data) {
      console.log(JSON.stringify(data, null, 2));
    }
  }

  info(message: string, data?: unknown): void {
    this.log('info', message, data);
  }

  warn(message: string, data?: unknown): void {
    this.log('warn', message, data);
  }

  error(message: string, error?: Error | unknown): void {
    if (error instanceof Error) {
      this.log('error', message, {
        message: error.message,
        stack: error.stack,
      });
    } else {
      this.log('error', message, error);
    }
  }

  debug(message: string, data?: unknown): void {
    if (process.env.DEBUG === 'true') {
      this.log('debug', message, data);
    }
  }
}

export const createLogger = (prefix: string) => new Logger(prefix);
