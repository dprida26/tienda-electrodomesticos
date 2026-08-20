"""
Scheduler
=========
Módulo para programar la ejecución automática del reporte
a las horas configuradas.
"""

import time
import logging
import schedule

logger = logging.getLogger(__name__)


def setup_schedule(job_func, morning_time: str, afternoon_time: str):
    """
    Configura el scheduler para ejecutar la función en los horarios indicados.

    Args:
        job_func: Función a ejecutar (sin argumentos)
        morning_time: Hora matutina en formato "HH:MM"
        afternoon_time: Hora vespertina en formato "HH:MM"
    """
    schedule.every().day.at(morning_time).do(job_func)
    schedule.every().day.at(afternoon_time).do(job_func)

    logger.info(f"⏰ Tareas programadas:")
    logger.info(f"   📅 Reporte matutino: {morning_time}")
    logger.info(f"   📅 Reporte vespertino: {afternoon_time}")


def run_scheduler():
    """
    Ejecuta el loop principal del scheduler.
    Se queda corriendo indefinidamente, ejecutando las tareas programadas.
    """
    logger.info("🚀 Scheduler iniciado. Esperando próxima ejecución...")
    logger.info(f"   Próxima ejecución: {schedule.next_run()}")

    while True:
        schedule.run_pending()
        # Esperar 30 segundos entre verificaciones
        time.sleep(30)
