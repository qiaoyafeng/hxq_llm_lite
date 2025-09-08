import logging

from fastapi import APIRouter

log = logging.getLogger(__name__)

router = APIRouter()


###########################
# GetModels
###########################


@router.get(
    "/",
)
async def get_models():
    return {"models": list()}
