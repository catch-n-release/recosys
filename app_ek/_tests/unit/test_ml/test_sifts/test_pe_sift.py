from ml.sifts import run_predictor_eval_suite
from test_ml import pytestmark

pytestmark


def test_predictor_eval_suite():
    assert run_predictor_eval_suite()
