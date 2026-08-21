#!/usr/bin/env python3
"""
GLPI Telegram Bot 24/7 - Bot interactivo que responde consultas en tiempo real
Usa polling para escuchar mensajes constantemente y responde con info de GLPI
"""

import os
import sys
import io
import logging
import signal
from dotenv import load_dotenv
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from glpi_client import GLPIClient
from report_builder import build_telegram_report, split_message

LOG_FMT = "%(asctime)s │ %(levelname)-7s │ %(message)s"

def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)

    console = logging.StreamHandler(io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8'))

    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FMT,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            console,
            logging.FileHandler(
                os.path.join(log_dir, f"bot_24_7.log"),
                encoding="utf-8"
            )
        ]
    )

def load_config():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"❌ No se encontró .env en {env_path}")

    load_dotenv(env_path)
    return {
        "glpi_url": os.getenv("GLPI_URL", ""),
        "app_token": os.getenv("APP_TOKEN", ""),
        "glpi_user": os.getenv("GLPI_USER", ""),
        "glpi_password": os.getenv("GLPI_PASSWORD", ""),
        "email_domain": os.getenv("EMAIL_DOMAIN", ""),
        "category_name": os.getenv("CATEGORY_NAME", ""),
        "telegram_bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
        "telegram_chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
    }

logger = logging.getLogger(__name__)
glpi = None
cfg = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start - Muestra menu de opciones"""
    logger.info(f"📥 Comando /start recibido de {update.effective_user.id} ({update.effective_user.first_name})")
    await update.message.reply_text(
        "🤖 <b>GLPI Bot - Ayuda</b>\n\n"
        "Comandos disponibles:\n"
        "🔍 <b>/tickets</b> - Ver tickets activos de @amsa.com.py\n"
        "📊 <b>/resumen</b> - Resumen detallado del mes\n"
        "❓ <b>/ayuda</b> - Mostrar esta ayuda\n\n"
        "O simplemente escribe cualquier cosa y buscaré tickets relacionados.",
        parse_mode="HTML"
    )

async def tickets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /tickets - Ver tickets activos"""
    logger.info(f"📥 Comando /tickets recibido de {update.effective_user.id}")
    try:
        await update.message.chat.send_action("typing")

        if not glpi.init_session():
            logger.error("❌ Error conectando a GLPI")
            await update.message.reply_text("❌ Error: No se pudo conectar a GLPI")
            return

        tickets_list = glpi.search_tickets(
            category_name=cfg.get("category_name"),
            email_domain=cfg.get("email_domain")
        )

        if not tickets_list:
            await update.message.reply_text("✅ No hay tickets pendientes en el momento.")
            return

        report = build_telegram_report(tickets_list)
        parts = split_message(report, max_length=4096)

        for part in parts:
            await update.message.reply_text(part, parse_mode="HTML")

        logger.info(f"✅ Enviados {len(tickets_list)} tickets al usuario")

    except Exception as e:
        logger.error(f"❌ Error en /tickets: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)[:100]}")

