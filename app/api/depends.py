from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jwt import InvalidTokenError

from controllers.chat_controller import ChatController
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
