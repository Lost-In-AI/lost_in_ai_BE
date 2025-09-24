from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Lost In AI"
    OPENAI_API_KEY: str
    MAX_TOKENS: int
    DATABASE_URL: str
    DATABASE_ECHO: bool
    CLERK_JWKS_URL: str
    CLERK_ISSUER: str
    CLERK_WEBHOOK_SECRET: str

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8"
    )

settings = Settings()
