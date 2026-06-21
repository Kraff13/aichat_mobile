"""Система логирования приложения."""
import logging
import os
from utils.storage import get_subdir


class AppLogger:
    """Обёртка над стандартным logging с выводом в файл и консоль."""

    def __init__(self):
        self.logger = logging.getLogger("AIChat")
        self.logger.setLevel(logging.DEBUG)

        # [FIX] защита от дублирования обработчиков при повторном создании AppLogger.
        if not self.logger.handlers:
            # [MOBILE] логи пишем в писабельный каталог хранилища, не в CWD.
            log_dir = get_subdir("logs")
            file_handler = logging.FileHandler(
                os.path.join(log_dir, "app.log"), encoding="utf-8"
            )
            file_handler.setLevel(logging.DEBUG)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def debug(self, message, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)
