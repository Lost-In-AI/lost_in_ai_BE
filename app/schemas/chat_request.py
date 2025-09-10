from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    session_id: str = Field(
        ...,
        description="Unique identifier for the chat session"
    )
    current_message: str = Field(
        ...,
        description="The latest user message to be processed by the AI chatbot"
    )
    history: Optional[list[str]] = Field(
        default=None,
        description="Optional list of the most recent N messages in the conversation"
    )
    summary: Optional[str] = Field(
        default=None,
        description="Optional condensed summary of the conversation, used to preserve context and reduce token usage"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "session_id": "12345ABC",
                    "current_message": "Ciao voglio informazioni per un mutuo"
                }
            ]
        }
    }
