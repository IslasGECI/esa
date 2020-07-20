#!/usr/bin/env python
#
#
from scipy.stats import genextreme
import numpy as np
import pandas as pd
import typer

app = typer.Typer()


@app.command()
def get_required_effort(
    name: str = "tests/data/camaras_trampa_erradicacion_rata_natividad.csv", seed: bool = False
):
    capture_date = pd.to_datetime("2019-11-09")

    datafile: str = name
    data = pd.read_csv(datafile)
    output = make_fit(data, capture_date, seed)
    print(output)


def make_fit(data, capture_date, seed):
    if seed:
        np.random.seed(3)
    data_before_capture = _get_date_before_capture(data, capture_date)

    effort_without_sighted = data_before_capture["Cantidad_de_trampas_activas"].sum()
    data_before_capture["is_sighting"] = data_before_capture.Cantidad_de_avistamientos != 0
    data_before_capture = _add_sighting(data_before_capture)
    effort_per_sighting = data_before_capture.groupby("sighting")[
        "Cantidad_de_trampas_activas"
    ].sum()

    n_effort_per_sighting = len(effort_per_sighting)
    n_boostraping: int = 20
    required_effort: np.array = np.zeros(n_boostraping)

    success_probability: float = 0.99
    for i in range(n_boostraping):
        resampled_effort_per_sighting = np.random.choice(effort_per_sighting, n_effort_per_sighting)
        fit = genextreme.fit(resampled_effort_per_sighting)
        required_effort[i] = genextreme.ppf(success_probability, fit[0], fit[1], fit[2])

    p_value_complement: float = 0.95
    reported_effort = np.quantile(required_effort, p_value_complement).astype(int)
    output: dict = {
        "required_effort": reported_effort,
        "success_probability": success_probability,
        "significance_level": 1 - p_value_complement,
        "effort_without_sighted": effort_without_sighted,
    }
    return output


@app.command()
def write_methodology():
    print(
        """
    \subsection*{Análisis}
Utilizamos la función de distribución de valores extremos generalizada (GEV, por sus siglas en 
inglés) para modelar la probabilidad de éxito en la erradiación de rata a partir de las 
observaciones en cámaras trampa. La GEV es una familia de funciones continuas de probabilidad que
combina las funciones de Gumbel, Fréchet y Weibull, conocidas como funciones de distribución de 
valores extremos de tipo I, II y III: 
$$
f(s;\\xi) = \\left\\{
        \\begin{array}{ll}
            \\exp(-(1+\\xi s)^{\\frac{-1}{\\xi}}) & \\quad \\xi \\neq 0 \\\\
            \\exp(-\\exp(-s)) & \\quad \\xi = 0
        \\end{array}
    \\right.
$$
el tipo I es cuando $\\xi = 0$, el tipo II cuando $\\xi > 0$ y el tipo III con $\\xi<0$.

Considerando los esfuerzos entre avistamientos, definimos la probabilidad de obtener una captura
dependiendo del esfuerzo dado. De manera similar, podemos saber cuál es el esfuerzo necesario para 
tener una probabilidad de éxito de erradicación deseada. A mayor esfuerzo, sin evidencia de rata, 
la probabilidad del éxito en la erradicación será mayor. 

Calculamos el esfuerzo necesario para alcanzar una probabilidad de 
\\py{'%4.1f'% success_probability}\\%
en el éxito de la erradicación, con un nivel de significancia del 
$\\alpha=$\\py{'%4.2f'% effort['significance_level']}.
"""
    )


def _get_date_before_capture(data: pd.DataFrame, capture_date):
    date: pd.DataFrame = pd.to_datetime(data.Fecha)
    is_before_capture = date <= capture_date
    data_before_capture = data[is_before_capture]
    return data_before_capture


def _get_date_after_capture(data: pd.DataFrame, capture_date):
    date: pd.DataFrame = pd.to_datetime(data.Fecha)
    is_after_capture = date > capture_date
    data_after_capture = data[is_after_capture]
    return data_after_capture

def _add_sighting(data: pd.DataFrame):
    i_sighting = 0
    for i_index, i_row in data.iterrows():
        if i_row["is_sighting"]:
            i_sighting = i_sighting + 1
        data.loc[i_index, "sighting"] = i_sighting
    return data
    

if __name__ == "__main__":
    app()