import pathlib

from ml.sifts import run_train_test_sift_suite


def test_train_test_sift(app_config):
    assert run_train_test_sift_suite()
    assert pathlib.Path(app_config.app.path.trainset).is_file()
    assert pathlib.Path(app_config.app.path.testset).is_file()
