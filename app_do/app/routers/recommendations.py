from fastapi import APIRouter, status, Depends, Response
from app.models import RecommendationOuput
from app import movie_recommender, log

router = APIRouter()


@router.get("/recommend/{user_id}", status_code=status.HTTP_200_OK)
async def recommend(
    recommendations: RecommendationOuput = Depends(
        movie_recommender.recommend),
) -> RecommendationOuput:

    return recommendations
