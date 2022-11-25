from ml.sifts import run_predictor_eval_suite
from test_ml import mlmark

mlmark


def test_predictor_eval_suite():
    assert run_predictor_eval_suite()
