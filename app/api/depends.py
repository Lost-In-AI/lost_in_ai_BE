from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from sqlmodel import Session
from typing import Generator


from controllers.chat_controller import ChatController
from controllers.user_controller import UserController
from controllers.webhook_controller import WebhookController
from repositories.user_repository import UserRepository
from services.database import engine
from services.openai_service import OpenAIService

from services.clerk_service import ClerkToken, http_bearer, ClerkService


def get_openai_service() -> OpenAIService:
    return OpenAIService()


def get_chat_controller() -> ChatController:
    return ChatController(get_openai_service())


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> ClerkToken:
    try:
        auth_service = ClerkService()
        token = credentials.credentials
        try:
            claims = auth_service.verify_and_decode_token(token)
            print(claims)
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token non valido: {e}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Accesso negato: {e}")

        email = claims.get("email") or claims.get("user_email")

        return ClerkToken(
            sub=claims.get("sub"),
            email=email,
            token_payload=claims,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Accesso negato: {e}")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as db:
        yield db


def get_user_repository(db: Session) -> UserRepository:
    return UserRepository(db)


def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    user_repository: UserRepository = get_user_repository(db)
    return UserController(user_repository)


def get_webhook_controller(db: Session = Depends(get_db)) -> WebhookController:
    user_controller = get_user_controller(db)
    return WebhookController(user_controller)
