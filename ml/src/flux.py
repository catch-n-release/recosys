from prefect import flow

from ml.src.sifts import run_data_integrity_suite, run_train_test_sift_suite, run_predictor_eval_suite
from ml import preprocess_dataset, train, log


@flow
def init_flux():
    try:
        run_data_integrity_suite()
        preprocess_dataset()
        run_train_test_sift_suite()
        train()
        run_predictor_eval_suite()
        return True
    except Exception as e:
        raise e
