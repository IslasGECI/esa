import eradication_success_assessment as esa
import pandas as pd
from eradication_success_assessment.get_required_effort import make_fit
from eradication_success_assessment.get_required_effort import get_required_effort

input_test: str = "tests/data/camaras_trampa_erradicacion_rata_natividad.csv"
data: pd.DataFrame = pd.read_csv(input_test)
capture_date = pd.to_datetime("2019-11-09")
d: dict = {
    "Fecha": ["2019-11-09", "2019-11-08", "2019-11-10", "2019-11-11"],
    "Cantidad_de_trampas_activas": [1, 2, 3, 4],
    "Cantidad_de_avistamientos": [1, 0, 0, 0],
}
dates: pd.DataFrame = pd.DataFrame(data=d)
output_tests = {
    "effort_without_sighted": 3,
    "required_effort": 3,
    "significance_level": 0.050000000000000044,
    "success_probability": 0.99,
}


def test_make_fit():
    output: dict = make_fit(dates, capture_date, True)
    assert output == output_tests

def test_get_required_effort():
    output: dict = get_required_effort()
    pass
