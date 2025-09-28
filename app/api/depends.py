from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from sqlmodel import Session as SQLSession
from typing import Generator, Optional


from controllers.chat_controller import ChatController
from controllers.user_controller import UserController
from controllers.webhook_controller import WebhookController

from repositories.chat_repository import ChatRepository
from repositories.user_repository import UserRepository

from services.database import engine
from services.openai_service import OpenAIService
from services.clerk_service import ClerkToken, http_bearer, ClerkService


def get_openai_service() -> OpenAIService:
    return OpenAIService()


def get_db() -> Generator[SQLSession, None, None]:
    with SQLSession(engine) as db:
        yield db


def get_user_repository(db: SQLSession) -> UserRepository:
    return UserRepository(db)


def get_chat_repository(db: SQLSession) -> ChatRepository:
    return ChatRepository(db)


def get_chat_controller(db: SQLSession = Depends(get_db)) -> ChatController:
    openai_service: OpenAIService = get_openai_service()
    user_repository: UserRepository = get_user_repository(db)
    chat_repository: ChatRepository = get_chat_repository(db)
    return ChatController(openai_service, user_repository, chat_repository)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
) -> Optional[ClerkToken]:
    if credentials is None or not credentials.credentials:
        return None

    token = credentials.credentials
    try:
        auth_service = ClerkService()
        claims = auth_service.verify_and_decode_token(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token not valid: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: {e}",
        )

    email = claims.get("email") or claims.get("user_email")
    return ClerkToken(sub=claims.get("sub"), email=email, token_payload=claims)


def get_user_controller(db: SQLSession = Depends(get_db)) -> UserController:
    user_repository: UserRepository = get_user_repository(db)
    return UserController(user_repository)


def get_webhook_controller(db: SQLSession = Depends(get_db)) -> WebhookController:
    user_controller = get_user_controller(db)
    return WebhookController(user_controller)
