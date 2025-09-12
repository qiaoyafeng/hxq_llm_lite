import uvicorn as uvicorn
from core.config import LOG_PATH, TEMP_PATH, settings
from core.db import DATABASE_URL, check_db_connection
from core.log import logger
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from routers import chats
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

app = FastAPI(
    title="好心情-LLM",
    summary="好心情-LLM",
    docs_url=None,
    redoc_url=None,
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


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/js/swagger-ui-bundle.js",
        swagger_css_url="/static/js/swagger-ui.css",
    )


@app.get("/health")
async def healthcheck():
    return {"status": True}


@app.get("/health/db")
async def healthcheck_with_db():
    status = check_db_connection()
    return {"status": status}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
