#!/usr/bin/env python3
"""
Script para descubrir el Chat ID de Telegram
Sin requerimientos de entrada interactiva
"""

import os
import sys
import logging
from dotenv import load_dotenv
from telegram_sender import TelegramSender

LOG_FMT = "%(asctime)s │ %(levelname)-7s │ %(message)s"

def setup_logging():
    logging.basicConfig(level=logging.INFO, format=LOG_FMT, datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)])

def load_config():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        print(f"❌ No se encontró .env en {env_path}"); sys.exit(1)
    load_dotenv(env_path)
    return os.getenv("TELEGRAM_BOT_TOKEN", "")

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    token = load_config()
    if not token or token == "TU_TOKEN_AQUI":
        print("❌ Configura TELEGRAM_BOT_TOKEN primero."); sys.exit(1)

    print("\n" + "="*50)
    print("🔍 DESCUBRIMIENTO DE CHAT ID")
    print("="*50)
    print("\n⚠️  INSTRUCCIONES:")
    print("1. Agrega el bot al grupo de Telegram")
    print("2. Envía un mensaje en el grupo")
    print("3. Espera a que este script lea los updates...\n")

    tg = TelegramSender(token, "")
    if not tg.test_connection():
        sys.exit(1)

    logger.info("📡 Obteniendo chats...")
    chats = tg.get_chat_id_from_updates()

    if not chats:
        print("\n❌ No se encontraron chats.")
        print("   Asegúrate de:")
        print("   - Agregar el bot al grupo")
        print("   - Enviar un mensaje en el grupo")
        print("   - Ejecutar este script inmediatamente después")
        sys.exit(1)

    print(f"\n✅ {len(chats)} chat(s) encontrado(s):\n")
    for c in chats:
        print(f"  📌 {c['title']:<30} | Tipo: {c['type']:<10} | ID: {c['chat_id']}")

    print("\n" + "="*50)
    print("📋 PRÓXIMO PASO:")
    print("="*50)
    print("\nCopia el Chat ID y actualiza el .env:")
    print('  TELEGRAM_CHAT_ID=<ID_COPIADO>')
    print("\nOr run:")
    print("  python update_env.py <CHAT_ID>\n")

if __name__ == "__main__":
    main()
