from datetime import datetime, timedelta
from fastapi import HTTPException, status
from passlib.context import CryptContext
import jwt
from src.services.base_service import BaseService
from src.config.settings import settings
from src.rest_models.token import TokenPair, OAuth2TokenResponse
from src.db_services.users_repository import auth_repository


class AuthService(BaseService):
    """Service for authentication logic using JWT."""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def _create_tokens(self, user_id: int) -> TokenPair:
        access_payload = {
            "sub": user_id,
            "exp": datetime.now() + timedelta(seconds=settings.token.ACCESS_TOKEN_LIFETIME),
        }
        refresh_payload = {
            "sub": user_id,
            "exp": datetime.now() + timedelta(seconds=settings.token.REFRESH_TOKEN_LIFETIME),
        }
        access_token = jwt.encode(
            access_payload,
            settings.token.JWT_SECRET,
            algorithm=settings.token.ALGORITHM,
        )
        refresh_token = jwt.encode(
            refresh_payload,
            settings.token.JWT_SECRET,
            algorithm=settings.token.ALGORITHM,
        )
        return TokenPair(access=access_token, refresh=refresh_token, user_id=user_id)

    async def register_oauth2_response(self, username: str, password: str) -> OAuth2TokenResponse:
        hashed = self.hash_password(password)
        user = await self.db.create_user(username=username, hashed_password=hashed)
        return await self._as_oauth2_response(user.id)

    async def login_oauth2_response(self, username: str, password: str) -> OAuth2TokenResponse:
        user = await self.db.get_by_username(username=username)
        if not user or not self.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return await self._as_oauth2_response(user.id)

    async def refresh_oauth2_response(self, refresh_token: str) -> OAuth2TokenResponse:
        try:
            payload = jwt.decode(
                refresh_token,
                settings.token.JWT_SECRET,
                algorithms=[settings.token.ALGORITHM],
            )
            return await self._as_oauth2_response(user_id=payload["sub"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    async def _as_oauth2_response(self, user_id: int) -> OAuth2TokenResponse:
        tokens = await self._create_tokens(user_id)
        return OAuth2TokenResponse(
            access_token=tokens.access,
            refresh_token=tokens.refresh,
            token_type="bearer",
        )

    async def decode_jwt(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.token.JWT_SECRET,
                algorithms=[settings.token.ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")


auth_service = AuthService(db=auth_repository)
