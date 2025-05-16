from pydantic import BaseModel


class TokenPair(BaseModel):
    access: str
    refresh: str
    user_id: int


class OAuth2TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str
