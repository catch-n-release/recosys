from prefect import task
import tomli as toml
import pandas as pd
from deepchecks.tabular import Dataset
from datetime import timedelta
from omegaconf import OmegaConf
from prefect.tasks import task_input_hash


@task
def boot_config() -> type:
    try:
        with open("pyproject.toml", "rb") as stream:
            toml_dict = toml.load(stream)
        config = OmegaConf.create(toml_dict)
        return config
    except Exception as e:
        raise e


@task
def sift_success(result) -> bool:
    try:
        assert result.passed()
    except Exception as e:
        raise e


@task(
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1),
)
def boot_dc_dataset(
    data: pd.DataFrame,
    config,
):
    try:
        return Dataset(
            data,
            cat_features=list(config.ml.data.categorical_columns),
            label=config.ml.data.label,
            label_type=config.ml.data.label_type,
        )
    except Exception as e:
        raise e


@task
def boot_train_test(config: OmegaConf) -> dict:
    try:
        datasets = {
            str(config.ml.const.trainset):
            pd.read_csv(config.ml.path.trainset),
            str(config.ml.const.testset): pd.read_csv(config.ml.path.testset),
        }

        return datasets

    except Exception as e:
        raise e


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
