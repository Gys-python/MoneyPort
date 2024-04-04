from fastapi import FastAPI
from fast_api.schemas.message_schema import FilteredMessageSchema
from fast_api.database.models import FilteredMessage
from typing import List


app = FastAPI()


@app.get("/api/get_message/", response_model=List[FilteredMessageSchema])
async def get_messages():
    messages = FilteredMessage.select()
    return [FilteredMessageSchema.from_orm(message) for message in messages]