async def resumen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /resumen - Resumen detallado"""
    try:
        await update.message.chat.send_action("typing")

        if not glpi.init_session():
            await update.message.reply_text("❌ Error: No se pudo conectar a GLPI")
            return

        tickets_list = glpi.search_tickets(
            category_name=cfg.get("category_name"),
            email_domain=cfg.get("email_domain")
        )

        if not tickets_list:
            await update.message.reply_text("✅ No hay tickets pendientes en el momento.")
            return

        # Contar por prioridad
        by_priority = {}
        for t in tickets_list:
            priority = t.get("priority", "MEDIA")
            by_priority[priority] = by_priority.get(priority, 0) + 1

        summary = f"📊 <b>Resumen de Tickets ({datetime.now():%d/%m/%Y})</b>\n\n"
        summary += f"📌 Total: {len(tickets_list)} tickets\n"
        summary += f"🏢 Dominio: @amsa.com.py\n"
        summary += f"🗂️ Categoría: {cfg.get('category_name')}\n\n"
        summary += "<b>Por Prioridad:</b>\n"

        for priority in ["MUY ALTA", "ALTA", "MEDIA", "BAJA"]:
            count = by_priority.get(priority, 0)
            if count > 0:
                summary += f"  • {priority}: {count}\n"

        await update.message.reply_text(summary, parse_mode="HTML")

    except Exception as e:
        logger.error(f"❌ Error en /resumen: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)[:100]}")

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /ayuda"""
    await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Procesar mensajes de texto genéricos"""
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    user_name = update.effective_user.first_name or update.effective_user.username or "Usuario"
    chat_type = update.message.chat.type

    logger.info(f"📥 [{chat_type}] Mensaje de {user_name} ({update.effective_user.id}): '{text[:50]}...'")

    # Ignorar si es un comando (ya lo procesa CommandHandler)
    if text.startswith("/"):
        logger.info(f"⏭️  Es un comando, ignorando (CommandHandler)")
        return

    # En grupos, solo responder si el bot es mencionado o es respuesta
    if chat_type == "group" or chat_type == "supergroup":
        is_reply_to_bot = (update.message.reply_to_message and
                          update.message.reply_to_message.from_user.is_bot)
        is_bot_mentioned = "@glpi_soporte_amsa_bot" in text or "@glpi_soporte_amsa" in text

        if not is_reply_to_bot and not is_bot_mentioned:
            logger.info(f"⏭️  Grupo: mensaje ignorado (bot no mencionado ni es respuesta)")
            return

    logger.info(f"✅ Procesando mensaje...")

    # Palabras clave para tickets
    if any(word in text for word in ["ticket", "tickets", "soporte", "glpi", "problema", "error", "active", "pending"]):
        logger.info(f"🔍 Detectada palabra clave: tickets")
        await tickets(update, context)
    # Palabras clave para ayuda
    elif any(word in text for word in ["ayuda", "help", "como", "que", "info", "commands", "comandos"]):
        logger.info(f"❓ Detectada palabra clave: ayuda")
        await start(update, context)
    else:
        logger.info(f"💬 Mensaje genérico, enviando opción de ayuda")
        await update.message.reply_text(
            "👋 Hola! Soy el bot de GLPI.\n\n"
            "Escribe /ayuda para ver los comandos disponibles, o pregúntame por:\n"
            "• tickets\n"
            "• soporte\n"
            "• problemas\n\n"
            "Ejemplos: 'muéstrame los tickets', 'hay algún error', etc."
        )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejo de errores global"""
    logger.error(f"❌ Error en bot: {context.error}", exc_info=True)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("❌ Ocurrió un error. Intenta de nuevo más tarde.")

def main():
    global glpi, cfg

    setup_logging()

    try:
        logger.info("=" * 50)
        logger.info("🤖 GLPI Bot 24/7 - Iniciando...")
        logger.info("=" * 50)

        cfg = load_config()

        # Validar configuración
        if not cfg.get("telegram_bot_token"):
            raise ValueError("❌ TELEGRAM_BOT_TOKEN no configurado en .env")

        # Inicializar cliente GLPI
        glpi = GLPIClient(
            base_url=cfg.get("glpi_url"),
            app_token=cfg.get("app_token"),
            username=cfg.get("glpi_user"),
            password=cfg.get("glpi_password")
        )

        logger.info("✅ Configuración cargada correctamente")
        logger.info(f"🔗 Bot token: {cfg.get('telegram_bot_token')[:10]}...")
        logger.info(f"💬 Chat ID: {cfg.get('telegram_chat_id')}")

        # Crear aplicación de Telegram
        app = Application.builder().token(cfg.get("telegram_bot_token")).build()

        # Registrar handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("tickets", tickets))
        app.add_handler(CommandHandler("resumen", resumen))
        app.add_handler(CommandHandler("ayuda", ayuda))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Error handler
        app.add_error_handler(error_handler)

        # Iniciar bot
        logger.info("🚀 Bot iniciado en modo polling (24/7)...")
        logger.info("💬 Escuchando mensajes en Telegram...")

        app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            poll_interval=1.0,
            timeout=30,
            drop_pending_updates=True
        )

    except KeyboardInterrupt:
        logger.info("⛔ Bot detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
