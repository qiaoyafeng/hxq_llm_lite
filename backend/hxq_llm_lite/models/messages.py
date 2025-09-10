from datetime import datetime
from typing import Optional

from core.config import settings
from core.db import Base, get_db
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Text


class Message(Base):
    __tablename__ = settings.TABLE_MESSAGE
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Text)
    role_id = Column(Text)
    role = Column(Text)
    content = Column(Text)
    del_status = Column(Boolean, default=False)
    created_time = Column(DateTime, default=datetime.now)
    updated_time = Column(DateTime, default=datetime.now)


class MessageModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str
    role_id: str
    role: str
    content: str
    del_status: bool
    created_time: datetime
    updated_time: datetime


class MessageForm(BaseModel):
    user_id: str
    role_id: str
    role: str
    content: Optional[str] = None
    created_time: Optional[datetime] = None
    updated_time: Optional[datetime] = None


class MessageTable:
    def get_messages_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 50
    ) -> list[MessageModel]:
        with get_db() as db:
            all_messages = (
                db.query(Message)
                .filter_by(user_id=user_id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            return [MessageModel.model_validate(message) for message in all_messages]

    def insert_message(self, form_data: MessageForm) -> Optional[MessageModel]:
        with get_db() as db:
            message = {
                "user_id": form_data.user_id,
                "role_id": form_data.role_id,
                "role": form_data.role,
                "content": form_data.content,
            }

            result = Message(**message)
            db.add(result)
            db.commit()
            db.refresh(result)
            return MessageModel.model_validate(result) if result else None


Messages = MessageTable()
