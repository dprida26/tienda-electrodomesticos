#!/usr/bin/env python3
"""
Script para inspeccionar la estructura de un ticket de GLPI
y descubrir qué campo contiene el usuario que creó el ticket
"""

import os
import sys
import logging
from dotenv import load_dotenv
from glpi_client import GLPIClient

LOG_FMT = "%(asctime)s │ %(levelname)-7s │ %(message)s"

def setup_logging():
    logging.basicConfig(level=logging.INFO, format=LOG_FMT, datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)])

def load_config():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        print(f"❌ No se encontró .env en {env_path}"); sys.exit(1)
    load_dotenv(env_path)
    return {k: os.getenv(v, d) for k, v, d in [
        ("glpi_url", "GLPI_URL", ""), ("app_token", "APP_TOKEN", ""),
        ("user_token", "USER_TOKEN", ""), ("glpi_user", "GLPI_USER", ""),
        ("glpi_password", "GLPI_PASSWORD", ""),
    ]}

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    cfg = load_config()
    glpi = GLPIClient(cfg["glpi_url"], cfg["app_token"], cfg["user_token"],
                      cfg["glpi_user"], cfg["glpi_password"])

    if not glpi.init_session():
        logger.error("No se pudo conectar a GLPI")
        sys.exit(1)

    try:
        logger.info("📡 Obteniendo estructura de un ticket...")
        tickets = glpi.search_tickets(email_domain="@amsa.com.py")

        if not tickets:
            logger.error("❌ No se encontraron tickets")
            sys.exit(1)

        ticket = tickets[0]
        logger.info(f"✅ Primer ticket encontrado: #{ticket.get('id')}")
        logger.info("\n📋 ESTRUCTURA DEL TICKET:\n")

        for key in sorted(ticket.keys()):
            value = ticket[key]
            # Truncar valores muy largos
            if isinstance(value, str) and len(value) > 80:
                value = value[:77] + "..."
            print(f"  {key:20} → {value}")

        print("\n" + "="*70)
        print("🔍 CAMPOS DE INTERÉS:")
        print("="*70)
        print(f"  Requester (campo 4)      : {ticket.get('4', 'N/A')}")
        print(f"  Requester email (22)     : {ticket.get('22', 'N/A')}")
        print(f"  User (campo 60?)         : {ticket.get('60', 'N/A')}")
        print(f"  Technician (5)           : {ticket.get('5', 'N/A')}")
        print(f"  Date (creation)          : {ticket.get('date', 'N/A')}")

    finally:
        glpi.kill_session()

if __name__ == "__main__":
    main()
