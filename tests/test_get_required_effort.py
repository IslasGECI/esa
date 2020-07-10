import eradication_success_assessment as esa
import pandas as pd
from eradication_success_assessment.get_required_effort import make_fit

input_test: str = "tests/data/camaras_trampa_erradicacion_rata_natividad.csv"
data: pd.DataFrame = pd.read_csv(input_test)
capture_date = pd.to_datetime("2019-11-09")

def test_make_fit():
    make_fit(data, capture_date)
    pass

