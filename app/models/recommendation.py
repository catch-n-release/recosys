"""Pydantic Model for Recommendations.
"""
from pydantic import BaseModel
from typing import List, Tuple
from surprise import AlgoBase, dump
import json
from fastapi import HTTPException, status
from omegaconf import OmegaConf

from app import log, app_config


class RecommendationInput(BaseModel):
    """Pydantic Model for input to Recommendation.
    """

    user_id: int


class RecommendationOuput(BaseModel):
    """Pydantic Model for output from Recommendation.
    """

    movies: List[str]


class MovieRecommender:
    """Class for Movie Recommender

            1. predictor: Trained Surprise Algobase object.
            2. movies: List of movies predictor is trained on.
            3. users: List of users predictor is trained on.
    """
    predictor: AlgoBase
    settings: OmegaConf = app_config
    movies: List[str]
    users: List[str]

    def load_recommender(self):
        """Method loads Surprise model.
        """

        try:
            predictor_path = self.settings.app.path.recommender
            loaded_predictor: Tuple[List[str],
                                    AlgoBase] = dump.load(predictor_path)
            _, self.predictor = loaded_predictor
            with open(self.settings.app.path.metadata, "r") as f:
                load_metadata = json.loads(f.read())
            self.movies = load_metadata["movies"]
            self.users = load_metadata["users"]
        except Exception as e:
            raise e

    async def recommend(
        self,
        user_id: int,
    ) -> RecommendationOuput:
        """Method uses predictors predict function to get ratings for a particular user on all movies. Top 20 of these movies are returned.

        Args:
            user_id (RecommendationInput): User ID from request.

        Returns:
            RecommendationOuput: List of movie recommendations.

        Raises:
            RuntimeError: Issues with model or metadata.
        """

        try:
            log.info(f"{user_id}")
            if not self.predictor or not self.movies:
                raise RuntimeError("Recommeder not loaded correctly.")
            if user_id not in self.users:
                raise RuntimeError("User ID not available in IDs list.")
            log.info("Running Preds.....")
            predictions = [
                self.predictor.predict(
                    user_id,
                    movie,
                    r_ui=4,
                    verbose=False,
                ) for movie in self.movies
            ]
            log.info("Got Preds.....")
            predictions = sorted(predictions,
                                 key=lambda z: z.est,
                                 reverse=True)

            return RecommendationOuput(
                movies=[pred.iid for pred in predictions][:20])
        except Exception as e:
            raise HTTPException(detail=str(e),
                                status_code=status.HTTP_400_BAD_REQUEST)
