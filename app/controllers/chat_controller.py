from datetime import datetime

from fastapi import status

from models.enums.message_sender import MessageSender
from schemas.chat_request import ChatRequest
from schemas.chat_response import ChatResponse
from schemas.message import Message
from services.openai_service import OpenAIService


class ChatController:
    def __init__(self, open_ai_service: OpenAIService):
        self.open_ai_service = open_ai_service

    def handle_test_chatbot(self, chat_request: ChatRequest) -> ChatResponse:
        current_response = Message(
            sender=MessageSender.BOT,
            text='Risposta di test... chatbot in pausa pranzo!!!',
            timestamp=datetime.now()
        )
        history = [
            Message(
                sender=MessageSender.USER,
                text="Ciao voglio informazioni per un mutuo",
                timestamp=datetime.now()
            ),
            Message(
                sender=MessageSender.BOT,
                text="Ciao di quali info hai bisogno",
                timestamp=datetime.now()
            )
        ]

        history.append(current_response)

        return ChatResponse(
            response_code=status.HTTP_200_OK,
            session_id=chat_request.session_id,
            history=history,
            summary="L'utente ha chiesto di essere messo in contatto con qualcuno.",
            current_response=current_response
        )
