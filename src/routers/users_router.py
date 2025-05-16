from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.rest_models.token import OAuth2TokenResponse
from src.rest_models.user import RegisterRequest
from src.services.auth_service import auth_service

user_router = APIRouter(prefix="/auth", tags=["auth"])


@user_router.post("/register", response_model=OAuth2TokenResponse)
async def register_user(data: RegisterRequest):
    """Register a new user."""
    return await auth_service.register_oauth2_response(data.username, data.password)


@user_router.post("/login", response_model=OAuth2TokenResponse)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2-compatible login.
    Requires `username`, `password` (form fields) and returns `access_token`, `token_type`.
    """
    if form_data.grant_type and form_data.grant_type != "password":
        raise HTTPException(status_code=400, detail="Only grant_type=password is supported")
    return await auth_service.login_oauth2_response(form_data.username, form_data.password)



@user_router.post("/refresh", response_model=OAuth2TokenResponse)
async def refresh_token(refresh_token: str):
    """Refresh access token."""
    return await auth_service.refresh_oauth2_response(refresh_token)
