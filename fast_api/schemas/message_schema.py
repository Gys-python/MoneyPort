from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class FilteredMessageSchema(BaseModel):
    message_id: int = Field(..., description="The ID of the message")
    date: datetime = Field(default_factory=datetime.now, description="The date and time the message was created")
    username: Optional[str] = Field(None, description="The username of the message sender")
    first_name: Optional[str] = Field(None, description="The first name of the message sender")
    last_name: Optional[str] = Field(None, description="The last name of the message sender")
    text: str = Field(..., description="The text content of the message")
    answers: Optional[str] = Field(None, description="Serialized JSON containing answers to the message")

    class Config:
        from_attributes = True  # Обновленная конфигурация для Pydantic версии 2 и выше
