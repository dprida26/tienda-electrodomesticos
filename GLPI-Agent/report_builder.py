"""
Report Builder
==============
Módulo para generar reportes formateados de tickets GLPI
optimizados para envío vía Telegram (con emojis y formato HTML).
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Emojis por nivel de prioridad
PRIORITY_EMOJI = {
    6: "🔴🔴",   # Mayor
    5: "🔴",     # Muy alta
    4: "🟠",     # Alta
    3: "🟡",     # Media
    2: "🟢",     # Baja
    1: "⚪",     # Muy baja
}

PRIORITY_LABEL = {
    6: "MAYOR",
    5: "MUY ALTA",
    4: "ALTA",
    3: "MEDIA",
    2: "BAJA",
    1: "MUY BAJA",
}

STATUS_EMOJI = {
    1: "🆕",     # Nuevo
    2: "🔧",     # En curso (Asignado)
    3: "📋",     # En curso (Planificado)
    4: "⏳",     # En espera
}


def build_telegram_report(tickets: list, report_time: datetime = None) -> str:
    """
    Genera un reporte formateado en HTML para Telegram.

    Args:
        tickets: Lista de diccionarios con datos de tickets
        report_time: Fecha/hora del reporte (por defecto: ahora)

    Returns:
        String con el mensaje formateado en HTML para Telegram
    """
    if report_time is None:
        report_time = datetime.now()

    timestamp = report_time.strftime("%d/%m/%Y %H:%M")

    if not tickets:
        return (
            f"📊 <b>RESUMEN GLPI — {timestamp}</b>\n"
            f"{'━' * 28}\n\n"
            f"✅ <b>¡Sin tickets pendientes!</b>\n\n"
            f"No hay tickets activos para el área técnica en este momento.\n"
            f"¡Excelente trabajo del equipo! 🎉"
        )

    # Agrupar tickets por prioridad
    tickets_by_priority = {}
    for ticket in tickets:
        priority = ticket.get("priority", 3)
        if priority not in tickets_by_priority:
            tickets_by_priority[priority] = []
        tickets_by_priority[priority].append(ticket)

    # Construir el mensaje
    lines = []

    # Encabezado
    lines.append(f"📊 <b>RESUMEN GLPI — {timestamp}</b>")
    lines.append(f"{'━' * 28}")
    lines.append(f"📌 <b>Tickets activos: {len(tickets)}</b>")
    lines.append("")

    # Tickets agrupados por prioridad (de mayor a menor)
    for priority in sorted(tickets_by_priority.keys(), reverse=True):
        group = tickets_by_priority[priority]
        emoji = PRIORITY_EMOJI.get(priority, "⚪")
        label = PRIORITY_LABEL.get(priority, "DESCONOCIDA")

        lines.append(f"{emoji} <b>PRIORIDAD {label} ({len(group)} ticket{'s' if len(group) > 1 else ''})</b>")
        lines.append(f"{'─' * 26}")

        for ticket in group:
            ticket_id = ticket.get("id", "?")
            title = _truncate(ticket.get("title", "Sin título"), 60)
            requester = ticket.get("requester", "Desconocido")
            date_str = _format_date(ticket.get("date_creation", ""))
            status_code = ticket.get("status", 1)
            status_emoji = STATUS_EMOJI.get(status_code, "❓")
            status_name = ticket.get("status_name", "Desconocido")
            technician = ticket.get("technician", "Sin asignar")

            lines.append(f"  📌 <b>#{ticket_id}</b> — {title}")
            lines.append(f"       👤 {requester}")
            lines.append(f"       📅 {date_str}")
            lines.append(f"       {status_emoji} {status_name}")
            if technician and technician != "Sin asignar":
                lines.append(f"       🔧 Técnico: {technician}")
            lines.append("")

    # Resumen al final
    lines.append(f"{'━' * 28}")
    lines.append(f"📈 <b>Resumen por prioridad:</b>")
    for priority in sorted(tickets_by_priority.keys(), reverse=True):
        emoji = PRIORITY_EMOJI.get(priority, "⚪")
        label = PRIORITY_LABEL.get(priority, "?")
        count = len(tickets_by_priority[priority])
        lines.append(f"  {emoji} {label}: {count}")

    # Resumen por estado
    status_counts = {}
    for ticket in tickets:
        status = ticket.get("status_name", "Desconocido")
        status_counts[status] = status_counts.get(status, 0) + 1

    lines.append("")
    lines.append(f"📋 <b>Resumen por estado:</b>")
    for status, count in sorted(status_counts.items()):
        lines.append(f"  • {status}: {count}")

    lines.append("")
    lines.append(f"🤖 <i>Bot GLPI Agent — Generado automáticamente</i>")

    return "\n".join(lines)


def build_summary_short(tickets: list) -> str:
    """
    Genera un resumen corto (una línea) para logging.

    Args:
        tickets: Lista de tickets

    Returns:
        String con resumen corto
    """
    if not tickets:
        return "0 tickets activos"

    priority_counts = {}
    for t in tickets:
        p = t.get("priority", 3)
        label = PRIORITY_LABEL.get(p, "?")
        priority_counts[label] = priority_counts.get(label, 0) + 1

    parts = [f"{v} {k}" for k, v in sorted(priority_counts.items(), reverse=True)]
    return f"{len(tickets)} tickets activos: {', '.join(parts)}"


def _truncate(text: str, max_length: int) -> str:
    """Trunca un texto a un largo máximo, añadiendo '...' si es necesario."""
    if not text:
        return ""
    text = str(text)
    # Limpiar HTML tags que podrían venir del GLPI
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text


def _format_date(date_str: str) -> str:
    """Convierte una fecha ISO a formato legible en español."""
    if not date_str or date_str == "N/A":
        return "Fecha desconocida"
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, AttributeError):
        return date_str


def split_message(message: str, max_length: int = 4096) -> list:
    """
    Divide un mensaje largo en partes que respeten el límite de Telegram.
    Intenta cortar en saltos de línea para no romper el formato.

    Args:
        message: Mensaje completo
        max_length: Largo máximo por mensaje de Telegram (default 4096)

    Returns:
        Lista de strings, cada uno dentro del límite
    """
    if len(message) <= max_length:
        return [message]

    parts = []
    current = ""

    for line in message.split("\n"):
        # Si agregar esta línea excede el límite, guardar lo actual y empezar nuevo
        if len(current) + len(line) + 1 > max_length:
            if current:
                parts.append(current.rstrip("\n"))
            current = line + "\n"
        else:
            current += line + "\n"

    if current.strip():
        parts.append(current.rstrip("\n"))

    # Agregar indicador de continuación
    if len(parts) > 1:
        for i in range(len(parts)):
            parts[i] = f"📄 ({i + 1}/{len(parts)})\n\n{parts[i]}"

    return parts
