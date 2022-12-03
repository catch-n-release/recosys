from datetime import timedelta
from deepchecks.tabular import Dataset
from deepchecks.tabular.suites import data_integrity
from prefect import flow, task
from prefect.tasks import task_input_hash

from ml.utils import boot_config, sift_success, boot_dc_dataset
from ml.src.ingress import boot_dataframe
from ml import log


@task(
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1),
)
def data_integrity_suite(
    dataset: Dataset,
    config: type,
):
    try:

        di_suite = data_integrity()
        if ignore_ticks := list(config.ml.data.ticks.ignore_di):
            for tick in ignore_ticks:
                di_suite.remove(tick)
        result = di_suite.run(dataset)
        result.save_as_html(config.ml.path.di_sift_html)
        return result
    except Exception as e:
        raise e


@flow
def run_data_integrity_suite():
    try:

        config = boot_config()
        raw_df = boot_dataframe(config)
        dc_dataset = boot_dc_dataset(raw_df, config)
        result = data_integrity_suite(dc_dataset, config)
        sift_success(result)
    except AssertionError:
        log.error(result.get_not_passed_checks())
    except Exception as e:
        raise e


if __name__ == "__main__":
    run_data_integrity_suite()
