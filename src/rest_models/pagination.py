"""Module with pagination schemas."""

from typing import Optional

from src.choices.api_choices import PaginationOrderChoices
from src.rest_models.base_schema import BaseSchema


class Pagination(BaseSchema):
    """Model with pagination schema."""

    page: int
    per_page: int
    order: PaginationOrderChoices = PaginationOrderChoices.asc

    @property
    def offset(self) -> Optional[int]:
        """
        Get offset.

        Returns:
            int: offset.
        """
        return (self.page - 1) * self.per_page if self.page != 1 else None


class PaginationOut(BaseSchema):
    """Model with base pagination schema out."""

    total: int
    count: int
    page: int
    pages: int
