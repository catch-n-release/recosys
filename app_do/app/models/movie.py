"""Pydatic Movie models used in application.
"""
from pydantic import BaseModel
from typing import Optional


class Movie(BaseModel):
    """Movie Pydantic Model."""

    id: int
    name: str
    year: Optional[int]
    rating: Optional[int]
