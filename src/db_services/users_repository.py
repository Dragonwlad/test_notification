from typing import Optional
from fastapi import HTTPException, status
from src.models.user import User


class AuthRepository:
    async def get_by_id(self, user_id: int) -> User:
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def get_by_username(self, username: str) -> Optional[User]:
        return await User.get_or_none(username=username)

    async def create_user(self, username: str, hashed_password: str) -> User:
        try:
            return await User.create(username=username, password=hashed_password)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


auth_repository = AuthRepository()
