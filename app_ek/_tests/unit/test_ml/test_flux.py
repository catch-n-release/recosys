from ml import init_flux
from test_ml import pytestmark

pytestmark


def test_flux():
    assert init_flux()
