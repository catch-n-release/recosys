"""Logger test cases.
"""
from utils.logger import Logger
import logging
import pytest


@pytest.mark.parametrize("fixture, instance, handler",
                         [("", True, True), ("app_config", True, True)])
def test_logger(fixture, instance, handler, request):
    """Test for custom Logger.

    Args:
        fixture (fixture): Pytest fixture for app configurations.
        insatnce (bool): check for same instance.
        handler (bool): check for handlers.
        request (fixture): request fixture.
    """
    logger = Logger(toml_file_path=request.getfixturevalue(
        fixture).app.path.self) if fixture else Logger()
    log = logger.setup()
    assert isinstance(log, logging.Logger)
    assert log.hasHandlers()
