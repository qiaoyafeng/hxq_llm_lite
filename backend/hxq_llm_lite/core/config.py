from functools import lru_cache

from pydantic_settings import BaseSettings

config_path = __file__


class Settings(BaseSettings):
    BASE_DOMAIN: str = "http://127.0.0.1:8000"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    WORKERS: int = 1
    RELOAD: bool = False
    USE_HTTPS: bool = False

    # DB
    DATABASE_TYPE: str = "mysql"  # sqlite or mysql
    DB_IP: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_NAME: str = "hxq_llm_lite"
    DB_USERNAME: str = "root"
    DB_PASSWORD: str = "123456"
    DB_SQLITE_PATH: str = "hxq_llm_lite.db"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
