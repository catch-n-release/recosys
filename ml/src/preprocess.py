from prefect import task, flow
import pandas as pd
from omegaconf import OmegaConf

from utils import boot_config
from src import boot_dataframe


@task(retries=3, retry_delay_seconds=5)
def ingress() -> pd.DataFrame:
    try:
        raise NotImplementedError
    except Exception as e:
        raise e


@task
def filter_columns(
    config: OmegaConf,
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    try:
        columns = list(config.ml.data.columns)
        return dataset[columns]
    except Exception as e:
        raise e


@task
def save_processed_dataset(
    config: OmegaConf,
    dataset: pd.DataFrame,
):
    try:
        dataset.to_csv(config.ml.path.processed_dataset)
    except Exception as e:
        raise e


@flow
def preprocess_dataset():
    try:
        config = boot_config()
        dataset = boot_dataframe(config)
        dataset = filter_columns(config, dataset)
        save_processed_dataset(config, dataset)
    except Exception as e:
        raise e


if __name__ == "__main__":
    preprocess_dataset()
