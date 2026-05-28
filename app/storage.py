import json
import os
import sqlite3
from datetime import datetime, timedelta
from threading import Lock

from app.constants import DEFAULT_LOG_RETENTION_DAYS, MESSAGES_DB_PATH


class MessageLogger:
    def __init__(self, db_path: str = MESSAGES_DB_PATH, retention_days: int = DEFAULT_LOG_RETENTION_DAYS):
        self.db_path = db_path
        self.retention_days = retention_days
        self.lock = Lock()
        self._init_database()
        self.clean_old_logs()

    def _init_database(self) -> None:
        with self.lock:
            os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    sender TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    message TEXT NOT NULL,
                    message_id TEXT,
                    send_time TEXT,
                    delivery_time TEXT,
                    read_time TEXT,
                    log_time TEXT NOT NULL
                )
            """
            )
            columns = {row[1] for row in cursor.execute("PRAGMA table_info(messages)")}
            if "message_id" not in columns:
                cursor.execute("ALTER TABLE messages ADD COLUMN message_id TEXT")
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_messages_message_id ON messages(message_id)"
            )
            conn.commit()
            conn.close()

    def clean_old_logs(self, days: int | None = None) -> int:
        days = days if days is not None else self.retention_days
        try:
            with self.lock:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                old_date = (datetime.now() - timedelta(days=days)).isoformat()
                cursor.execute("DELETE FROM messages WHERE log_time < ?", (old_date,))
                deleted = cursor.rowcount
                conn.commit()
                conn.close()
                return deleted
        except OSError:
            return 0

    def log_message(
        self,
        msg_type: str,
        sender: str,
        recipient: str,
        message: str,
        send_time: datetime | None = None,
        delivery_time: datetime | None = None,
        read_time: datetime | None = None,
        message_id: str | None = None,
    ) -> None:
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO messages
                (type, sender, recipient, message, message_id, send_time, delivery_time, read_time, log_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    msg_type,
                    sender,
                    recipient,
                    message,
                    message_id,
                    send_time.isoformat() if send_time else None,
                    delivery_time.isoformat() if delivery_time else None,
                    read_time.isoformat() if read_time else None,
                    datetime.now().isoformat(),
                ),
            )
            conn.commit()
            conn.close()

    def mark_delivered(self, message_id: str, delivery_time: datetime | None = None) -> None:
        if not message_id:
            return
        delivery_time = delivery_time or datetime.now()
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE messages
                SET delivery_time = ?
                WHERE message_id = ? AND type = 'SENT' AND delivery_time IS NULL
            """,
                (delivery_time.isoformat(), message_id),
            )
            conn.commit()
            conn.close()

    def mark_read(self, message_id: str, read_time: datetime | None = None) -> None:
        if not message_id:
            return
        read_time = read_time or datetime.now()
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE messages
                SET read_time = ?
                WHERE message_id = ? AND type = 'SENT' AND read_time IS NULL
            """,
                (read_time.isoformat(), message_id),
            )
            conn.commit()
            conn.close()

    def export_to_json(self, filepath: str = "logs/messages_export.json") -> str:
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM messages ORDER BY id")
            rows = cursor.fetchall()
            columns = [
                "id",
                "type",
                "sender",
                "recipient",
                "message",
                "message_id",
                "send_time",
                "delivery_time",
                "read_time",
                "log_time",
            ]
            messages = [dict(zip(columns, row)) for row in rows]
            with open(filepath, "w", encoding="utf-8") as handle:
                json.dump(messages, handle, ensure_ascii=False, indent=2)
            conn.close()
            return filepath
