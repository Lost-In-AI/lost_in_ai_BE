from pydantic import BaseModel, Field
from typing import Optional

from schemas.enums.bot_personality import BotPersonality
from schemas.message import Message


class PatchChatRequest(BaseModel):
    session_id: str = Field(
        ...,
        description="Unique identifier for the chat session"
    )
    history: Optional[list[Message]] = Field(
        default=None,
        description="Optional list of the most recent N messages in the conversation"
    )
    bot_personality: Optional[BotPersonality] = Field(
        default=BotPersonality.WITTY,
        description="The bot's personality"
    )

    model_config = {
        "json_schema_extra": {
            "example":
                {
                "session_id": "12345ABC",
                "history": [
                    {
                        "sender": "user",
                        "text": "Ciao voglio informazioni per un mutuo",
                        "timestamp": "2025-09-05T15:02:00Z",
                    },
                    {
                        "sender": "assistant",
                        "text": "L'agente umano è occupato al momento. Posso aiutarle con qualcosa di diverso?",
                        "timestamp": "2025-09-05T15:02:00Z",
                    },
                    {
                        "sender": "user",
                        "text": "Ciao voglio informazioni per un mutuo",
                        "timestamp": "2025-09-05T15:02:00Z",
                    }
                ],
                "chat_personality": "witty"
            }
        }
    }
