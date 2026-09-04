from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DevShowcase API"
    app_version: str = "1.0.0"
    app_description: str = "API REST para cadastro de perfis, projetos, tecnologias e feedbacks."
    database_url: str = "sqlite:///./devshowcase.db"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
