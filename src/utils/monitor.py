"""Мониторинг производительности приложения."""
import time

# [MOBILE] psutil — нативная библиотека, которая не собирается под Android/iOS
# через flet build. Делаем импорт опциональным и корректно деградируем.
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False


class PerformanceMonitor:
    """Сбор метрик производительности."""

    def __init__(self):
        self.start_time = time.time()

    def get_metrics(self):
        metrics = {
            "uptime_seconds": round(time.time() - self.start_time, 2),
            "psutil_available": PSUTIL_AVAILABLE,
        }
        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process()
                metrics["memory_mb"] = round(process.memory_info().rss / (1024 * 1024), 2)
                metrics["cpu_percent"] = process.cpu_percent(interval=None)
            except Exception:
                # На некоторых платформах метрики недоступны — просто пропускаем.
                pass
        return metrics

    def log_metrics(self, logger):
        metrics = self.get_metrics()
        logger.info(f"Performance metrics: {metrics}")
        return metrics
