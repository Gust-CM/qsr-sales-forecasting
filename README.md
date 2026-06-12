# 🍗 Forecasting de ventas para una cadena QSR — *Validación técnica*

Sistema de **proyección de ventas diarias** para una cadena de restaurantes de
comida rápida, con foco en lo que de verdad da confianza a un equipo de negocio:
**validar el modelo antes de usarlo.**

> ⚠️ **Datos 100% sintéticos.** Todos los datos de este repositorio son generados
> por simulación (`data/generate_synthetic_data.py`) y no provienen de ninguna
> empresa real. El objetivo es mostrar la **metodología y la habilidad técnica**,
> no datos de negocio de un tercero.

---

## 🎯 El problema

En una operación de restaurantes, proyectar ventas no es solo "adivinar el total
del año". El reto real es:

1. Proyectar la venta con suficiente precisión para planificar.
2. Bajar ese número anual a una **meta diaria por tienda** que la operación
   pueda usar (staffing, inventario, compras).
3. **Confiar** en el modelo: ¿cómo sé que no se está equivocando feo?

Este repositorio se concentra en el punto 3, que es la base de todo lo demás.

---

## 🧪 Qué demuestra este repo: el *backtest*

En lugar de pedirle al modelo que prediga el futuro (que no se puede verificar),
le pedimos que prediga un año que **ya conocemos**:

- Se entrena con **2021–2024**.
- Se le pide proyectar **2025** sin haberlo visto nunca.
- Se compara la proyección contra lo que realmente pasó.

### Resultados sobre los datos sintéticos

| Métrica            | Resultado |
|--------------------|-----------|
| **MAPE mensual**   | **0.88%** |
| MAPE diario        | 3.34%     |
| Bias anual         | +0.14%    |

> Un MAPE mensual por debajo del 1% indica que el modelo reproduce la estructura
> estacional de la cadena con alta fidelidad. (El número exacto depende de la
> semilla aleatoria del generador.)

El notebook produce además una comparación visual **real vs. forecast**:

📓 **[`notebooks/01_validacion_backtest.ipynb`](notebooks/01_validacion_backtest.ipynb)**

---

## 🔧 Metodología

- **Modelo:** [Prophet](https://facebook.github.io/prophet/) con estacionalidad
  **anual** y **semanal** (los dos patrones dominantes en un QSR: temporada del
  año + efecto fin de semana).
- **Validación:** holdout temporal (train 2021–2024 / test 2025), métricas MAPE y
  bias agregadas a nivel mensual, que es la granularidad típica de un presupuesto.
- **Datos sintéticos** con estructura realista: tendencia de crecimiento,
  estacionalidad anual y semanal, feriados con uplift, y ruido idiosincrático por
  tienda.

---

## 🚀 Cómo correrlo

```bash
# 1. Clonar el repo
git clone https://github.com/<tu-usuario>/qsr-sales-forecasting.git
cd qsr-sales-forecasting

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Generar los datos sintéticos
python data/generate_synthetic_data.py

# 4. Abrir el notebook de validación
jupyter notebook notebooks/01_validacion_backtest.ipynb
```

---

## 📂 Estructura

```
qsr-sales-forecasting/
├── data/
│   └── generate_synthetic_data.py   # genera ventas diarias sintéticas
├── notebooks/
│   └── 01_validacion_backtest.ipynb # backtest + métricas + gráfico
├── requirements.txt
└── README.md
```

---

## 🗺️ Roadmap (proyecto completo)

Este repo cubre la **validación**. La metodología completa, aplicada en un entorno
profesional, incluye además:

- Forecast del año siguiente con feriados, calendario comercial y promociones
  recurrentes como regresores.
- Distribución del presupuesto anual en **metas diarias por tienda**, con efecto
  quincena, eventos especiales y sensibilidad por zona.
- Proyección de **transacciones** a partir del ticket promedio ajustado por pricing.

---

## 📝 Licencia

MIT — ver `LICENSE`. Libre de usar como referencia metodológica.
