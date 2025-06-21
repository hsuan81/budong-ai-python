import os

from dotenv import load_dotenv

load_dotenv(".env.local")

MODEL_LIST = [
    "openai/gpt-4.1-nano-2025-04-14",
    "mistralai/devstral-small:free",
    "mistralai/mistral-7b-instruct:free",
]


class Config:
    def __init__(self):
        self.openrouter_api_key = self._get_required_env("OPENROUTER_API_KEY")
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        self.model = MODEL_LIST[0]

    def _get_required_env(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"{key} not found in environment")
        return value


# config = Config()
