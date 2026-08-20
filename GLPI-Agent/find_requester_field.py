#!/usr/bin/env python3
"""
Script para encontrar qué campo contiene el email del solicitante
"""

import os
import sys
import logging
import requests
import base64
from dotenv import load_dotenv

LOG_FMT = "%(asctime)s │ %(levelname)-7s │ %(message)s"

def setup_logging():
    logging.basicConfig(level=logging.INFO, format=LOG_FMT, datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)])

def load_config():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
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

    requests.packages.urllib3.disable_warnings()
    sess = requests.Session()
    sess.verify = False
    sess.headers.update({"App-Token": cfg["app_token"], "Content-Type": "application/json"})

    credentials = base64.b64encode(f"{cfg['glpi_user']}:{cfg['glpi_password']}".encode()).decode()
    sess.headers["Authorization"] = f"Basic {credentials}"

    resp = sess.get(f"{cfg['glpi_url']}/initSession", timeout=30)
    data = resp.json()
    session_token = data.get("session_token")
    sess.headers["Session-Token"] = session_token
    del sess.headers["Authorization"]

    logger.info("✅ Sesión iniciada")

    # Obtener un ticket y sus usuarios asociados
    logger.info("📡 Obteniendo ticket 8431 (tiene solicitante maria.brizuela@amsa.com.py)...")

    resp = sess.get(f"{cfg['glpi_url']}/Ticket/8431", timeout=30)
    ticket = resp.json()

    logger.info(f"✅ Ticket obtenido\n")
    print("="*100)
    print("CAMPOS DEL TICKET 8431:")
    print("="*100 + "\n")

    for key in sorted(ticket.keys()):
        value = ticket[key]
        if isinstance(value, str) and len(value) > 80:
            value = value[:77] + "..."
        if key not in ['links', 'content']:
            print(f"  {str(key):30} → {value}")

    # Obtener los usuarios del ticket
    logger.info("📡 Obteniendo usuarios del ticket...")
    resp = sess.get(f"{cfg['glpi_url']}/Ticket/8431/Ticket_User", timeout=30)
    users = resp.json()

    print("\n" + "="*100)
    print("USUARIOS ASOCIADOS AL TICKET:")
    print("="*100 + "\n")
    print(f"Total de usuarios: {len(users)}\n")

    for user in users:
        print(f"  Usuario ID: {user.get('users_id')}")
        print(f"  Tipo: {user.get('type')}")
        print(f"  Data: {user}\n")

    sess.get(f"{cfg['glpi_url']}/killSession", timeout=10)

if __name__ == "__main__":
    main()
