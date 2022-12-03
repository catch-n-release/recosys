from pathlib import Path

from ml import preprocess_dataset


def test_preprocess_dataset(app_config):
    preprocess_dataset()
    assert Path(app_config.app.path.processed_dataset).is_file()
