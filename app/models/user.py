"""Pydatic User models used in application.
"""
from pydantic import BaseModel


class User(BaseModel):
    """Pydantic User model."""

    id: int
