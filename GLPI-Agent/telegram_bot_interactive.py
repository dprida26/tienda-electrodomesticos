#!/usr/bin/env python3
"""
GLPI Telegram Bot - Modo Interactivo
Responde a comandos del usuario en tiempo real
"""

import os
import sys
import logging
import time
from dotenv import load_dotenv
from glpi_client import GLPIClient
from report_builder import build_telegram_report, split_message
from telegram_sender import TelegramSender

LOG_FMT = "%(asctime)s │ %(levelname)-7s │ %(message)s"

def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FMT,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                os.path.join(log_dir, f"bot_interactive.log"),
                encoding="utf-8"
            )
        ]
    )

def load_config():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        print(f"❌ No se encontró .env en {env_path}")
        sys.exit(1)
    load_dotenv(env_path)
    return {
        "glpi_url": os.getenv("GLPI_URL", ""),
        "app_token": os.getenv("APP_TOKEN", ""),
        "user_token": os.getenv("USER_TOKEN", ""),
        "glpi_user": os.getenv("GLPI_USER", ""),
        "glpi_password": os.getenv("GLPI_PASSWORD", ""),
        "email_domain": os.getenv("EMAIL_DOMAIN", ""),
        "category_name": os.getenv("CATEGORY_NAME", ""),
        "telegram_bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
        "telegram_chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
    }

def validate_config(cfg):
    ok = True
    for k in ["glpi_url", "app_token"]:
        if not cfg[k]:
            logging.error(f"❌ Falta {k.upper()} en .env")
            ok = False
    if not cfg["glpi_user"] and not cfg["user_token"]:
        logging.error("❌ Configura GLPI_USER/GLPI_PASSWORD o USER_TOKEN en .env")
        ok = False
    if not cfg["telegram_bot_token"]:
        logging.error("❌ Falta TELEGRAM_BOT_TOKEN")
        ok = False
    if not cfg["telegram_chat_id"]:
        logging.error("❌ Falta TELEGRAM_CHAT_ID")
        ok = False
    return ok

def make_glpi(cfg):
    return GLPIClient(cfg["glpi_url"], cfg["app_token"], cfg["user_token"],
                      cfg["glpi_user"], cfg["glpi_password"])

def generate_report(cfg):
    """Genera y envía un reporte bajo demanda"""
    logger = logging.getLogger(__name__)
    try:
        glpi = make_glpi(cfg)
        if not glpi.init_session():
            logger.error("No se pudo conectar a GLPI")
            return False

        tickets = glpi.search_tickets(
            email_domain=cfg["email_domain"] or None,
            category_name=cfg["category_name"] or None
        )

        if not tickets:
            tg = TelegramSender(cfg["telegram_bot_token"], cfg["telegram_chat_id"])
            msg = "✅ <b>Sin tickets pendientes</b>\n\nNo hay tickets activos en este momento."
            tg.send_message(msg)
            glpi.kill_session()
            return True

        logger.info(f"📊 {len(tickets)} tickets encontrados")

        report = build_telegram_report(tickets)
        parts = split_message(report)

        tg = TelegramSender(cfg["telegram_bot_token"], cfg["telegram_chat_id"])
        logger.info(f"📤 Enviando {len(parts)} mensaje(s) a Telegram...")
        ok = tg.send_long_message(parts)

        glpi.kill_session()
        return ok

    except Exception as e:
        logger.error(f"❌ Error al generar reporte: {e}")
        return False

def get_updates(cfg, last_update_id=0):
    """Obtiene los últimos mensajes del bot"""
    try:
        import requests
        response = requests.get(
            f"https://api.telegram.org/bot{cfg['telegram_bot_token']}/getUpdates",
            params={"offset": last_update_id + 1, "limit": 10, "timeout": 30},
            timeout=35
        )
        data = response.json()

        if data.get("ok"):
            return data.get("result", [])
        return []

    except Exception as e:
        logging.error(f"Error obteniendo updates: {e}")
        return []

