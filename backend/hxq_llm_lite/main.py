import uvicorn as uvicorn
from core.db import check_db_connection
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


@app.get("/health")
async def healthcheck():
    return {"status": True}


@app.get("/health/db")
async def healthcheck_with_db():
    status = check_db_connection()
    return {"status": status}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=32110)
