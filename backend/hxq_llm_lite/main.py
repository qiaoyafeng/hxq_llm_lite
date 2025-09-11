import uvicorn as uvicorn
from core.config import LOG_PATH, TEMP_PATH, settings
from core.db import DATABASE_URL, check_db_connection
from core.log import logger
from fastapi import FastAPI
from routers import chats
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

app = FastAPI(
    title="好心情-LLM",
    summary="好心情-LLM",
    version="1.0.0",
)


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(chats.router, prefix="/api/chats", tags=["chats"])

logo_ascii = """
.----------------------------------------------------------------------------------.
| █████   █████ █████ █████    ██████       █████       █████       ██████   ██████|
|░░███   ░░███ ░░███ ░░███   ███░░░░███    ░░███       ░░███       ░░██████ ██████ |
| ░███    ░███  ░░███ ███   ███    ░░███    ░███        ░███        ░███░█████░███ |
| ░███████████   ░░█████   ░███     ░███    ░███        ░███        ░███░░███ ░███ |
| ░███░░░░░███    ███░███  ░███   ██░███    ░███        ░███        ░███ ░░░  ░███ |
| ░███    ░███   ███ ░░███ ░░███ ░░████     ░███      █ ░███      █ ░███      ░███ |
| █████   █████ █████ █████ ░░░██████░██    ███████████ ███████████ █████     █████|
|░░░░░   ░░░░░ ░░░░░ ░░░░░    ░░░░░░ ░░    ░░░░░░░░░░░ ░░░░░░░░░░░ ░░░░░     ░░░░░ |
'----------------------------------------------------------------------------------'
"""

logger.info(logo_ascii)
logger.info(f"TEMP_PATH: {TEMP_PATH}")
logger.info(f"LOG_PATH: {LOG_PATH}")
logger.info(f"DATABASE_URL: {DATABASE_URL}")
print(f"settings: {settings}")


@app.get("/health")
async def healthcheck():
    return {"status": True}


@app.get("/health/db")
async def healthcheck_with_db():
    status = check_db_connection()
    return {"status": status}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
