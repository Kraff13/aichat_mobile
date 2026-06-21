"""Кэш истории чата на основе SQLite."""
import sqlite3
from datetime import datetime
from utils.storage import get_db_path
from utils.logger import AppLogger


class ChatCache:
    """Хранение истории диалогов в локальной БД."""

    def __init__(self):
        self.logger = AppLogger()
        # [MOBILE] путь к БД берём из кроссплатформенного хранилища.
        self.db_path = get_db_path()
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model TEXT,
                    user_message TEXT,
                    ai_response TEXT,
                    timestamp TEXT,
                    tokens_used INTEGER
                )
                """
            )
            conn.commit()
            conn.close()
            self.logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            self.logger.error(f"Database init failed: {e}", exc_info=True)

    def save_message(self, model, user_message, ai_response, tokens_used=0):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chat_history
                    (model, user_message, ai_response, timestamp, tokens_used)
                VALUES (?, ?, ?, ?, ?)
                """,
                (model, user_message, ai_response, datetime.now().isoformat(), tokens_used),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Save message failed: {e}", exc_info=True)

    def get_chat_history(self):
        """Возвращает список кортежей
        (id, model, user_message, ai_response, timestamp, tokens_used), новые сначала."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, model, user_message, ai_response, timestamp, tokens_used
                FROM chat_history
                ORDER BY id DESC
                """
            )
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            self.logger.error(f"Get history failed: {e}", exc_info=True)
            return []

    def clear_history(self):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_history")
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Clear history failed: {e}", exc_info=True)
