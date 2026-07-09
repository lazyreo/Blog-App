from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    POSTGRESQL_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    AI_API_KEY: str
    REDIS_BROKER: str
    REDIS_BACKEND: str
    BOT1_PASSWORD: str
    BOT2_PASSWORD: str
    BOT3_PASSWORD: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings() # type: ignore
