"""Router for all movies endpoint.

Attributes:
    outer (FastAPI Router): Used to add users route.
"""
from fastapi import APIRouter, status
from app.models import User
from typing import List
import json
from app import app_config

router = APIRouter()


@router.get("/users", status_code=status.HTTP_200_OK)
async def users() -> List[User]:
    """
    Functionality to get all users.

    Returns:
        List[User]: List of Pydantic User models.
    """
    with open(app_config.app.path.metadata, "r") as meta_data_file:
        metadata = json.load(meta_data_file)
    return [User(id=int(z)) for z in metadata.get("users")]
