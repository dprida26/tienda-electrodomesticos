#!/usr/bin/env python3
"""
Script de prueba para el bot interactivo
Valida conexión GLPI y carga de configuración
"""

import os
import sys
import io
import logging
from dotenv import load_dotenv
from glpi_client import GLPIClient

LOG_FMT = "%(asctime)s │ %(levelname)-7s │ %(message)s"

def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    console = logging.StreamHandler(io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8'))
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FMT,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[console, logging.FileHandler(os.path.join(log_dir, f"test_bot.log"), encoding="utf-8")]
    )

logger = logging.getLogger(__name__)

def main():
    setup_logging()

    logger.info("=" * 50)
    logger.info("🤖 Test Bot Interactivo")
    logger.info("=" * 50)

    # Cargar .env
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        logger.error(f"❌ No se encontró .env en {env_path}")
        sys.exit(1)

    load_dotenv(env_path)

    cfg = {
        "glpi_url": os.getenv("GLPI_URL", ""),
        "app_token": os.getenv("APP_TOKEN", ""),
        "glpi_user": os.getenv("GLPI_USER", ""),
        "glpi_password": os.getenv("GLPI_PASSWORD", ""),
        "email_domain": os.getenv("EMAIL_DOMAIN", ""),
        "category_name": os.getenv("CATEGORY_NAME", ""),
        "telegram_bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
        "telegram_chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
    }

    # 1. Validar configuración
    logger.info("\n✓ Validando configuración...")
    required = ["glpi_url", "glpi_user", "glpi_password", "telegram_bot_token", "telegram_chat_id"]
    missing = [k for k in required if not cfg.get(k)]

    if missing:
        logger.error(f"❌ Configuración incompleta: {', '.join(missing)}")
        sys.exit(1)

    logger.info("✅ Configuración válida")
    logger.info(f"  • GLPI URL: {cfg['glpi_url'][:40]}...")
    logger.info(f"  • Usuario GLPI: {cfg['glpi_user']}")
    logger.info(f"  • Bot Token: {cfg['telegram_bot_token'][:20]}...")
    logger.info(f"  • Chat ID: {cfg['telegram_chat_id']}")

    # 2. Probar conexión GLPI
    logger.info("\n✓ Probando conexión a GLPI...")
    glpi = GLPIClient(
        base_url=cfg.get("glpi_url"),
        app_token=cfg.get("app_token"),
        username=cfg.get("glpi_user"),
        password=cfg.get("glpi_password")
    )

    if not glpi.init_session():
        logger.error("❌ No se pudo conectar a GLPI")
        sys.exit(1)

    logger.info("✅ Conexión GLPI exitosa")

    # 3. Probar búsqueda de tickets
    logger.info("\n✓ Probando búsqueda de tickets...")
    tickets = glpi.search_tickets(
        category_name=cfg.get("category_name"),
        email_domain=cfg.get("email_domain")
    )

    logger.info(f"✅ Se encontraron {len(tickets)} tickets")

    # 4. Probar bot de Telegram
    logger.info("\n✓ Probando bot de Telegram...")
    try:
        import requests
        url = f"https://api.telegram.org/bot{cfg['telegram_bot_token']}/getMe"
        resp = requests.get(url, timeout=5)

        if resp.status_code == 200:
            bot_info = resp.json()
            if bot_info.get("ok"):
                logger.info(f"✅ Bot de Telegram válido")
                logger.info(f"  • Nombre: {bot_info['result']['first_name']}")
                logger.info(f"  • Usuario: @{bot_info['result']['username']}")
            else:
                logger.error(f"❌ Token de Telegram inválido: {bot_info.get('description')}")
                sys.exit(1)
        else:
            logger.error(f"❌ Error en API de Telegram: {resp.status_code}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error probando Telegram: {e}")
        sys.exit(1)

    # 5. Resumen
    logger.info("\n" + "=" * 50)
    logger.info("✅ ¡TODO LOS TESTS PASARON!")
    logger.info("=" * 50)
    logger.info("\nEl bot está listo para iniciar.")
    logger.info("\nPara ejecutar el bot 24/7:")
    logger.info("  1. PowerShell como Admin")
    logger.info("  2. cd 'C:\\Users\\Administrador\\Desktop\\AMSA\\Personal\\Proyectos IA\\GLPI-Agent'")
    logger.info("  3. powershell -ExecutionPolicy Bypass -File run_bot_with_restart.ps1")
    logger.info("\nO instalar como servicio:")
    logger.info("  powershell -ExecutionPolicy Bypass -File install_bot_service.ps1")
    logger.info("")

if __name__ == "__main__":
    main()
