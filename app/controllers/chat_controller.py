from fastapi import status, HTTPException
import random
import json
import re
from typing import Optional
from uuid import uuid4

from core.configs import settings
from utils import utc_now_isoformat

from exceptions.chat_exception import BotResponseParsingError, PlaceholdersParsingError

from models.message import Message
from models.session import Session

from schemas.enums.bot_personality import BotPersonality
from schemas.enums.message_sender import MessageSender
from schemas.message import Message as MessageSchema
from schemas.chat_request import ChatRequest
from schemas.chat_response import ChatResponse
from schemas.patch_chat_request import PatchChatRequest
from schemas.patch_chat_response import PatchChatResponse

from services.clerk_service import ClerkToken
from services.openai_service import OpenAIService
from services import prompt_builders, prompts

from repositories.user_repository import UserRepository
from repositories.chat_repository import ChatRepository


class ChatController:
    def __init__(self, openai_service: OpenAIService, user_repository: UserRepository, chat_repository: ChatRepository):
        self.openai_service = openai_service
        self.user_repository = user_repository
        self.chat_repository = chat_repository
        self.MUSIC_REGEX = r"\[HOLD_MUSIC.*?\].*?\[/HOLD_MUSIC\]"

    def process_chat(self, chat_request: ChatRequest, token: ClerkToken = None) -> ChatResponse:
        try:
            user_input_message = chat_request.current_message
            summary = chat_request.summary if chat_request.summary else ""
            session_id = str(chat_request.session_id) if str(chat_request.session_id) else str(uuid4())

            bot_personality = self._resolve_bot_personality(chat_request.bot_personality)
            init_prompt = self.personality_to_prompt(bot_personality)

            if token:
                user_id = token.sub
                user = self.user_repository.get_user_by_id(user_id)
                if not user:
                    return ChatResponse(
                        response_code=status.HTTP_404_NOT_FOUND,
                        message="User not found"
                    )

                if str(chat_request.session_id) and str(chat_request.session_id) != session_id:
                    session = self.chat_repository.create_session(Session(user_id=user.id, session_id=session_id))

            else:
                if str(chat_request.session_id) and str(chat_request.session_id) != session_id:
                    session = self.chat_repository.create_session(Session(session_id=session_id))

            new_message = self.chat_repository.create_message(
                Message(
                    session_id=session_id,
                    sender=MessageSender.USER.value,
                    message=user_input_message,
                    created_at=utc_now_isoformat()
                )
            )

            history = self.chat_repository.get_session_messages(session_id)
            history_message = [self._to_message(session_id=session_id, role=message.sender, message=message.message, personality=message.bot_personality, timestamp=message.created_at) for message in history]

            prompt = prompt_builders.prepare_prompt(init_prompt, user_input_message, history_message, summary)

            user_message = self._to_message(session_id=session_id, role='user', message=user_input_message)
            openai_response = self.openai_service.generate_response(prompt)

            try:
                parsed_output = json.loads(openai_response.output[0].content[0].text)
            except:
                parsed_output = self.parse_or_repair_payload(openai_response.output[0].content[0].text)

            bot_reply = parsed_output['reply']
            summary = parsed_output['summary']

            bot_replies = self._handle_music_placeholders(bot_reply)
            bot_message = self._to_message(session_id=session_id, role='assistant', message=bot_reply, personality=bot_personality)
            bot_split_messages = [self._to_message(session_id=session_id, role='assistant', message=bot_reply, personality=bot_personality) for bot_reply in bot_replies]

            for message in bot_split_messages:
                message_model = Message(
                    session_id=session_id,
                    sender=message.sender,
                    message=message.text,
                    created_at=utc_now_isoformat()
                )
                self.chat_repository.create_message(message_model)

            history_message.append(user_message)
            history_message.append(bot_message)

            if openai_response.usage.input_tokens + openai_response.usage.output_tokens >= settings.MAX_TOKENS:
                history_message.pop(0)

            music = 'music' if len(bot_split_messages) > 1 else None

            return ChatResponse(
                response_code=status.HTTP_200_OK,
                session_id=str(session_id),
                history=history_message,
                summary=summary,
                current_responses=bot_split_messages,
                bot_personality=bot_personality,
                break_reason=music if music else None
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def patch_chat(self, patch_request: PatchChatRequest) -> PatchChatResponse:
        return PatchChatResponse(
            response_code=status.HTTP_200_OK,
            session_id=patch_request.session_id,
            bot_personality=patch_request.bot_personality
        )


    @staticmethod
    def _to_message(session_id: str, role: str, message: str, personality: BotPersonality = None, timestamp: Optional[str] = None) -> MessageSchema:
        bot_personality = None
        if role == "user":
            role = 'user'
        elif role == "assistant":
            role = "assistant"
            bot_personality = personality if personality else None
        else:
            role = "system"

        return MessageSchema(
            sender=role,
            session_id=session_id,
            text=message,
            timestamp=utc_now_isoformat() if not timestamp else timestamp,
            bot_personality=bot_personality
        )

    def _handle_music_placeholders(self, bot_reply: str):
        try:
            return [
                part.strip()
                for part in re.split(self.MUSIC_REGEX, bot_reply, flags=re.DOTALL)
                if part.strip()
            ]
        except Exception as e:
            raise PlaceholdersParsingError(str(e))

    @staticmethod
    def mock_response(chat_request: ChatRequest) -> ChatResponse:
        current_response = Message(
            sender=MessageSender.ASSISTANT,
            text='Risposta di test... chatbot in pausa pranzo!!!',
            timestamp=utc_now_isoformat()
        )
        history = [
            Message(
                sender=MessageSender.USER,
                text="Ciao voglio informazioni per un mutuo",
                timestamp=utc_now_isoformat()
            ),
            Message(
                sender=MessageSender.ASSISTANT,
                text="Ciao di quali info hai bisogno",
                timestamp=utc_now_isoformat()
            )
        ]

        history.append(current_response)

        return ChatResponse(
            response_code=status.HTTP_200_OK,
            session_id=chat_request.session_id,
            history=history,
            summary="L'utente ha chiesto di essere messo in contatto con qualcuno.",
            current_responses=[current_response]
        )

    @staticmethod
    def _resolve_bot_personality(bot_personality: BotPersonality= None) -> str:
        if bot_personality is None:
            return random.choice(list(BotPersonality))

        return bot_personality.value
    
    @staticmethod
    def personality_to_prompt(bot_personality: BotPersonality) -> str:
        if bot_personality == BotPersonality.WITTY:
            return prompts.CHATBOT_INIT_WITTY
        else:
            return prompts.CHATBOT_INIT_INEPT
            

    @staticmethod
    def parse_or_repair_payload(raw_text: str, previous_summary: str = "") -> dict:
        try:
            s = (raw_text or "").strip()
            if not s:
                raise HTTPException(status_code=502, detail="Empty response from AI")

            if s.startswith('"') and s.endswith('"') and len(s) >= 2:
                return {"reply": s[1:-1], "summary": previous_summary or ""}

            return {"reply": s, "summary": previous_summary or ""}
        except Exception as e:
            raise BotResponseParsingError(str(e))
