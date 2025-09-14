from controllers.chat_controller import ChatController
from services.openai_service import OpenAIService


def get_openai_service() -> OpenAIService:
    return OpenAIService()


def get_chat_controller() -> ChatController:
    return ChatController(get_openai_service())
