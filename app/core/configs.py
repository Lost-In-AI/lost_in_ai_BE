from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Lost In AI"
    OPENAI_API_KEY: str
    MAX_TOKENS: int
    DATABASE_URL: str
    DATABASE_ECHO: bool

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8"
    )


settings = Settings()
