from prefect import flow, task
from surprise import Dataset, SVD, Reader, accuracy, AlgoBase, dump
import pandas as pd
from omegaconf import OmegaConf

from ml.utils import boot_train_test, boot_config
from ml import log


@task
def surprise_dataset(
    config,
    dataset: pd.DataFrame,
) -> Dataset:
    try:

        dataset = Dataset.load_from_df(
            dataset[list(config.ml.data.columns)],
            Reader(rating_scale=tuple(config.ml.data.rating_scale)),
        )
        return dataset
    except Exception as e:
        raise e


@task
def train_predictor(trainset: Dataset) -> AlgoBase:
    try:
        predictor = SVD(
            n_factors=100,
            biased=True,
            random_state=15,
            verbose=True,
        )
        predictor.fit(trainset.build_full_trainset())
        return predictor
    except Exception as e:
        raise e


@task
def test_predictions(
    testset: Dataset,
    predictor: AlgoBase,
) -> list:
    try:
        return predictor.test(testset.build_full_trainset().build_testset())
    except Exception as e:
        raise e


@task
def sift_predictor(predictions) -> float:
    try:
        rmse = accuracy.rmse(predictions)
        mae = accuracy.mae(predictions)
        log.info(f"RMSE : {rmse}")
        log.info(f"MAE : {mae}")
    except Exception as e:
        raise e


@task
def save_predictor(
    config: OmegaConf,
    predictor: AlgoBase,
):
    try:
        dump.dump(
            config.ml.path.predictor,
            algo=predictor,
        )
        # dump.dump(
        #     config.ml.path.recommender,
        #     algo=predictor,
        # )
    except Exception as e:
        raise e


@flow
def train():
    try:
        config = boot_config()
        datasets = boot_train_test(config)
        trainset = surprise_dataset(
            config,
            datasets.get(config.ml.const.trainset),
        )
        testset = surprise_dataset(
            config,
            datasets.get(config.ml.const.testset),
        )
        predictor = train_predictor(trainset)
        predictions = test_predictions(testset, predictor)
        sift_predictor(predictions)
        save_predictor(config, predictor)

    except Exception as e:
        raise e


if __name__ == "__main__":
    train()
