"""Константы и общие утилиты проекта."""

from uuid import uuid4

MAX_MESSAGE_LENGTH = 256
DEFAULT_LOG_RETENTION_DAYS = 14
CONFIG_PATH = "config/config.json"
CHAT_HISTORY_PATH = "logs/chat_history.json"
MESSAGES_DB_PATH = "logs/messages.db"


def new_message_id() -> str:
    """Сквозной ID сообщения (UUID4). Используется в REST, GUI, XMPP и БД."""
    return str(uuid4())