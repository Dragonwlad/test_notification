"""Module with service choices."""

from enum import Enum


class OperatingModeChoices(str, Enum):
    """Pagination order choices."""

    iif_mode = 'iif_mode'
    local_mode = 'local_mode'
    domain_mode = 'domain_mode'
