"""Summary
"""
from surprise import Reader, Dataset as SurpDataset
import pandas as pd
import numpy as np


class DeepchecksModelWrapper:
    """Summary

    Attributes:
        model (TYPE): Description
    """

    def __init__(self, surp_model):
        """Summary

        Args:
            surp_model (TYPE): Description
        """

        try:
            self.model = surp_model
        except Exception as e:
            raise e

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Summary

        Args:
            data (pd.DataFrame): Description

        Returns:
            np.ndarray: Description
        """
        try:
            reader = Reader(rating_scale=(1, 5))

            data["movie_rating"] = pd.Series([0] * data.shape[0])
            surp_data = SurpDataset.load_from_df(
                data[["user_id", "movie_name", "movie_rating"]], reader)
            surp_test_data = surp_data.build_full_trainset().build_testset()

            predictions = self.model.test(surp_test_data)
            return np.array([pred.est for pred in predictions])
        except Exception as e:
            raise e

    def predict_proba(self, data: pd.DataFrame) -> np.ndarray:
        """Summary

        Args:
            data (pd.DataFrame): Description
        """
        raise NotImplementedError()

    @property
    def feature_importances_(self) -> pd.Series:  # optional
        """Summary"""
        raise NotImplementedError()
