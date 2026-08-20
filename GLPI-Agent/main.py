"""
GLPI Agent - Bot de Telegram para resumen de tickets

Uso:
    python main.py              → Scheduler (modo producción)
    python main.py --now        → Reporte inmediato
    python main.py --discover   → Descubrir Chat ID de Telegram
    python main.py --test-glpi  → Probar conexión GLPI
    python main.py --test-tg    → Probar Telegram
"""

import os, sys, logging, argparse, urllib3, io
from datetime import datetime
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from glpi_client import GLPIClient
from report_builder import build_telegram_report, build_summary_short, split_message
from telegram_sender import TelegramSender
from scheduler import setup_schedule, run_scheduler

LOG_FMT = "%(asctime)s │ %(levelname)-7s │ %(message)s"

def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)

    console = logging.StreamHandler(io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8'))

    logging.basicConfig(level=logging.INFO, format=LOG_FMT, datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[console,
                  logging.FileHandler(os.path.join(log_dir, f"agent_{datetime.now():%Y%m%d}.log"), encoding="utf-8")])

def load_config():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        print(f"❌ No se encontró .env en {env_path}"); sys.exit(1)
    load_dotenv(env_path)
    return {k: os.getenv(v, d) for k, v, d in [
        ("glpi_url", "GLPI_URL", ""), ("app_token", "APP_TOKEN", ""),
        ("user_token", "USER_TOKEN", ""), ("glpi_user", "GLPI_USER", ""),
        ("glpi_password", "GLPI_PASSWORD", ""), ("email_domain", "EMAIL_DOMAIN", ""),
        ("category_name", "CATEGORY_NAME", ""), ("telegram_bot_token", "TELEGRAM_BOT_TOKEN", ""),
        ("telegram_chat_id", "TELEGRAM_CHAT_ID", ""),
        ("schedule_morning", "SCHEDULE_MORNING", "08:00"),
        ("schedule_afternoon", "SCHEDULE_AFTERNOON", "17:00"),
    ]}

def validate_config(cfg, need_tg=True):
    ok = True
    for k in ["glpi_url", "app_token"]:
        if not cfg[k]: logging.error(f"❌ Falta {k.upper()} en .env"); ok = False
    if not cfg["glpi_user"] and not cfg["user_token"]:
        logging.error("❌ Configura GLPI_USER/GLPI_PASSWORD o USER_TOKEN en .env"); ok = False
    if need_tg:
        if not cfg["telegram_bot_token"] or cfg["telegram_bot_token"] == "TU_TOKEN_AQUI":
            logging.error("❌ Falta TELEGRAM_BOT_TOKEN"); ok = False
        if not cfg["telegram_chat_id"] or cfg["telegram_chat_id"] == "TU_CHAT_ID_AQUI":
            logging.error("❌ Falta TELEGRAM_CHAT_ID. Usa: python main.py --discover"); ok = False
    return ok

def make_glpi(cfg):
    return GLPIClient(cfg["glpi_url"], cfg["app_token"], cfg["user_token"], cfg["glpi_user"], cfg["glpi_password"])

def run_report(cfg):
    logger = logging.getLogger(__name__)
    logger.info("=" * 45)
    logger.info("🤖 GLPI AGENT — Generando reporte...")
    glpi = make_glpi(cfg)
    if not glpi.init_session():
        logger.error("No se pudo conectar a GLPI."); return False
    try:
        tickets = glpi.search_tickets(
            email_domain=cfg["email_domain"] or None,
            category_name=cfg["category_name"] or None)
        if not tickets:
            logger.info("🔄 Intentando método alternativo...")
            raw = glpi.get_all_tickets_raw()
            if raw:
                tickets = [{
                    "id": t.get("id","?"), "title": t.get("name","Sin título"),
                    "priority": t.get("priority",3), "priority_name": GLPIClient.PRIORITY_MAP.get(t.get("priority",3),"Media"),
                    "status": t.get("status",1), "status_name": GLPIClient.STATUS_MAP.get(t.get("status",1),"Nuevo"),
                    "date_creation": t.get("date",""), "category": str(t.get("itilcategories_id","")),
                    "requester": "", "requester_email": "", "technician": "",
                    "urgency": t.get("urgency",3), "due_date": t.get("time_to_resolve",""),
                } for t in raw]
                tickets.sort(key=lambda t: (-t["priority"], t["date_creation"]))
        logger.info(f"📊 {build_summary_short(tickets)}")
        report = build_telegram_report(tickets)
        tg = TelegramSender(cfg["telegram_bot_token"], cfg["telegram_chat_id"])
        parts = split_message(report)
        logger.info(f"📤 Enviando {len(parts)} mensaje(s) a Telegram...")
        ok = tg.send_long_message(parts)
        logger.info("✅ Reporte enviado." if ok else "❌ Error al enviar.")
        return ok
    finally:
        glpi.kill_session()

def discover_chat_id(cfg):
    bt = cfg["telegram_bot_token"]
    if not bt or bt == "TU_TOKEN_AQUI":
        print("❌ Configura TELEGRAM_BOT_TOKEN primero."); return
    tg = TelegramSender(bt, "")
    if not tg.test_connection(): return
    print("\n🔍 DESCUBRIMIENTO DE CHAT ID")
    print("1. Agrega el bot al grupo  2. Envía un mensaje  3. Presiona Enter")
    input("\nPresiona Enter...")
    chats = tg.get_chat_id_from_updates()
    if not chats:
        print("❌ No se encontraron chats. Verifica que el bot esté en el grupo."); return
    print(f"\n✅ {len(chats)} chat(s) encontrado(s):\n")
    for c in chats:
        print(f"  📌 {c['title']}  |  Tipo: {c['type']}  |  ID: {c['chat_id']}")
    print("\nCopia el ID y pégalo en .env como TELEGRAM_CHAT_ID")

def test_glpi(cfg):
    glpi = make_glpi(cfg)
    if not glpi.init_session(): return
    try:
        tickets = glpi.search_tickets(cfg["email_domain"] or None, cfg["category_name"] or None)
        if tickets:
            print(f"\n✅ {len(tickets)} tickets encontrados:\n")
            for t in tickets[:15]:
                e = {5:"🔴",4:"🟠",3:"🟡",2:"🟢",1:"⚪"}.get(t["priority"],"⚪")
                title = str(t['title'])[:50]
                print(f"  {e} #{t['id']} — {title}  [{t['status_name']}]")
        else:
            print("⚠️ No se encontraron tickets con los filtros actuales.")
            raw = glpi.get_all_tickets_raw()
            if raw:
                print(f"\n📋 {len(raw)} tickets activos (sin filtro):")
                for t in raw[:10]: print(f"   #{t.get('id')} — {t.get('name','N/A')[:50]}")
    finally:
        glpi.kill_session()

def test_telegram(cfg):
    tg = TelegramSender(cfg["telegram_bot_token"], cfg["telegram_chat_id"])
    if not tg.test_connection(): return
    msg = f"🧪 <b>Test GLPI Agent</b>\n✅ Bot funcionando\n📅 {datetime.now():%d/%m/%Y %H:%M}"
    print("✅ Mensaje enviado!" if tg.send_message(msg) else "❌ Error al enviar.")

def main():
    p = argparse.ArgumentParser(description="GLPI Agent — Bot Telegram")
    p.add_argument("--now", action="store_true", help="Reporte inmediato")
    p.add_argument("--discover", action="store_true", help="Descubrir Chat ID")
    p.add_argument("--test-glpi", action="store_true", help="Probar GLPI")
    p.add_argument("--test-tg", action="store_true", help="Probar Telegram")
    args = p.parse_args()
    setup_logging()
    cfg = load_config()
    print("\n" + "="*40)
    print("   GLPI AGENT - Telegram Bot")
    print("="*40 + "\n")

    if args.discover:
        discover_chat_id(cfg); return
    if args.test_glpi:
        if validate_config(cfg, False): test_glpi(cfg); return
    if args.test_tg:
        if validate_config(cfg, True): test_telegram(cfg); return
    if args.now:
        if validate_config(cfg, True): run_report(cfg); return

    if not validate_config(cfg, True): return
    logger = logging.getLogger(__name__)
    logger.info(f"📡 GLPI: {cfg['glpi_url']}")
    logger.info(f"📧 Filtro: {cfg['email_domain'] or 'Ninguno'}")
    logger.info(f"⏰ Horarios: {cfg['schedule_morning']} y {cfg['schedule_afternoon']}")
    setup_schedule(lambda: run_report(cfg), cfg["schedule_morning"], cfg["schedule_afternoon"])
    try:
        run_scheduler()
    except KeyboardInterrupt:
        logger.info("🛑 Detenido.")

if __name__ == "__main__":
    main()
