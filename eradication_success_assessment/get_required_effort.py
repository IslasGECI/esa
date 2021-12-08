#!/usr/bin/env python
#
#
from scipy.stats import genextreme
from geci_plots import plot_histogram_with_limits
import numpy as np
import pandas as pd
import typer
import json

app = typer.Typer()


def read_json(path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
    return data


@app.command()
def get_required_effort(
    name: str = "tests/data/camaras_trampa_erradicacion_rata_natividad.csv",
    seed: bool = False,
    n_bootstrapping: int = 30,
    return_effort: bool = False,
):
    capture_date = pd.to_datetime("2019-11-09")

    datafile: str = name
    data = pd.read_csv(datafile)
    output = make_fit(data, capture_date, seed, n_bootstrapping, return_effort)
    print(json.dumps(output))
    return output


def make_fit(data, capture_date, seed, n_bootstrapping, return_effort):
    if seed:
        np.random.seed(3)

    data_before_capture = _get_date_before_capture(data, capture_date)
    success_probability: float = 0.99
    required_effort = calculate_required_effort(
        data_before_capture, n_bootstrapping, success_probability
    )

    p_value_complement: float = 0.95
    effort_without_sighted = data_before_capture["Cantidad_de_trampas_activas"].sum()
    bound_effort = np.quantile(required_effort, p_value_complement).astype(int)
    output = export_output(
        p_value_complement, bound_effort, success_probability, effort_without_sighted
    )
    if return_effort:
        required_effort = {"effort": list(required_effort)}
        output.update(required_effort)
    return output


def calculate_required_effort(data_before_capture, n_bootstrapping, success_probability):
    effort_per_sighting = calculate_effort_per_sighting(data_before_capture)
    n_effort_per_sighting = len(effort_per_sighting)
    required_effort: np.array = np.zeros(n_bootstrapping)
    for i in range(n_bootstrapping):
        resampled_effort_per_sighting = np.random.choice(effort_per_sighting, n_effort_per_sighting)
        fit = genextreme.fit(resampled_effort_per_sighting)
        required_effort[i] = genextreme.ppf(success_probability, fit[0], fit[1], fit[2])
    return required_effort


def export_output(p_value_complement, bound_effort, success_probability, effort_without_sighted):
    output: dict = {
        "required_effort": int(bound_effort),
        "success_probability": success_probability,
        "significance_level": 1 - p_value_complement,
        "effort_without_sighted": int(effort_without_sighted),
    }
    return output


def calculate_effort_per_sighting(data_before_capture):
    data_before_capture["is_sighting"] = data_before_capture.Cantidad_de_avistamientos != 0
    data_before_capture = _add_sighting(data_before_capture)
    effort_per_sighting = data_before_capture.groupby("sighting")[
        "Cantidad_de_trampas_activas"
    ].sum()
    return effort_per_sighting


@app.command()
def write_methodology():
    print(
        """
\\subsection*{Análisis}
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
tener una probabilidad de éxito de erradicación deseada. A mayor esfuerzo, sin evidencia de rata, la
probabilidad del éxito en la erradicación será mayor.

Calculamos el esfuerzo necesario para alcanzar una probabilidad de
\\py{'%4.1f'% success_probability}\\%
en el éxito de la erradicación, con un nivel de significancia del
$\\alpha=$\\py{'%4.2f'% effort['significance_level']}.
"""
    )


@app.command()
def version():
    ver = "0.2.0"
    print(ver)


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


@app.command()
def plot_histogram_effort(path: str = "salidita.json"):
    data = read_json(path)
    to_plot = [x for x in data["effort"] if x < 1000]
    limits = [data["required_effort"], data["effort_without_sighted"]]
    figure = plot_histogram_with_limits(x=to_plot, bins=10, limits=limits)
    return figure


if __name__ == "__main__":
    app()
