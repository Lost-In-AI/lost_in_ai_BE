from fastapi import status
from datetime import datetime
import random
import json

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
        self.bot_init = prompts.CHATBOT_INIT

    def process_chat(self, chat_request: ChatRequest) -> ChatResponse:
        user_input_message = chat_request.current_message
        user_message = self._to_message('user', user_input_message)
        bot_personality = self._resolve_bot_personality(chat_request.bot_personality)

        summary = chat_request.summary if chat_request.summary else ""
        history = chat_request.history if chat_request.history else []
        prompt = prompt_builders.prepare_prompt(self.bot_init, user_input_message, history, summary)

        openai_response = self.openai_service.generate_response(prompt)

        parsed_output = json.loads(openai_response.output[0].content[0].text)
        bot_reply = parsed_output['reply']
        summary = parsed_output['summary']

        bot_message = self._to_message('assistant', bot_reply)

        history.append(user_message)
        history.append(bot_message)

        if openai_response.usage.input_tokens + openai_response.usage.output_tokens >= settings.MAX_TOKENS:
            history.pop(0)

        return ChatResponse(
            response_code=status.HTTP_200_OK,
            session_id=chat_request.session_id,
            history=history,
            summary=summary,
            current_responses=[bot_message],
            bot_personality=bot_personality
        )

    @staticmethod
    def _to_message(role: str, message: str, timestamp: datetime = None) -> Message:
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

    def mock_response(self, chat_request: ChatRequest) -> ChatResponse:
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
    def _resolve_bot_personality(bot_personality: BotPersonality = None) -> BotPersonality:
        if bot_personality is None:
            return random.choice(list(BotPersonality))

        return bot_personality.value
