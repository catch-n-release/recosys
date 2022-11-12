"""Test for all FastAPI routers.
"""
import pytest
import httpx
from fastapi import status
from typing import List


@pytest.mark.asyncio
async def test_recommend(client: httpx.AsyncClient, random_user_id):
    """Test for recommendation API.

    Args:
        client (httpx.AsyncClient): client to send HTTP requests.
        random_user_id (int): User ID to get recommendations.
    """
    response = await client.get(f"/recommend/{random_user_id}")
    json_response = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert [*json_response][0] == "movies"
    assert len(*json_response.values()) == 20


@pytest.mark.asyncio
async def test_movies(client: httpx.AsyncClient):
    """Test for movies API.

    Args:
        client (httpx.AsyncClient): client to send HTTP requests.
    """
    response = await client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), List)


@pytest.mark.asyncio
async def test_users(client: httpx.AsyncClient):
    """Test for users API.

    Args:
        client (httpx.AsyncClient): client to send HTTP requests.
    """
    response = await client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), List)


@pytest.mark.asyncio
async def test_data_integrity_check(client):
    """Test for data integrity check API.

    Args:
        client (httpx.AsyncClient): client to send HTTP requests.
    """
    response = await client.get("/data_integrity_check")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_train_test_check(client):
    """Test for train test split check API.

    Args:
        client (httpx.AsyncClient): client to send HTTP requests.
    """
    response = await client.get("/train_test_check")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_predictor_check(client):
    """Test for model evalution check API.

    Args:
        client (httpx.AsyncClient): client to send HTTP requests.
    """
    response = await client.get("/predictor_check")

    assert response.status_code == 200
