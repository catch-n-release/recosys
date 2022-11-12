"""Tests for Pydantic Models.
"""
import pytest

from app.models import (
    User,
    Movie,
    RecommendationInput,
    RecommendationOuput,
    MovieRecommender,
)


def test_user(random_user_id):
    """Test for User model.

    Args:
        random_user_id (fixture): Random user id.
    """
    user = User(id=int(random_user_id))
    assert user.id == int(random_user_id)


def test_movie():
    """Test for Movie model.
    """
    movie = Movie(id=123, name="sxfdsv", year=1123, rating=2)
    assert movie.id == 123
    assert movie.name == "sxfdsv"
    assert movie.year == 1123
    assert movie.rating == 2


def test_recommendation_input(random_user_id):
    """Test for RecommendationInput model.

    Args:
        random_user_id (fixture): Random user id.
    """
    reco_in = RecommendationInput(user_id=int(random_user_id))
    assert reco_in.user_id == int(random_user_id)


def test_recommendation_ouput(movies):
    """Test for RecommendationOutput.

    Args:
        faker (fixture): Faker fixture.
    """
    recommendation = RecommendationOuput(
        movies=[movie for movie in movies[:10]])
    assert len(recommendation.movies) == 10


@pytest.mark.asyncio
async def test_movie_recommender(predictor, random_user_id):
    """Summary

    Args:
        predictor (fixture): Surprise Model
        random_user_id (fixture): Random User ID
    """
    movie_recommender = MovieRecommender()
    movie_recommender.load_recommender()
    recommendation = await movie_recommender.recommend(user_id=random_user_id)
    assert len(recommendation.movies) == 20
