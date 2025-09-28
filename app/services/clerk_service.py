import jwt
from jwt import PyJWKClient, InvalidTokenError
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Any, Dict, Optional
from core.configs import settings


http_bearer = HTTPBearer(auto_error=False)

class ClerkToken(BaseModel):
    sub: str
    email: Optional[str] = None
    token_payload: Dict[str, Any]


class ClerkService:
    def __init__(self):
        self.jwks_url = settings.CLERK_JWKS_URL
        self.issuer = settings.CLERK_ISSUER
        self.client = PyJWKClient(self.jwks_url)


    def verify_and_decode_token(self, token: str) -> Dict[str, Any]:
        try:
            signing_key = self.client.get_signing_key_from_jwt(token)
        except Exception as e:
            raise InvalidTokenError(f"Invalid token. Error: {e}")

        return jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"require": ["exp", "iat"]},
            issuer=self.issuer
        )
