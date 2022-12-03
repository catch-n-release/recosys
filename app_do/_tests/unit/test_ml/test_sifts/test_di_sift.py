from ml.sifts import run_data_integrity_suite
from test_ml import pytestmark

pytestmark


def test_data_integrity_suite():
    assert run_data_integrity_suite()
