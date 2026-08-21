import schedule from 'node-schedule';
import { Agent } from '../agent/index.js';
import config from '../config/env.js';

export class DailyTaskScheduler {
  private agent: Agent;
  private job: schedule.Job | null = null;

  constructor() {
    this.agent = new Agent();
  }

  start(): void {
    const time = config.SCHEDULE_TIME; // Formato: "HH:MM"

    console.log(`⏰ Programando tarea diaria a las ${time}`);

    this.job = schedule.scheduleJob(time, async () => {
      console.log(`🚀 Ejecutando tarea diaria a las ${new Date().toLocaleTimeString()}`);
      await this.runDailyTask();
    });

    console.log('✅ Planificador iniciado');
  }

  stop(): void {
    if (this.job) {
      this.job.cancel();
      console.log('⏹️ Planificador detenido');
    }
  }

  private async runDailyTask(): Promise<void> {
    try {
      console.log('📨 Iniciando generación de reporte diario...');
      const reportPath = await this.agent.generateDailyReport();
      console.log(`✅ Reporte generado: ${reportPath}`);
    } catch (error) {
      console.error('❌ Error en la tarea diaria:', error);
    }
  }

  // Ejecutar manualmente (para pruebas)
  async executeNow(): Promise<void> {
    console.log('🔄 Ejecutando tarea manualmente...');
    await this.runDailyTask();
  }
}
