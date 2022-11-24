from pathlib import Path

from ml import train
from test_ml import pytestmark

pytestmark


def test_train(app_config):
    train()
    assert Path(app_config.app.path.predictor).is_file()
