from fastapi import status
from datetime import datetime
import random

from schemas.enums.bot_personality import BotPersonality
from schemas.enums.message_sender import MessageSender
from schemas.chat_request import ChatRequest
from schemas.chat_response import ChatResponse
from schemas.message import Message
from services.openai_service import OpenAIService
from services import prompt_builders, prompts
from core.configs import settings


class ChatController:
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service
        self.MAX_TOKENS = settings.MAX_TOKENS
        self.bot_init = prompts.CHATBOT_INIT

    def new_chatbot(self, chat_request: ChatRequest) -> ChatResponse:
        current_message = chat_request.current_message
        user_message = self.get_message_from_request_message('user', current_message)
        bot_personality = self.get_bot_personality(chat_request.bot_personality)

        summary = chat_request.summary if chat_request.summary else ""
        history = chat_request.history if chat_request.history else []
        prompt = prompt_builders.prepare_prompt(self.bot_init, current_message, history, summary)

        response = self.openai_service.generate_response(prompt)


        current_response = response.output[0].content[0].text
        current_response_message = self.get_message_from_request_message('assistant', current_response)

        history.append(user_message)
        history.append(current_response_message)

        if response.usage.input_tokens + response.usage.output_tokens >= self.MAX_TOKENS:
            history.pop(0)

        return ChatResponse(
            response_code=status.HTTP_200_OK,
            session_id=chat_request.session_id,
            history=history,
            summary=summary if summary else None,
            current_responses=[current_response_message],
            bot_personality=bot_personality
        )

    @staticmethod
    def get_message_from_request_message(role: str, message: str, timestamp: datetime = None) -> Message:
        if role == "user":
            role = MessageSender.USER
        elif role == "assistant":
            role = MessageSender.ASSISTANT
        else:
            role = MessageSender.SYSTEM

        return Message(
            sender=role,
            text=message,
            timestamp=datetime.now() if not timestamp else timestamp
        )

    # TODO
    def handle_summary(self, history: list[Message], summary: str = None) -> str:
        history_message = [{sender, message} for sender, message in history]
        summary_prompt = self.openai_service.summary_builder(history_message, summary)
        response = self.openai_service.generate_response(prompt=summary_prompt)

        return response.output_text

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
    def get_bot_personality(bot_personality: BotPersonality = None) -> BotPersonality:
        if bot_personality is None:
            return random.choice(list(BotPersonality))

        return bot_personality.value
