"""Interfaz Streamlit del modelo epidemiológico SIR."""

from __future__ import annotations

import matplotlib.pyplot as plt
import streamlit as st

from backend import simulate_sir


st.set_page_config(page_title="Modelo SIR", page_icon="🦠", layout="wide")
st.title("Modelo de propagación epidemiológica · SIR")
st.write("Simula la evolución de personas susceptibles, infectadas y recuperadas en una población cerrada.")

with st.sidebar:
    st.header("Parámetros")
    population = st.number_input("Población total", min_value=10, value=10000, step=1000)
    infected = st.number_input("Infectados iniciales", min_value=1, value=10, step=1)
    recovered = st.number_input("Recuperados iniciales", min_value=0, value=0, step=1)
    beta = st.number_input("Tasa de transmisión β", min_value=0.0, value=0.30, step=0.05, format="%.3f")
    gamma = st.number_input("Tasa de recuperación γ", min_value=0.001, value=0.10, step=0.01, format="%.3f")
    duration = st.slider("Días simulados", min_value=30, max_value=730, value=180, step=10)

try:
    result = simulate_sir(population, infected, recovered, beta, gamma, duration)
except ValueError as error:
    st.error(str(error))
    st.stop()

metrics = st.columns(3)
metrics[0].metric("Número reproductivo inicial R₀", f"{beta / gamma:.2f}")
metrics[1].metric("Pico de infectados", f"{result.peak_infected:,.0f}")
metrics[2].metric("Día del pico", f"{result.peak_day:.1f}")

fig, axis = plt.subplots(figsize=(11, 5.5))
axis.plot(result.times, result.susceptible, label="Susceptibles")
axis.plot(result.times, result.infected, label="Infectados")
axis.plot(result.times, result.recovered, label="Recuperados")
axis.set(title="Evolución del brote", xlabel="Días", ylabel="Personas")
axis.grid(True, alpha=0.3)
axis.legend()
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)
st.caption("SIR es un modelo simplificado: supone mezcla homogénea, población cerrada y tasas constantes.")
