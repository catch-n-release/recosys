from ml.sifts import run_data_integrity_suite


def test_data_integrity_suite():
    assert run_data_integrity_suite()
