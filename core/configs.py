from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    APP_NAME: str = "Lost In AI"


    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8"
        )

settings = Settings()


    