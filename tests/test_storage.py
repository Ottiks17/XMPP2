import os
import tempfile

from app.storage import MessageLogger


def test_log_and_mark_read():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = os.path.join(tmp, "test.db")
        logger = MessageLogger(db_path=db_path, retention_days=14)
        logger.log_message(
            "SENT",
            "a@b",
            "c@d",
            "hi",
            message_id="msg-1",
        )
        logger.mark_delivered("msg-1")
        logger.mark_read("msg-1")

        import sqlite3

        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT delivery_time, read_time FROM messages WHERE message_id = ?",
            ("msg-1",),
        ).fetchone()
        conn.close()
        assert row[0] is not None
        assert row[1] is not None
