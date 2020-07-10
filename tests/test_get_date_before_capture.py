import eradication_success_assessment as esa
from eradication_success_assessment.get_required_effort import _get_date_before_capture
from eradication_success_assessment.get_required_effort import _get_date_after_capture
import pandas as pd
from pandas._testing import assert_frame_equal

d: dict = {
    "Fecha": ["2019-11-09", "2019-11-08", "2019-11-10"],
    "Cantidad_de_trampas_activas": [1, 2, 3],
    "Cantidad_de_avistamientos": [1, 0, 0],
}
dates: pd.DataFrame = pd.DataFrame(data=d)
e: dict = {
    "Fecha": ["2019-11-09", "2019-11-08"],
    "Cantidad_de_trampas_activas": [1, 2],
    "Cantidad_de_avistamientos": [1, 0],
}
expected_dates: pd.DataFrame = pd.DataFrame(data=e)
capture_date = pd.to_datetime("2019-11-09")


def test_get_date_before_capture():
    salida = _get_date_before_capture(dates, capture_date)
    assert_frame_equal(expected_dates, salida)


a: dict = {
    "Fecha": ["2019-11-10"],
    "Cantidad_de_trampas_activas": [3],
    "Cantidad_de_avistamientos": [0],
}
expected_dates_2: pd.DataFrame = pd.DataFrame(data=a)


def test_get_date_after_capture():
    salida = _get_date_after_capture(dates, capture_date)
    assert_frame_equal(dates.iloc[[2]], salida)
