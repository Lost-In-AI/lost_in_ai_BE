from fastapi import status
from datetime import datetime

from models.enums.message_sender import MessageSender
from schemas.chat_request import ChatRequest
from schemas.chat_response import ChatResponse
from schemas.message import Message
from services.openai_service import OpenAIService


class ChatController:
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service

    def new_chatbot(self, chat_request: ChatRequest) -> ChatResponse:
        current_message = chat_request.current_message

        response = self.openai_service.generate_response(current_message)

        history = self.prepare_history(current_message, response.output_text, chat_request.history)

        return ChatResponse(
            response_code=status.HTTP_200_OK,
            session_id=chat_request.session_id,
            history=history,
            summary=None,
            current_response=history[-1]
        )


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

    @staticmethod
    def prepare_history(current_message, current_response, history: list[Message] = None):
        user_message = Message(
            sender=MessageSender.USER,
            text=current_message,
            timestamp=datetime.now()
        )

        current_response = Message(
            sender=MessageSender.BOT,
            text=current_response,
            timestamp=datetime.now()
        )
        if not history:
            history = []

        history.append(user_message)
        history.append(current_response)

        return history
