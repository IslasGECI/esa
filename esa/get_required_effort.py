#!/usr/bin/env python
#
#
from scipy.stats import genextreme
from geci_plots import plot_histogram_with_limits
import numpy as np
import pandas as pd
import json

def read_json(path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
    return data


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


def plot_histogram_effort(path: str = "tests/data/salidita.json"):
    data = read_json(path)
    to_plot = _clean_effort(data)
    limits = [data["required_effort"], data["effort_without_sighted"]]
    figure = plot_histogram_with_limits(x=to_plot, bins=10, limits=limits)
    return figure


def _clean_effort(data):
    to_plot = [x for x in data["effort"] if x < 1000]
    return to_plot
