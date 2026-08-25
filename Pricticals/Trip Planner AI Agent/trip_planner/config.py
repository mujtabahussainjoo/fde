from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5.3-codex")
    app_data_dir: Path = Path(os.getenv("APP_DATA_DIR", "./data"))
    app_log_level: str = os.getenv("APP_LOG_LEVEL", "INFO")

    nominatim_base_url: str = os.getenv(
        "NOMINATIM_BASE_URL", "https://nominatim.openstreetmap.org"
    )
    overpass_base_url: str = os.getenv(
        "OVERPASS_BASE_URL", "https://overpass-api.de/api/interpreter"
    )
    wikivoyage_api_url: str = os.getenv(
        "WIKIVOYAGE_API_URL", "https://en.wikivoyage.org/w/api.php"
    )

    http_timeout_seconds: int = int(os.getenv("HTTP_TIMEOUT_SECONDS", "30"))
    http_retries: int = int(os.getenv("HTTP_RETRIES", "3"))
    http_backoff_seconds: float = float(os.getenv("HTTP_BACKOFF_SECONDS", "1.2"))


def get_settings() -> Settings:
    settings = Settings()
    settings.app_data_dir.mkdir(parents=True, exist_ok=True)
    return settings
