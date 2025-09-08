import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from routers import chats

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=32110)
