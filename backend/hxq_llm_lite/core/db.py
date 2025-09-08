from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings
from contextlib import contextmanager
from loguru import logger

# 根据配置选择数据库
if settings.DATABASE_TYPE == "mysql":
    DATABASE_URL = f"mysql+pymysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_IP}:{settings.DB_PORT}/{settings.DB_NAME}"
    engine = create_engine(DATABASE_URL)
else:
    DATABASE_URL = f"sqlite:///{settings.DB_SQLITE_PATH}"
    # SQLite aiosqlite dialect needs this connect_args
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


logger.info(f"Using DATABASE_URL: {DATABASE_URL}")

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db = contextmanager(get_session)


def check_db_connection():
    """
    检查数据库是否可连接
    - MySQL: 执行 SELECT 1
    - SQLite: 执行 PRAGMA quick_check
    """
    try:
        with get_db() as db:
            db.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"check_db_connection error: {e}")
        return False
