"""
Generador de datos sintéticos — Cadena QSR ficticia "Pollos del Valle"
======================================================================

Crea ventas diarias por tienda (2021-2025) con la MISMA estructura que se
observa en una operación real de restaurantes:

    - Tendencia de crecimiento de largo plazo
    - Estacionalidad anual (picos en vacaciones / fin de año)
    - Estacionalidad semanal (viernes y sábado fuertes)
    - Efecto de feriados (afluencia elevada)
    - Ruido diario idiosincrático por tienda

NINGÚN dato proviene de una empresa real. Todo es generado por simulación
con una semilla fija para que el resultado sea 100% reproducible.

Uso:
    python generate_synthetic_data.py
    -> escribe data/ventas_sinteticas.csv
"""

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------------------------------
SEED = 42
START = "2021-01-01"
END = "2025-12-31"
N_STORES = 12                  # cantidad de tiendas ficticias
ANNUAL_GROWTH = 0.06           # crecimiento orgánico anual (~6%)
BASE_DAILY_SALES = 1_800_000   # venta diaria base por tienda (₡, ficticio)

rng = np.random.default_rng(SEED)


# --------------------------------------------------------------------------
# COMPONENTES ESTACIONALES (multiplicadores)
# --------------------------------------------------------------------------
def weekly_factor(dow: int) -> float:
    """0 = lunes ... 6 = domingo. Viernes/sábado arriba, lunes/martes abajo."""
    table = {0: 0.82, 1: 0.85, 2: 0.95, 3: 1.00, 4: 1.28, 5: 1.35, 6: 1.10}
    return table[dow]


def yearly_factor(day_of_year: int) -> float:
    """Onda anual suave + repunte de fin de año."""
    base = 1.0 + 0.10 * np.sin(2 * np.pi * (day_of_year - 60) / 365.0)
    december_lift = 0.18 if day_of_year >= 350 else 0.0
    return base + december_lift


# Feriados ficticios (mismas fechas cada año) con su uplift
HOLIDAYS = {
    (1, 1): 1.15,    # Año Nuevo
    (4, 11): 1.10,   # feriado cívico ficticio
    (5, 1): 1.12,    # Día del Trabajo
    (7, 25): 1.20,   # feriado de temporada alta
    (8, 15): 1.18,   # feriado familiar
    (9, 15): 1.16,   # fiestas patrias
    (12, 24): 1.35,  # Nochebuena
    (12, 25): 0.70,  # Navidad (cierre parcial)
    (12, 31): 1.30,  # fin de año
}


def holiday_factor(month: int, day: int) -> float:
    return HOLIDAYS.get((month, day), 1.0)


# --------------------------------------------------------------------------
# GENERACIÓN
# --------------------------------------------------------------------------
def build() -> pd.DataFrame:
    dates = pd.date_range(START, END, freq="D")

    # Cada tienda tiene un nivel y una volatilidad propios
    store_levels = rng.uniform(0.55, 1.6, size=N_STORES)
    store_noise = rng.uniform(0.04, 0.09, size=N_STORES)

    rows = []
    for s in range(N_STORES):
        cod_tienda = f"T{s + 1:03d}"
        level = store_levels[s]
        sigma = store_noise[s]

        for d in dates:
            years_in = (d - pd.Timestamp(START)).days / 365.0
            trend = (1 + ANNUAL_GROWTH) ** years_in

            mult = (
                weekly_factor(d.dayofweek)
                * yearly_factor(d.dayofyear)
                * holiday_factor(d.month, d.day)
                * trend
            )

            noise = rng.normal(1.0, sigma)
            ventaneta = BASE_DAILY_SALES * level * mult * noise
            ventaneta = max(ventaneta, 0)

            # ticket promedio ficticio ~ ₡4.500 con leve variación
            ticket = rng.normal(4500, 250)
            transacciones = max(int(round(ventaneta / ticket)), 1)

            rows.append(
                {
                    "tienda": cod_tienda,
                    "fechacierre": d,
                    "ventaneta": round(ventaneta, 2),
                    "transacciones": transacciones,
                }
            )

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    df = build()
    out = "ventas_sinteticas.csv"
    df.to_csv(out, index=False)
    print(f"Generadas {len(df):,} filas en {out}")
    print(df.head())
    print("\nVenta total por año (₡):")
    print(df.assign(anio=df["fechacierre"].dt.year).groupby("anio")["ventaneta"].sum().map(lambda x: f"{x:,.0f}"))
