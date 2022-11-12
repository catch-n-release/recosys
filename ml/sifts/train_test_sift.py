from prefect import flow, task
from datetime import timedelta
from prefect.tasks import task_input_hash
from deepchecks.tabular import Dataset
from deepchecks.tabular.suites import train_test_validation
import pandas as pd

from utils import boot_config, sift_success, boot_dc_dataset
from ml import log


@task(
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1),
)
def boot_processed_dataframe(config: type) -> pd.DataFrame:
    try:
        return pd.read_csv(config.app.path.processed_dataset)
    except Exception as e:
        raise e


@task
def save_splits(
    datasets: dict,
    config: type,
):
    try:
        datasets.get(config.app.ml.const.trainset).data.to_csv(
            config.app.path.trainset)
        datasets.get(config.app.ml.const.testset).data.to_csv(
            config.app.path.testset)
    except Exception as e:
        raise e


@task
def train_test_sift_suite(
    trainset: Dataset,
    testset: Dataset,
    config: dict,
):
    try:

        tts_suite = train_test_validation()
        if ignore_ticks := list(config.app.ml.data.ticks.ignore_ttv):
            for tick in ignore_ticks:
                tts_suite.remove(tick)
        result = tts_suite.run(
            trainset,
            testset,
        )
        result.save_as_html(config.app.path.tt_sift_html)
        return result
    except Exception as e:
        raise e


@flow
def run_train_test_sift_suite():
    try:
        config = boot_config()
        processed_df = boot_processed_dataframe(config)
        dc_dataset = boot_dc_dataset(
            processed_df,
            config,
        )
        trainset, testset = dc_dataset.train_test_split()
        result = train_test_sift_suite(
            trainset,
            testset,
            config,
        )
        sift_success(result)
        save_splits(
            dict(
                trainset=trainset,
                testset=testset,
            ),
            config,
        )

    except AssertionError:
        log.error(result.get_not_passed_checks())

    except Exception as e:
        raise e


if __name__ == "main":
    run_train_test_sift_suite()
