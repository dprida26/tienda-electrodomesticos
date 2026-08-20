"""
GLPI REST API Client — Soporta Basic Auth y User Token
"""

import requests
import logging
import base64
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


class GLPIClient:
    STATUS_MAP = {1: "Nuevo", 2: "En curso (Asignado)", 3: "En curso (Planificado)", 4: "En espera", 5: "Resuelto", 6: "Cerrado"}
    PRIORITY_MAP = {1: "Muy baja", 2: "Baja", 3: "Media", 4: "Alta", 5: "Muy alta", 6: "Mayor"}
    URGENCY_MAP = {1: "Muy baja", 2: "Baja", 3: "Media", 4: "Alta", 5: "Muy alta"}
    ACTIVE_STATUSES = [1, 2, 3, 4]

    def __init__(self, base_url, app_token, user_token="", username="", password=""):
        self.base_url = base_url.rstrip("/")
        self.app_token = app_token
        self.user_token = user_token
        self.username = username
        self.password = password
        self.session_token = None
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({"App-Token": self.app_token, "Content-Type": "application/json"})

    def init_session(self):
        try:
            # Preferir Basic Auth si hay usuario y contraseña
            if self.username and self.password:
                credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
                self.session.headers["Authorization"] = f"Basic {credentials}"
                logger.info("🔑 Usando autenticación por usuario/contraseña...")
            elif self.user_token:
                self.session.headers["Authorization"] = f"user_token {self.user_token}"
                logger.info("🔑 Usando autenticación por User Token...")
            else:
                logger.error("❌ No hay credenciales configuradas.")
                return False

            resp = self.session.get(f"{self.base_url}/initSession", timeout=30)
            resp.raise_for_status()
            self.session_token = resp.json().get("session_token")
            if not self.session_token:
                logger.error("❌ No se recibió session_token.")
                return False
            self.session.headers["Session-Token"] = self.session_token
            del self.session.headers["Authorization"]
            logger.info("✅ Sesión GLPI iniciada.")
            return True
        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ Error HTTP al iniciar sesión: {e}")
            if e.response is not None:
                logger.error(f"   Respuesta: {e.response.text[:300]}")
            return False
        except Exception as e:
            logger.error(f"❌ Error de conexión: {e}")
            return False

    def kill_session(self):
        if self.session_token:
            try:
                self.session.get(f"{self.base_url}/killSession", timeout=10)
            except Exception:
                pass
            self.session_token = None

    def get_requester_email(self, ticket_id):
        """Obtiene el email del solicitante (type=1) de un ticket."""
        try:
            resp = self.session.get(f"{self.base_url}/Ticket/{ticket_id}/Ticket_User", timeout=10)
            if resp.status_code == 200:
                try:
                    users = resp.json()
                    if isinstance(users, list):
                        for user in users:
                            if user.get("type") == 1:  # 1 = solicitante
                                email = user.get("alternative_email", "")
                                if email:
                                    return email
                except ValueError:
                    pass
        except Exception as e:
            logger.debug(f"Error obtener email de ticket {ticket_id}: {e}")
        return ""

    def search_tickets(self, email_domain=None, category_name=None):
        if not self.session_token:
            logger.error("No hay sesión activa.")
            return []
        try:
            params = {
                "forcedisplay[0]": 1, "forcedisplay[1]": 2, "forcedisplay[2]": 3,
                "forcedisplay[3]": 12, "forcedisplay[4]": 15, "forcedisplay[5]": 7,
                "forcedisplay[6]": 4, "forcedisplay[7]": 22, "forcedisplay[8]": 5,
                "forcedisplay[9]": 10, "forcedisplay[10]": 18,
                "range": "0-500", "sort": 3, "order": "DESC",
            }
            ci = 0
            for i, s in enumerate(self.ACTIVE_STATUSES):
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

            # Filtro de fecha: del mes actual
            today = datetime.now()
            month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

            ci += 1
            params[f"criteria[{ci}][link]"] = "AND"
            params[f"criteria[{ci}][field]"] = 15  # Campo de fecha de creación
            params[f"criteria[{ci}][searchtype]"] = ">=>"
            params[f"criteria[{ci}][value]"] = month_start.isoformat()

            ci += 1
            params[f"criteria[{ci}][link]"] = "AND"
            params[f"criteria[{ci}][field]"] = 15  # Campo de fecha de creación
            params[f"criteria[{ci}][searchtype]"] = "<"
            params[f"criteria[{ci}][value]"] = month_end.isoformat()

            if category_name:
                ci += 1
                params[f"criteria[{ci}][link]"] = "AND"
                params[f"criteria[{ci}][field]"] = 7
                params[f"criteria[{ci}][searchtype]"] = "contains"
                params[f"criteria[{ci}][value]"] = category_name

            logger.info(f"🔍 Buscando tickets (cat: {category_name or 'todas'}, mes: {today:%B %Y})...")
            resp = self.session.get(f"{self.base_url}/search/Ticket", params=params, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            total = result.get("totalcount", 0)
            logger.info(f"📊 Tickets encontrados en API: {total}")
            if total == 0:
                return []

            items = result.get("data", [])
            tickets = []

            if email_domain:
                logger.info(f"🔄 Filtrando {total} tickets por {email_domain} y mes {today:%B %Y}...")
                for item in items:
                    ticket_id = item.get("2", "?")  # Campo 2 = ID
                    date_creation = item.get("15", "N/A")

                    # Verificar que la fecha esté en el rango del mes actual
                    if date_creation != "N/A":
                        try:
                            ticket_date = datetime.fromisoformat(date_creation.replace("Z", "+00:00"))
                            if not (month_start <= ticket_date <= month_end):
                                continue  # Fecha fuera del rango, saltar
                        except (ValueError, AttributeError):
                            continue  # Fecha inválida, saltar

                    requester_email = self.get_requester_email(ticket_id)

                    if email_domain in str(requester_email):
                        tickets.append({
                            "id": ticket_id, "title": item.get("1", "Sin título"),  # Campo 1 = Título
                            "priority": item.get("3", 3), "priority_name": self.PRIORITY_MAP.get(item.get("3", 3), "Media"),
                            "status": item.get("12", 1), "status_name": self.STATUS_MAP.get(item.get("12", 1), "Nuevo"),
                            "date_creation": date_creation, "category": item.get("7", ""),
                            "requester": item.get("4", "Desconocido"), "requester_email": requester_email,
                            "technician": item.get("5", "Sin asignar"), "urgency": item.get("10", 3),
                            "due_date": item.get("18", ""),
                        })
                logger.info(f"📊 Tickets filtrados por {email_domain} + mes actual: {len(tickets)}")
            else:
                for item in items:
                    ticket_id = item.get("2", "?")  # Campo 2 = ID
                    tickets.append({
                        "id": ticket_id, "title": item.get("1", "Sin título"),  # Campo 1 = Título
                        "priority": item.get("3", 3), "priority_name": self.PRIORITY_MAP.get(item.get("3", 3), "Media"),
                        "status": item.get("12", 1), "status_name": self.STATUS_MAP.get(item.get("12", 1), "Nuevo"),
                        "date_creation": item.get("15", "N/A"), "category": item.get("7", ""),
                        "requester": item.get("4", "Desconocido"), "requester_email": item.get("22", ""),
                        "technician": item.get("5", "Sin asignar"), "urgency": item.get("10", 3),
                        "due_date": item.get("18", ""),
                    })
            tickets.sort(key=lambda t: (-t["priority"], t["date_creation"]))
            return tickets
        except Exception as e:
            logger.error(f"❌ Error al buscar tickets: {e}")
            return []

    def get_all_tickets_raw(self):
        try:
            resp = self.session.get(f"{self.base_url}/Ticket",
                params={"range": "0-200", "expand_dropdowns": "true", "sort": 3, "order": "DESC"}, timeout=60)
            resp.raise_for_status()
            return [t for t in resp.json() if t.get("status") in self.ACTIVE_STATUSES]
        except Exception as e:
            logger.error(f"❌ Error al obtener tickets: {e}")
            return []
