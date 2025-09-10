import json

import requests
from constants import (
    DEFAULT_SYS_MESSAGE,
    HXQ_DEFAULT_ROLE_NAME,
    HXQ_ROLES,
    SUCCESS_CODE,
    Role,
)
from core.config import settings
from core.log import logger
from fastapi import APIRouter, status
from models.chats import ChatRequest
from models.messages import MessageForm, Messages
from utils.common import build_resp, safe_int

##########################################
#
# API routes
#
##########################################

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def create_chat(chat_request: ChatRequest):
    Messages.insert_message(
        MessageForm(
            user_id=chat_request.user_id,
            role_id=chat_request.role_id,
            role=Role.USER,
            content=chat_request.content,
        )
    )
    message_list = Messages.get_messages_by_user_id(chat_request.user_id)
    messages = [
        {
            "role": "system",
            "content": DEFAULT_SYS_MESSAGE.format(
                role_name=HXQ_ROLES.get(
                    safe_int(chat_request.role_id), HXQ_DEFAULT_ROLE_NAME
                )
            ),
        }
    ]
    for message in message_list:
        if not message.del_status:
            role = message.role
            content = message.content if message.content else ""
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": chat_request.content})
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": chat_request.model,
        "messages": messages,
        "think": chat_request.think,
        "stream": chat_request.stream,
    }

    try:
        response = requests.post(
            f"{settings.OLLAMA_HOST}/api/chat",
            headers=headers,
            data=json.dumps(payload),
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        content = data["message"]["content"]
    except Exception as e:
        logger.error(f"请求失败: {e}")
        content = ""
    Messages.insert_message(
        MessageForm(
            user_id=chat_request.user_id,
            role_id=chat_request.role_id,
            role=Role.ASSISTANT,
            content=content,
        )
    )
    res_data = {"content": content}
    return build_resp(SUCCESS_CODE, res_data)
