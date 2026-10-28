from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="", extra="ignore"
    )

    app_nome: str = "Catálogo"
    app_ambiente: str = "dev"
    database_url: str = ""
    secret_key: str = ""


@lru_cache
def get_config() -> Config:
    return Config()
