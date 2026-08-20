"""
Telegram Sender
===============
Módulo para enviar mensajes a un grupo de Telegram
usando directamente la API HTTP de Telegram Bot.
"""

import requests
import logging

logger = logging.getLogger(__name__)

TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}"


class TelegramSender:
    """Cliente para enviar mensajes a Telegram via Bot API."""

    def __init__(self, bot_token: str, chat_id: str):
        """
        Inicializa el sender de Telegram.

        Args:
            bot_token: Token del bot (de @BotFather)
            chat_id: ID del chat/grupo donde enviar mensajes
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_base = TELEGRAM_API_BASE.format(token=bot_token)

    def test_connection(self) -> bool:
        """Verifica que el bot token sea válido."""
        try:
            response = requests.get(
                f"{self.api_base}/getMe",
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            if data.get("ok"):
                bot_info = data.get("result", {})
                bot_name = bot_info.get("first_name", "Desconocido")
                bot_username = bot_info.get("username", "")
                logger.info(f"✅ Bot conectado: {bot_name} (@{bot_username})")
                return True
            else:
                logger.error(f"❌ Token de bot inválido: {data}")
                return False
        except Exception as e:
            logger.error(f"❌ Error al verificar bot de Telegram: {e}")
            return False

    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """
        Envía un mensaje al chat/grupo configurado.

        Args:
            text: Texto del mensaje (puede contener HTML/Markdown)
            parse_mode: Modo de parseo ("HTML" o "Markdown")

        Returns:
            True si el mensaje se envió correctamente
        """
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True,
            }

            response = requests.post(
                f"{self.api_base}/sendMessage",
                json=payload,
                timeout=30,
            )

            data = response.json()

            if data.get("ok"):
                logger.info("✅ Mensaje enviado a Telegram exitosamente.")
                return True
            else:
                error_desc = data.get("description", "Error desconocido")
                error_code = data.get("error_code", "?")
                logger.error(f"❌ Error de Telegram [{error_code}]: {error_desc}")

                # Si el error es por formato HTML, intentar enviar sin formato
                if error_code == 400 and "parse" in error_desc.lower():
                    logger.info("🔄 Reintentando sin formato HTML...")
                    return self.send_message(text, parse_mode=None)

                return False

        except requests.exceptions.Timeout:
            logger.error("❌ Timeout al enviar mensaje a Telegram.")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado al enviar mensaje: {e}")
            return False

    def send_long_message(self, messages: list, parse_mode: str = "HTML") -> bool:
        """
        Envía una lista de mensajes (para mensajes que exceden el límite de 4096 chars).

        Args:
            messages: Lista de strings a enviar secuencialmente
            parse_mode: Modo de parseo

        Returns:
            True si todos los mensajes se enviaron correctamente
        """
        success = True
        for i, msg in enumerate(messages):
            if not self.send_message(msg, parse_mode):
                logger.error(f"❌ Falló el envío del mensaje parte {i + 1}/{len(messages)}")
                success = False
        return success

    def get_chat_id_from_updates(self) -> list:
        """
        Obtiene los chat IDs de los mensajes recientes recibidos por el bot.
        Útil para descubrir el chat_id del grupo.

        Returns:
            Lista de diccionarios con info de chats encontrados
        """
        try:
            response = requests.get(
                f"{self.api_base}/getUpdates",
                params={"limit": 20},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if not data.get("ok"):
                logger.error("No se pudieron obtener updates del bot.")
                return []

            chats = {}
            for update in data.get("result", []):
                message = update.get("message") or update.get("my_chat_member", {}).get("chat", {})
                if not message:
                    continue

                chat = message.get("chat", message) if "chat" in message else message
                chat_id = chat.get("id")
                chat_title = chat.get("title", chat.get("first_name", "DM Privado"))
                chat_type = chat.get("type", "desconocido")

                if chat_id and chat_id not in chats:
                    chats[chat_id] = {
                        "chat_id": chat_id,
                        "title": chat_title,
                        "type": chat_type,
                    }

            return list(chats.values())

        except Exception as e:
            logger.error(f"Error al obtener updates: {e}")
            return []
