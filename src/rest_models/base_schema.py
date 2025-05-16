"""Module with base schema."""
from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base pydantic model."""

    class Config:
        """Model config."""

        from_attributes = True
        orm_mode = True
