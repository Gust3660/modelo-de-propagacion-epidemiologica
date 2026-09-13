"""Modelo SIR para simulación de propagación epidemiológica."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SIRResult:
    times: np.ndarray
    susceptible: np.ndarray
    infected: np.ndarray
    recovered: np.ndarray
    peak_infected: float
    peak_day: float


def simulate_sir(population: float, initial_infected: float, initial_recovered: float,
                 beta: float, gamma: float, duration: float, steps: int = 1200) -> SIRResult:
    if population <= 0 or min(initial_infected, initial_recovered) < 0:
        raise ValueError("La población debe ser positiva y los conteos iniciales no negativos.")
    if initial_infected + initial_recovered > population:
        raise ValueError("La suma de infectados y recuperados no puede superar la población.")
    if beta < 0 or gamma <= 0 or duration <= 0 or steps < 2:
        raise ValueError("Usa β ≥ 0, γ > 0, duración positiva y al menos dos pasos.")
    initial = np.array([population - initial_infected - initial_recovered,
                        initial_infected, initial_recovered], dtype=float)

    def derivative(state: np.ndarray) -> np.ndarray:
        susceptible, infected, _ = state
        new_infections = beta * susceptible * infected / population
        recoveries = gamma * infected
        return np.array([-new_infections, new_infections - recoveries, recoveries])

    times = np.linspace(0, duration, steps + 1)
    values = np.empty((steps + 1, 3), dtype=float)
    values[0] = initial
    h = duration / steps
    for index in range(steps):
        current = values[index]
        k1 = derivative(current)
        k2 = derivative(current + h * k1 / 2)
        k3 = derivative(current + h * k2 / 2)
        k4 = derivative(current + h * k3)
        values[index + 1] = current + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        values[index + 1] = np.maximum(values[index + 1], 0)
        values[index + 1] *= population / values[index + 1].sum()
    peak_index = int(np.argmax(values[:, 1]))
    return SIRResult(times, values[:, 0], values[:, 1], values[:, 2],
                     float(values[peak_index, 1]), float(times[peak_index]))
