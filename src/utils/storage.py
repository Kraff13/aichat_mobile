"""
[MOBILE] Кроссплатформенное хранилище данных.

На десктопе файлы можно писать рядом с приложением, но на Android/iOS рабочий каталог
только для чтения. Flet предоставляет переменную окружения FLET_APP_STORAGE_DATA,
указывающую на писабельный каталог приложения. Используем её везде.
"""
import os


def get_storage_dir() -> str:
    """Возвращает писабельный каталог данных приложения."""
    base = os.getenv("FLET_APP_STORAGE_DATA")
    if not base:
        # Десктоп / разработка: папка app_data рядом с src.
        base = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "app_data",
        )
    os.makedirs(base, exist_ok=True)
    return base


def get_subdir(name: str) -> str:
    """Возвращает (создавая при необходимости) подкаталог хранилища."""
    path = os.path.join(get_storage_dir(), name)
    os.makedirs(path, exist_ok=True)
    return path


def get_db_path(filename: str = "chat_cache.db") -> str:
    """Возвращает полный путь к файлу БД внутри хранилища."""
    return os.path.join(get_storage_dir(), filename)
