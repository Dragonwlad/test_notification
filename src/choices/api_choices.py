"""Module with api choices."""

from enum import Enum


class PaginationOrderChoices(str, Enum):
    """Pagination order choices."""

    asc = 'asc'
    desc = 'desc'
