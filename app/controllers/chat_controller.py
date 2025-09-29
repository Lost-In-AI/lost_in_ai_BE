from fastapi import status, HTTPException
import random
import json
import re
from typing import Optional
from uuid import uuid4
import unicodedata

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
        self._SWITCH_PATTERNS = [
            r"\bcambia( re)? (operatore|assistente|bot)\b",
            r"\bcambia (modalita|personalita)\b",
            r"\bpassami (un|una)? (operatore|agente|persona|umano)\b",
            r"\b(parla|parlare|metti(mi)?) in contatto con (un|una)? (umano|persona|operatore|agente)\b",
            r"\bvorrei parlare con (un|una)? (umano|persona|operatore|agente)\b",
            r"\bparlare con un umano\b",
            r"\bumano\b", r"\boperatore\b", r"\bagente\b"
        ]
        self.switch_first_response = [
            "Capisco che preferisci non continuare con me, ti metto subito in contatto con un altro operatore.",
            "Va bene, rispetto la tua scelta. Ti passo a un collega che potrà aiutarti.",
            "Nessun problema, ti trasferisco subito a un nuovo operatore.",
            "Capisco, non ti preoccupare. Ti metto in comunicazione con un altro operatore.",
            "Ti ringrazio comunque per il tempo, ora ti passo a un collega che continuerà ad assisterti.",
            "Va bene, interrompo qui e ti passo subito a un altro operatore."
        ]
        self.switch_second_response = [
            "Buongiorno, sono il nuovo operatore. Come posso aiutarti oggi?",
            "Ciao. Sono qui per assisterti, di cosa hai bisogno?",
            "Salve, sono il nuovo operatore che seguirà la tua richiesta. Come posso esserti utile?",
            "Buongiorno, prendo in carico ora la conversazione. Qual è la tua esigenza?",
            "Ciao, sono il nuovo operatore. Dimmi pure come posso supportarti."
        ]


    def process_chat(self, chat_request: ChatRequest) -> ChatResponse:
        try:
            session_id = chat_request.session_id if chat_request.session_id else str(uuid4())
            session_id = str(session_id)
            self.handle_session(session_id)

            user_input_message = self.handle_user_message(chat_request, session_id)

            summary = chat_request.summary if chat_request.summary else ""

            history_model = self.chat_repository.get_session_messages(session_id)

            current_bot_personality = self.handle_bot_personality(history_model)

            switch_request = None
            bot_personality = None
            if self.wants_switch(user_input_message):
                return self.handle_switch_request(current_bot_personality, session_id)

            history_message = [self._to_message(
                session_id=session_id, role=message.sender, message=message.message, personality=message.bot_personality, timestamp=message.created_at)
                for message in history_model]

            prompt = self.handle_prompt(current_bot_personality, history_message, summary, user_input_message)

            self._to_message(session_id=session_id, role='user', message=user_input_message)
            openai_response = self.openai_service.generate_response(prompt)

            try:
                parsed_output = json.loads(openai_response.output[0].content[0].text)
            except:
                parsed_output = self.parse_or_repair_payload(openai_response.output[0].content[0].text)

            bot_message, bot_split_messages = self.handle_bot_response(bot_personality if switch_request else current_bot_personality, parsed_output, session_id)

            splitted_message = None
            if switch_request:
                splitted_message = [switch_request] + bot_split_messages

            if openai_response.usage.input_tokens + openai_response.usage.output_tokens >= settings.MAX_TOKENS:
                history_message.pop(0)

            return ChatResponse(
                response_code=status.HTTP_200_OK,
                session_id=session_id,
                summary=parsed_output['summary'],
                current_responses=splitted_message if splitted_message else bot_split_messages,
                break_reason='music' if len(bot_split_messages) > 1 else None
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    def handle_switch_request(self, current_bot_personality, session_id: str) -> ChatResponse:
        bot_personality = self.flip_personality(current_bot_personality)

        switch_request = Message(
            session_id=session_id,
            sender='assistant',
            message=random.choice(self.switch_first_response),
            bot_personality=current_bot_personality,
            created_at=utc_now_isoformat()
        )
        self.chat_repository.create_message(switch_request)

        bot_response = Message(
            session_id=session_id,
            sender='assistant',
            message=random.choice(self.switch_second_response),
            bot_personality=bot_personality,
            created_at=utc_now_isoformat()
        )
        self.chat_repository.create_message(bot_response)


        switch_request_schema = self._to_message(
            session_id=session_id,
            role='assistant',
            message=random.choice(self.switch_first_response),
            personality=current_bot_personality
        )

        bot_response_schema = self._to_message(
            session_id=session_id,
            role='assistant',
            message=random.choice(self.switch_second_response),
            personality=bot_personality
        )

        return ChatResponse(
            response_code=status.HTTP_200_OK,
            session_id=session_id,
            current_responses=[switch_request_schema, bot_response_schema],
            break_reason='music'
        )

    def handle_bot_response(self, bot_personality, parsed_output, session_id: str) -> tuple[
        Message, list[Message]]:
        bot_reply = parsed_output['reply']
        bot_replies = self._handle_music_placeholders(parsed_output['reply'])
        bot_message = self._to_message(session_id=session_id, role='assistant', message=bot_reply,
                                       personality=bot_personality)
        bot_split_messages = [
            self._to_message(session_id=session_id, role='assistant', message=bot_reply, personality=bot_personality)
            for bot_reply in bot_replies]

        for message in bot_split_messages:
            message_model = Message(
                session_id=session_id,
                sender=message.sender,
                message=message.text,
                bot_personality=message.bot_personality,
                created_at=utc_now_isoformat()
            )
            self.chat_repository.create_message(message_model)
        return bot_message, bot_split_messages

    def handle_prompt(self, bot_personality, history_message: list[Message], summary: str, user_input_message: str) -> list[
        dict]:
        init_prompt = self.personality_to_prompt(bot_personality)
        prompt = prompt_builders.prepare_prompt(init_prompt, user_input_message, history_message, summary)
        return prompt

    def handle_bot_personality(self, history_model):
        bot_personality = next(
            (message.bot_personality for message in reversed(history_model) if message.sender == "assistant"),
            None
        )

        if not bot_personality:
            bot_personality = self._resolve_bot_personality()
        return bot_personality

    def handle_session(self, session_id: str):
        session_model = self.chat_repository.get_session(session_id)

        if not session_model:
            new_session_model = self.chat_repository.create_session(Session(session_id=session_id))

    def handle_user_message(self, chat_request: ChatRequest, session_id: str) -> str:
        user_input_message = chat_request.current_message
        new_message = self.chat_repository.create_message(
            Message(
                session_id=session_id,
                sender=MessageSender.USER.value,
                message=user_input_message,
                created_at=utc_now_isoformat()
            )
        )
        return user_input_message


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
    def _resolve_bot_personality(bot_personality: str = None) -> str:
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

    @staticmethod
    def _normalize_session_id(session_id: str = None) -> str:
        return session_id if session_id else str(uuid4())

    def handle_db_session(self, session_id: str, token = None) -> Session:
        if not token:
            return self.chat_repository.create_session(Session(session_id=session_id))

        user_id = token.sub
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return ChatResponse(
                response_code=status.HTTP_404_NOT_FOUND,
                message="User not found"
            )
        return self.chat_repository.create_session(Session(user_id=user.id, session_id=session_id))


    def wants_switch(self, user_text: str) -> bool:
        text = unicodedata.normalize("NFKD", user_text).encode("ascii", "ignore").decode("ascii").lower().strip()
        return any(re.search(word, text) for word in self._SWITCH_PATTERNS)


    def flip_personality(self, current: Optional[BotPersonality]) -> BotPersonality:
        if current is None:
            return random.choice(list(BotPersonality))
        return BotPersonality.INEPT if current == BotPersonality.WITTY else BotPersonality.WITTY
