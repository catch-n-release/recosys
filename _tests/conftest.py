"""Pytest fixtures used throughout testing.
"""
import pytest
import httpx
import asyncio
import pytest_asyncio
from asgi_lifespan import LifespanManager
import pandas as pd
from deepchecks.tabular.dataset import Dataset
import tomli as toml
from omegaconf import OmegaConf
import pathlib


@pytest.fixture(scope="session")
def app_config():
    """Fixture for getting app config.

    Returns:
        Setting: Settings object
    """
    try:
        with open("pyproject.toml", "rb") as stream:
            toml_dict = toml.load(stream)
        config = OmegaConf.create(toml_dict)
        return config
    except Exception as e:
        raise e


@pytest.fixture(scope="session")
def metadata(app_config):
    """Fixture for getting movies and users metadata.

    Args:
        app_config (fixture): fixture for getting app config.

    Returns:
        dict: users and movies metadata in dict format.
    """
    import json

    with open(app_config.app.path.metadata, "r") as meta_data_file:
        return json.load(meta_data_file)


@pytest.fixture(scope="session")
def users_ids(metadata):
    """Summary

    Args:
        metadata (TYPE): Description

    Returns:
        TYPE: Description
    """
    return metadata.get("users")


@pytest.fixture(scope="session")
def movies(metadata):
    """Summary

    Args:
        metadata (TYPE): Description

    Returns:
        TYPE: Description
    """
    return metadata.get("movies")


@pytest.fixture(scope="function")
def random_user_id(users_ids):
    """Summary

    Args:
        users_ids (TYPE): Description

    Returns:
        TYPE: Description
    """
    import random as rn

    return int(rn.choice(users_ids))


@pytest.fixture(scope="session")
def dataframe():
    """Summary

    Returns:
        TYPE: Description
    """
    csv_path = "data/movie_log_25k_half.csv"
    return pd.read_csv(csv_path)


@pytest.fixture(scope="session")
def clean_df(dataframe):
    """Fixture for preprocessed dataframe.

    Args:
        dataframe (fixture): raw dataframe.

    Returns:
        pd.Dataframe: clean dataframe.
    """
    processed_df = dataframe.drop(columns=[
        "Unnamed: 0",
        "movie_year",
        "timestamp",
        "event",
        "request",
    ])
    return processed_df


@pytest.fixture(scope="session")
def deepcheck_dataset(dataframe):
    """Summary

    Args:
        dataframe (TYPE): Description

    Returns:
        TYPE: Description
    """
    dc_dataset = Dataset(
        dataframe,
        cat_features=["movie_name", "movie_year"],
        datetime_name="timestamp",
        index_name="Unnamed: 0",
        label="movie_rating",
        label_type="regression",
    )
    return dc_dataset


@pytest.fixture(scope="session")
def train_test_data(clean_df):
    """Summary

    Args:
        clean_df (TYPE): Description

    Returns:
        TYPE: Description
    """
    dc_dataset = Dataset(
        clean_df,
        cat_features=["movie_name"],
        label="movie_rating",
        label_type="regression",
    )
    return dc_dataset.train_test_split()


@pytest.fixture(scope="session",
                params=[
                    "app/recommenders/legacy/rec_model_BaseLine_v1.surp",
                    "app/recommenders/legacy/rec_model_SVD_v1.surp",
                ])
def predictor_paths(request):
    """Summary

    Args:
        request (TYPE): Description

    Returns:
        TYPE: Description
    """
    return request.param


@pytest.fixture(scope="session")
def predictor(predictor_paths):
    """Summary

    Args:
        predictor_paths (TYPE): Description

    Returns:
        TYPE: Description
    """
    from surprise import dump
    from utils.testing import DeepchecksModelWrapper

    _, surp_model = dump.load(predictor_paths)
    return DeepchecksModelWrapper(surp_model), surp_model


@pytest.fixture(scope="session")
def event_loop():
    """Summary

    Yields:
        TYPE: Description
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client():
    """Summary

    Yields:
        TYPE: Description
    """
    from app.app import app
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app,
                                     base_url="http://app.io") as client:
            yield client


def pytest_collection_modifyitems(config, items):
    rootdir = pathlib.Path(config.rootdir)
    for item in items:
        rel_path = pathlib.Path(item.fspath).relative_to(rootdir)
        mark_name = rel_path.parts[2].split("_")[1]
        if mark_name:
            mark = getattr(pytest.mark, mark_name)
            item.add_marker(mark)
