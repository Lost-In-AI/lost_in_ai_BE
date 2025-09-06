from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Lost In AI"


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()


    