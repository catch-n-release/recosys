from pathlib import Path

from ml import train


def test_train(app_config):
    train()
    assert Path(app_config.app.path.predictor).is_file()
