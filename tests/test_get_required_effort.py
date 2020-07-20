import subprocess
import pandas as pd
from pandas._testing import assert_frame_equal
from eradication_success_assessment import make_fit
from eradication_success_assessment import get_required_effort
from eradication_success_assessment.get_required_effort import _add_sighting

input_test: str = "tests/data/camaras_trampa_erradicacion_rata_natividad.csv"
data: pd.DataFrame = pd.read_csv(input_test)
capture_date = pd.to_datetime("2019-11-09")
d: dict = {
    "Fecha": ["2019-11-09", "2019-11-08", "2019-11-10", "2019-11-11"],
    "Cantidad_de_trampas_activas": [1, 2, 3, 4],
    "Cantidad_de_avistamientos": [1, 0, 0, 0],
    "is_sighting": [True, False, False, False],
}
d_2: dict = {
    "Fecha": ["2019-11-09", "2019-11-08", "2019-11-10", "2019-11-11"],
    "Cantidad_de_trampas_activas": [1, 2, 3, 4],
    "Cantidad_de_avistamientos": [1, 0, 0, 0],
    "is_sighting": [True, False, False, False],
    "sighting": [1, 1, 1, 1],
}
dates: pd.DataFrame = pd.DataFrame(data=d)
dates_2: pd.DataFrame = pd.DataFrame(data=d_2)
output_tests = {
    "effort_without_sighted": 3,
    "required_effort": 3,
    "significance_level": 0.050000000000000044,
    "success_probability": 0.99,
}

output_tests_2 = "{'required_effort': 381, 'success_probability': 0.99, 'significance_level': 0.050000000000000044, 'effort_without_sighted': 681}\n"


def test_make_fit():
    output: dict = make_fit(dates, capture_date, True)
    assert output == output_tests


def test_get_required_effort(capsys):
    output: dict = get_required_effort(seed=True)
    captured = capsys.readouterr()
    assert captured.out == output_tests_2
    output: dict = get_required_effort()
    captured = capsys.readouterr()
    assert captured.out != output_tests_2


def test_add_sighting():
    output = _add_sighting(dates)
    assert_frame_equal(dates_2, output, check_dtype=False)
