# from settings import Settings

# app_config = Settings()

from utils import app_config, log

from app.models import MovieRecommender

movie_recommender = MovieRecommender()

from utils import DeepchecksModelWrapper
