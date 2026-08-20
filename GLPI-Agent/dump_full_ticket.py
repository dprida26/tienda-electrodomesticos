#!/usr/bin/env python3
"""
Script para obtener la estructura completa de un ticket
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

    # Obtener un ticket específico por su ID
    logger.info("📡 Obteniendo ticket específico...")
    resp = sess.get(f"{cfg['glpi_url']}/Ticket/8426", timeout=30)

    if resp.status_code == 200:
        ticket = resp.json()
        logger.info(f"✅ Ticket obtenido: {ticket.get('id')}\n")

        print("="*100)
        print("ESTRUCTURA COMPLETA DEL TICKET (ID: 8426)")
        print("="*100 + "\n")

        for key in sorted(ticket.keys()):
            value = ticket[key]
            if isinstance(value, str) and len(value) > 100:
                value = value[:97] + "..."
            print(f"  {str(key):30} → {value}")

    else:
        logger.error(f"Error: {resp.status_code}")
        print(resp.text[:500])

    sess.get(f"{cfg['glpi_url']}/killSession", timeout=10)

if __name__ == "__main__":
    main()
