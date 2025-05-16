from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.services.auth_service import auth_service  # тебе нужно реализовать

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = await auth_service.decode_jwt(token)
    return payload['sub']
