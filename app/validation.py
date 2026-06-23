import re

from app.constants import MAX_MESSAGE_LENGTH

JID_PATTERN = re.compile(r"^[^@\s/]+@[^@\s/]+$|^[^@\s/]+$")


def validate_message(text: str) -> str:
    message = (text or "").strip()
    if not message:
        raise ValueError("Сообщение не может быть пустым")
    if len(message) > MAX_MESSAGE_LENGTH:
        raise ValueError(f"Сообщение превышает {MAX_MESSAGE_LENGTH} символов")
    return message


def validate_jid(jid: str, default_domain: str) -> str:
    value = (jid or "").strip()
    if not value:
        raise ValueError("JID не указан")
    if "@" not in value:
        value = f"{value}@{default_domain}"
    if not JID_PATTERN.match(value.split("/")[0]):
        raise ValueError("Некорректный JID")
    return value.split("/")[0]
