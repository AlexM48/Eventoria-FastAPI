from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str | None = None
    # POSTGRES_HOST: str | None = None
    # POSTGRES_PORT: int | None = None
    # POSTGRES_USER: str | None = None
    # POSTGRES_PASSWORD: str | None = None
    # POSTGRES_DB: str | None = None
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }
    # class Config:
    #     env_file = ".env"

settings = Settings()
