# Импорт необходимых библиотек
import requests  # HTTP-запросы к API
import os       # Работа с переменными окружения
from dotenv import load_dotenv  # Загрузка переменных из .env
from utils.logger import AppLogger

load_dotenv()


class OpenRouterClient:
    """Клиент для взаимодействия с OpenRouter API."""

    def __init__(self):
        self.logger = AppLogger()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("BASE_URL")

        if not self.api_key:
            self.logger.error("OpenRouter API key not found in .env")
            raise ValueError("OpenRouter API key not found in .env")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.logger.info("OpenRouterClient initialized successfully")
        self.available_models = self.get_models()

    def get_models(self):
        self.logger.debug("Fetching available models")
        try:
            response = requests.get(f"{self.base_url}/models", headers=self.headers)
            models_data = response.json()
            # [FIX] вложенные кавычки одного типа в f-строке (models_data["data"])
            # работают только в Python 3.12+. Используем одинарные кавычки внутри.
            self.logger.info(f"Retrieved {len(models_data['data'])} models")
            return [
                {"id": model["id"], "name": model["name"]}
                for model in models_data["data"]
            ]
        except Exception as e:
            models_default = [
                {"id": "deepseek/deepseek-chat", "name": "DeepSeek"},
                {"id": "anthropic/claude-3.5-sonnet", "name": "Claude 3.5 Sonnet"},
                {"id": "openai/gpt-3.5-turbo", "name": "GPT-3.5 Turbo"}
            ]
            self.logger.info(f"Retrieved {len(models_default)} models with Error: {e}")
            return models_default

    def send_message(self, message: str, model: str):
        self.logger.debug(f"Sending message to model: {model}")
        data = {
            "model": model,
            "messages": [{"role": "user", "content": message}]
        }
        try:
            self.logger.debug("Making API request")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            self.logger.info("Successfully received response from API")
            return response.json()
        except Exception as e:
            error_msg = f"API request failed: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return {"error": str(e)}

    def get_balance(self):
        try:
            response = requests.get(f"{self.base_url}/credits", headers=self.headers)
            data = response.json()
            if data:
                data = data.get('data')
                return f"${(data.get('total_credits', 0) - data.get('total_usage', 0)):.2f}"
            return "Ошибка"
        except Exception as e:
            error_msg = f"API request failed: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return "Ошибка"
