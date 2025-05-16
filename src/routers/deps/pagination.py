"""Module with pagination dependencies."""
from fastapi import Query

from src.choices.api_choices import PaginationOrderChoices
from src.rest_models.pagination import Pagination


def generate_pagination_query_params(
    page: int = Query(ge=1, default=1),
    per_page: int = Query(ge=1, le=1000, default=50),
    order: PaginationOrderChoices = PaginationOrderChoices.asc,
) -> Pagination:
    """
    Generate pagination query parameters for FastAPI endpoints.

    Args:
        page (int): The page number, must be 1 or higher.
        per_page (int): Number of items per page, must be between 1 and 1000.
        order (PaginationOrderChoices): The order of pagination, either ascending or descending.

    Returns:
        Pagination: An instance of the Pagination schema containing the pagination parameters.
    """
    return Pagination(page=page, per_page=per_page, order=order)
