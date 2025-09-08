import logging

from fastapi import APIRouter, Request, status

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_chat_list(request: Request):
    return {"status": True}