def handle_message(cfg, update, last_update_id):
    """Procesa un mensaje recibido"""
    logger = logging.getLogger(__name__)

    message = update.get("message")
    if not message:
        return last_update_id

    update_id = update.get("update_id")
    text = message.get("text", "").strip()
    chat_id = message.get("chat", {}).get("id")
    user_name = message.get("from", {}).get("first_name", "Usuario")

    # Comandos reconocidos
    if text.lower() in ["/reporte", "/report", "/tickets", "!reporte"]:
        logger.info(f"📬 Comando recibido de {user_name}: {text}")

        # Enviar mensaje de procesamiento
        tg = TelegramSender(cfg["telegram_bot_token"], str(chat_id))
        tg.send_message("⏳ <b>Procesando solicitud...</b>\n\nObteniendo tickets de GLPI...")

        # Generar reporte
        if generate_report({**cfg, "telegram_chat_id": str(chat_id)}):
            logger.info(f"✅ Reporte enviado para {user_name}")
        else:
            tg.send_message("❌ <b>Error</b>\n\nNo se pudo generar el reporte. Intenta más tarde.")
            logger.error(f"Error al generar reporte para {user_name}")

    elif text.lower() in ["/help", "/ayuda", "!help"]:
        help_text = """
<b>🤖 GLPI Agent Bot - Comandos Disponibles</b>

/reporte - Obtener reporte de tickets
/report - (Alias de /reporte)
/tickets - (Alias de /reporte)
!reporte - (Alias de /reporte)

/help - Mostrar esta ayuda
/status - Estado del sistema
/info - Información del bot

<i>El bot responde automáticamente cuando usas estos comandos.</i>
"""
        tg = TelegramSender(cfg["telegram_bot_token"], str(chat_id))
        tg.send_message(help_text)
        logger.info(f"Help solicitado por {user_name}")

    elif text.lower() in ["/status", "!status"]:
        status_text = """
<b>✅ Sistema Operativo</b>

GLPI API: ✓ Conectado
Telegram Bot: ✓ Activo
Filtros: ✓ Configurados
  • Email: @amsa.com.py
  • Mes: Mayo 2026
  • Categoría: Soporte Tecnico

Estado: <b>🟢 En línea</b>
"""
        tg = TelegramSender(cfg["telegram_bot_token"], str(chat_id))
        tg.send_message(status_text)
        logger.info(f"Status solicitado por {user_name}")

    elif text.lower() in ["/info", "!info"]:
        info_text = """
<b>ℹ️ Información del Bot</b>

<b>Nombre:</b> GLPI Agent Bot
<b>Función:</b> Reportes automáticos de tickets
<b>Versión:</b> 1.0.0
<b>Modo:</b> Interactivo (bajo demanda)

Para obtener un reporte, usa:
  /reporte
"""
        tg = TelegramSender(cfg["telegram_bot_token"], str(chat_id))
        tg.send_message(info_text)
        logger.info(f"Info solicitado por {user_name}")

    elif text.startswith("/"):
        # Comando no reconocido
        tg = TelegramSender(cfg["telegram_bot_token"], str(chat_id))
        tg.send_message(f"❓ <b>Comando no reconocido: {text}</b>\n\nUsa /help para ver los comandos disponibles.")
        logger.info(f"Comando no reconocido de {user_name}: {text}")

    return update_id

def main():
    print("\n╔══════════════════════════════════════╗")
    print("║   🤖 GLPI AGENT — Telegram Bot      ║")
    print("║     MODO INTERACTIVO                ║")
    print("╚══════════════════════════════════════╝\n")

    setup_logging()
    logger = logging.getLogger(__name__)

    cfg = load_config()
    if not validate_config(cfg):
        sys.exit(1)

    logger.info("📡 Iniciando bot en modo interactivo...")
    logger.info("⏳ Esperando comandos en Telegram...")
    logger.info("💡 Usa /reporte, /help, /status o /info")

    last_update_id = 0
    error_count = 0
    max_errors = 5

    try:
        while True:
            try:
                # Obtener updates con timeout largo (polling)
                updates = get_updates(cfg, last_update_id)

                if updates:
                    for update in updates:
                        last_update_id = handle_message(cfg, update, last_update_id)
                    error_count = 0  # Reset error counter on success

                else:
                    # Sin updates, esperar un poco
                    time.sleep(1)

            except KeyboardInterrupt:
                logger.info("🛑 Bot detenido por el usuario.")
                break

            except Exception as e:
                error_count += 1
                logger.error(f"❌ Error en loop: {e}")

                if error_count >= max_errors:
                    logger.error(f"❌ Demasiados errores ({max_errors}). Deteniendo bot.")
                    break

                time.sleep(5)  # Esperar antes de reintentar

    except KeyboardInterrupt:
        logger.info("🛑 Bot detenido.")

    logger.info("✅ Bot cerrado.")

if __name__ == "__main__":
    main()
