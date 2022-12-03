"""Router for all movies endpoint.

Attributes:
    router (FastAPI Router): Used to add movies route.
"""
from fastapi import APIRouter, status
from app.models import Movie
from typing import List
import json
from app import app_config

router = APIRouter()


@router.get("/movies", status_code=status.HTTP_200_OK)
async def movies(status=status.HTTP_200_OK) -> List[Movie]:
    """
        Functionality to get all movies.
    Args:
        status (status, optional): Staus Codes class.

    Returns:
        List[Movie]: List of Pydantic Movies
    """
    try:
        with open(app_config.app.path.metadata, "r") as meta_data_file:
            metadata = json.load(meta_data_file)
        return [
            Movie(id=i, name=movie)
            for i, movie in enumerate(metadata.get("movies"))
        ]
    except Exception as e:
        raise e
