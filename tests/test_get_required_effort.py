import pytest
import pandas as pd
from pandas._testing import assert_frame_equal
from eradication_success_assessment import make_fit
from eradication_success_assessment import get_required_effort
from eradication_success_assessment import plot_histogram_effort
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
dates: pd.DataFrame = pd.DataFrame(data=d)


def test_make_fit():
    expected_output = {
        "effort_without_sighted": 3,
        "required_effort": 3,
        "significance_level": 0.050000000000000044,
        "success_probability": 0.99,
        "effort": [
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
            3.0,
        ],
    }

    obtained_output = make_fit(dates, capture_date, True, n_bootstrapping=30, return_effort=True)
    assert obtained_output == expected_output


OUTPUT_TESTS_2 = '{"required_effort": 381, "success_probability": 0.99, "significance_level": 0.050000000000000044, "effort_without_sighted": 681}\n'


def test_get_required_effort(capsys):
    get_required_effort(seed=True, n_bootstrapping=30)
    captured = capsys.readouterr()
    assert captured.out == OUTPUT_TESTS_2
    get_required_effort(n_bootstrapping=30)
    captured = capsys.readouterr()
    assert captured.out != OUTPUT_TESTS_2
    get_required_effort(seed=True)
    captured = capsys.readouterr()
    assert captured.out == OUTPUT_TESTS_2


d_2: dict = {
    "Fecha": ["2019-11-09", "2019-11-08", "2019-11-10", "2019-11-11"],
    "Cantidad_de_trampas_activas": [1, 2, 3, 4],
    "Cantidad_de_avistamientos": [1, 0, 0, 0],
    "is_sighting": [True, False, False, False],
    "sighting": [1, 1, 1, 1],
}
dates_2: pd.DataFrame = pd.DataFrame(data=d_2)


def test_add_sighting():
    output = _add_sighting(dates)
    assert_frame_equal(dates_2, output, check_dtype=False)


@pytest.mark.mpl_image_compare
def test_plot_histogram_effort():
    obtainad_histogram = plot_histogram_effort("salidita.json")
    return obtainad_histogram
