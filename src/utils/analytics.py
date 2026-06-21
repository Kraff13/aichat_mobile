"""Аналитика использования чата."""
from datetime import datetime


class Analytics:
    """Сбор статистики по сообщениям текущей сессии."""

    def __init__(self, cache=None):
        self.cache = cache
        self.messages = []
        self.start_time = datetime.now()

    def track_message(self, model, message_length, response_time, tokens_used):
        self.messages.append({
            "model": model,
            "message_length": message_length,
            "response_time": response_time,
            "tokens_used": tokens_used,
            "timestamp": datetime.now(),
        })

    def get_statistics(self):
        total_messages = len(self.messages)
        total_tokens = sum(m.get("tokens_used", 0) for m in self.messages)
        tokens_per_message = (total_tokens / total_messages) if total_messages else 0.0
        elapsed_minutes = max(
            (datetime.now() - self.start_time).total_seconds() / 60.0, 1e-9
        )
        messages_per_minute = (total_messages / elapsed_minutes) if total_messages else 0.0
        return {
            "total_messages": total_messages,
            "total_tokens": total_tokens,
            "tokens_per_message": tokens_per_message,
            "messages_per_minute": messages_per_minute,
        }

    def clear_data(self):
        self.messages = []
        self.start_time = datetime.now()
