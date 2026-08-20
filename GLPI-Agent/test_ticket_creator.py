#!/usr/bin/env python3
"""
Script para debuggear qué campo contiene el usuario creador del ticket
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

    # Buscar tickets con todos los campos posibles
    logger.info("📡 Obteniendo tickets de @amsa.com.py...")
    resp = sess.get(f"{cfg['glpi_url']}/search/Ticket", params={
        "criteria[0][field]": 12,
        "criteria[0][searchtype]": "equals",
        "criteria[0][value]": 1,  # Nuevo
        "criteria[1][link]": "OR",
        "criteria[1][field]": 12,
        "criteria[1][searchtype]": "equals",
        "criteria[1][value]": 2,  # En curso
        "criteria[2][link]": "AND",
        "criteria[2][field]": 22,
        "criteria[2][searchtype]": "contains",
        "criteria[2][value]": "@amsa.com.py",
        "range": "0-5",
        "expand_dropdowns": "true"
    }, timeout=60)

    result = resp.json()
    data = result.get("data", [])

    print("\n" + "="*80)
    print(f"ENCONTRADOS: {len(data)} tickets")
    print("="*80 + "\n")

    for i, ticket in enumerate(data[:3]):
        print(f"--- TICKET {i+1} (ID: {ticket.get('1')}) ---")
        print(f"  Campo 2  (Título)           : {str(ticket.get('2', ''))[:50]}")
        print(f"  Campo 4  (Requester)        : {ticket.get('4', 'N/A')}")
        print(f"  Campo 22 (Requester Email)  : {ticket.get('22', 'N/A')}")
        print(f"  Campo 15 (Date creation)    : {ticket.get('15', 'N/A')}")
        print()

    sess.get(f"{cfg['glpi_url']}/killSession", timeout=10)

if __name__ == "__main__":
    main()
