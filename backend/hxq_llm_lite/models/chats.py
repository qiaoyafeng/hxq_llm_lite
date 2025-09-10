from core.config import settings
from pydantic import BaseModel


class ChatRequest(BaseModel):
    model: str = settings.DEFAULT_LLM_MODEL
    user_id: str
    role_id: str
    content: str
    think: bool = False
    stream: bool = False
