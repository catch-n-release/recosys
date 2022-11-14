from deepchecks.tabular.suites import model_evaluation
from deepchecks.core import SuiteResult
from prefect import flow, task
from surprise import dump, AlgoBase

from utils import boot_config, sift_success, DeepchecksModelWrapper, boot_dc_dataset, boot_train_test
from ml import log


@task
def boot_predictor(config: type) -> AlgoBase:
    try:
        return dump.load(config.app.path.predictor)[1]
    except Exception as e:
        raise e


@task
def predictor_eval_sift_suite(
    config: type,
    predictor: AlgoBase,
    datasets: dict,
) -> SuiteResult:
    try:
        pes_suite = model_evaluation()
        if ignore_ticks := list(config.app.ml.data.ticks.ignore_pe):
            for tick in ignore_ticks:
                pes_suite.remove(tick)
        result = pes_suite.run(
            train_dataset=datasets.get(config.app.ml.const.trainset),
            test_dataset=datasets.get(config.app.ml.const.trainset),
            model=DeepchecksModelWrapper(predictor),
        )
        result.save_as_html(config.app.path.algo_eval_sift_html)
        return result

    except Exception as e:
        raise e


@flow
def run_predictor_eval_suite():
    try:
        config = boot_config()
        datasets = boot_train_test(config)
        datasets = boot_train_test(config)
        dc_datasets = {
            name: boot_dc_dataset(dataset, config)
            for name, dataset in datasets.items()
        }
        predictor = boot_predictor(config)
        result = predictor_eval_sift_suite(config, predictor, dc_datasets)
        sift_success(result)
    except AssertionError:
        log.error(result.get_not_passed_checks())
    except Exception as e:
        raise e


if __name__ == "main":
    run_predictor_eval_suite()
