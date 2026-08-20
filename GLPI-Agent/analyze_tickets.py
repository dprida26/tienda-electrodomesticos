#!/usr/bin/env python3
"""
Script para analizar qué tickets cumplen los criterios de filtro
"""

import os
import sys
import logging
from dotenv import load_dotenv
from glpi_client import GLPIClient
from datetime import datetime

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
        ("glpi_password", "GLPI_PASSWORD", ""), ("email_domain", "EMAIL_DOMAIN", ""),
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
        logger.info("📡 Obteniendo todos los tickets sin filtros...")

        # Obtener tickets sin filtro de email
        import requests
        import base64

        today = datetime.now()
        month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = (month_start.replace(day=1) + __import__('datetime').timedelta(days=32)).replace(day=1) - __import__('datetime').timedelta(seconds=1)

        params = {
            "forcedisplay[0]": 1, "forcedisplay[1]": 2, "forcedisplay[2]": 3,
            "forcedisplay[3]": 12, "forcedisplay[4]": 15, "forcedisplay[5]": 7,
            "forcedisplay[6]": 4, "forcedisplay[7]": 22, "forcedisplay[8]": 5,
            "forcedisplay[9]": 10, "forcedisplay[10]": 18,
            "range": "0-200", "sort": 3, "order": "DESC",
        }

        # Criterios: solo estados activos y mes actual (SIN filtro de email)
        ci = 0
        for i, s in enumerate([1, 2, 3, 4]):
            if i == 0:
                params[f"criteria[{ci}][field]"] = 12
                params[f"criteria[{ci}][searchtype]"] = "equals"
                params[f"criteria[{ci}][value]"] = s
            else:
                ci += 1
                params[f"criteria[{ci}][link]"] = "OR"
                params[f"criteria[{ci}][field]"] = 12
                params[f"criteria[{ci}][searchtype]"] = "equals"
                params[f"criteria[{ci}][value]"] = s

        ci += 1
        params[f"criteria[{ci}][link]"] = "AND"
        params[f"criteria[{ci}][field]"] = 15
        params[f"criteria[{ci}][searchtype]"] = ">=>"
        params[f"criteria[{ci}][value]"] = month_start.isoformat()

        ci += 1
        params[f"criteria[{ci}][link]"] = "AND"
        params[f"criteria[{ci}][field]"] = 15
        params[f"criteria[{ci}][searchtype]"] = "<"
        params[f"criteria[{ci}][value]"] = month_end.isoformat()

        resp = glpi.session.get(f"{glpi.base_url}/search/Ticket", params=params, timeout=60)
        result = resp.json()

        all_tickets = result.get("data", [])
        logger.info(f"✅ Total sin filtro email: {len(all_tickets)} tickets")

        # Analizar los emails
        print("\n" + "="*80)
        print("ANÁLISIS DE EMAILS EN TICKETS:")
        print("="*80 + "\n")

        emails = {}
        for ticket in all_tickets:
            email = ticket.get("22", "SIN EMAIL")
            if email not in emails:
                emails[email] = 0
            emails[email] += 1

        print("Distribución de emails (campo 22):\n")
        for email, count in sorted(emails.items(), key=lambda x: -x[1])[:15]:
            email_str = str(email) if email else "None"
            print(f"  {email_str:40} → {count} tickets")

        print(f"\n... y {len(emails) - 15} emails más" if len(emails) > 15 else "")

        # Contar con @amsa.com.py
        amsa_count = sum(1 for t in all_tickets if "@amsa.com.py" in str(t.get("22", "")))
        print(f"\n📌 Tickets con @amsa.com.py en campo 22: {amsa_count}")

    finally:
        glpi.kill_session()

if __name__ == "__main__":
    main()
