from core.config import settings
from pydantic import BaseModel


class ChatRequest(BaseModel):
    model: str = settings.DEFAULT_LLM_MODEL
    user_id: str = "10000"
    role_id: str = "630020"
    content: str = "你好"
    think: bool = False
    stream: bool = False
