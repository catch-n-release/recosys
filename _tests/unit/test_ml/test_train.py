from ml import train
from pathlib import Path


def test_train(app_config):
    train()
    assert Path(app_config.app.path.predictor).is_file()
