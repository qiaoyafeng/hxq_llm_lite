import os
from functools import lru_cache

from pydantic_settings import BaseSettings

config_path = __file__


class Config:
    @classmethod
    def get_home_path(cls):
        if settings.CUSTOMIZE_DATA_DIR:
            return settings.CUSTOMIZE_DATA_DIR
        return os.path.dirname(config_path)

    @classmethod
    def check_path(cls, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    @classmethod
    def get_temp_path(cls):
        temp_path = os.path.join(cls.get_home_path(), "temp")
        cls.check_path(temp_path)
        return temp_path

    @classmethod
    def get_log_path(cls):
        log_path = os.path.join(cls.get_home_path(), "log")
        cls.check_path(log_path)
        return log_path

    @classmethod
    def get_checkpoints_path(cls):
        checkpoints_path = os.path.join(cls.get_home_path(), "checkpoints")
        cls.check_path(checkpoints_path)
        return checkpoints_path


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

    # Table 名
    TABLE_MESSAGE: str = "message"

    # OLLAMA
    OLLAMA_HOST: str = "http://127.0.0.1:11434"

    DEFAULT_LLM_MODEL: str = "qwen3:4b-instruct"

    # 目录相关
    CUSTOMIZE_DATA_DIR: str = ""

    # 日志相关
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

TEMP_PATH = Config.get_temp_path()
LOG_PATH = Config.get_log_path()
