# Modelo de propagación epidemiológica SIR

Aplicación Streamlit para simular un brote con el modelo SIR: Susceptibles, Infectados y Recuperados. Integra las ecuaciones diferenciales con Runge-Kutta de cuarto orden.

## Parámetros y resultados

- Configura población, infectados y recuperados iniciales, tasas `β` y `γ` y duración.
- Consulta el número reproductivo inicial `R₀ = β/γ`.
- Visualiza las tres poblaciones y el tamaño y día del pico de infectados.

## Estructura

```text
.
├── backend.py       # Ecuaciones SIR e integración RK4
├── frontend.py      # Interfaz y gráfica
├── requirements.txt
└── README.md
```

## Instalación y ejecución

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run frontend.py
```

En macOS o Linux, activa el entorno con `source .venv/bin/activate`.

## Interpretación

El modelo es ilustrativo. Supone mezcla homogénea, población cerrada y parámetros constantes; no representa por sí solo diferencias de edad, medidas sanitarias o reinfecciones.
