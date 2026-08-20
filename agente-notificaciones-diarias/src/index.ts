import { DailyTaskScheduler } from './scheduler/daily-task.js';
import { Agent } from './agent/index.js';
import { NotificationsServer } from './api/server.js';
import { createLogger } from './utils/logger.js';

const logger = createLogger('Main');

async function main() {
  logger.info('🚀 Iniciando Agente de Notificaciones Diarias');

  const agent = new Agent();
  const scheduler = new DailyTaskScheduler();
  const server = new NotificationsServer(agent);

  try {
    // Inicializar agent (autenticación)
    await agent.initialize();

    // Iniciar servidor API
    server.start();

    // Iniciar planificador
    scheduler.start();

    // Mantener el proceso activo
    process.on('SIGINT', () => {
      logger.info('\n⏹️ Deteniendo agente...');
      scheduler.stop();
      process.exit(0);
    });

    // Para desarrollo: generar reporte inmediatamente
    if (process.env.DEV_MODE === 'true') {
      logger.info('\n🧪 Modo desarrollo: generando reporte de prueba...');
      await agent.generateDailyReport();
    }
  } catch (error) {
    logger.error('❌ Error al iniciar el agente:', error);
    process.exit(1);
  }
}

main();
