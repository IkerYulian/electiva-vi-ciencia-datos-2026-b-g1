"""
Serie temporal: resample mensual + medias moviles + descomposicion + 2 visualizaciones.

Uso:  python serie_temporal.py
- Por defecto genera una serie diaria SINTETICA y reproducible (semilla 42) y la guarda
  en datos_diarios.csv.
- Para usar datos reales: pon la ruta en CSV_REAL (columnas: fecha, ventas).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # permite ejecutar sin ventana grafica
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

BASE = Path(__file__).parent
IMG = BASE / "img"
IMG.mkdir(exist_ok=True)
CSV_REAL = None  # p.ej. "mis_datos.csv"

# ---------------------------------------------------------------- 1. DATOS
if CSV_REAL:
    df = pd.read_csv(BASE / CSV_REAL, parse_dates=["fecha"], index_col="fecha")
    serie = df["ventas"].asfreq("D")
    FUENTE = f"Fuente: {CSV_REAL}"
else:
    rng = np.random.default_rng(42)
    dias = pd.date_range("2022-01-01", "2024-12-31", freq="D")
    t = np.arange(len(dias))
    tendencia = 100 + 0.05 * t                                             # +0.05 u/dia
    estacional = 25 * np.cos(2 * np.pi * (dias.dayofyear - 355) / 365)     # pico ~21-dic
    ruido = rng.normal(0, 8, len(dias))
    serie = pd.Series(tendencia + estacional + ruido, index=dias, name="ventas")
    serie.rename_axis("fecha").round(2).to_csv(BASE / "datos_diarios.csv")
    FUENTE = "Fuente: datos sinteticos simulados (semilla 42)"

# ------------------------------------------------- 2. RESAMPLE + MEDIA MOVIL
mensual = serie.resample("MS").sum().to_frame("ventas")       # suma mensual
mensual["mm3"] = mensual["ventas"].rolling(3).mean()          # corto plazo
mensual["mm12"] = mensual["ventas"].rolling(12).mean()        # 1 ciclo estacional completo
mensual.round(1).rename_axis("fecha").to_csv(BASE / "serie_mensual.csv")
print("Ultimos 12 meses:\n", mensual.round(0).tail(12), "\n")

# --------------------------------------------- 3. TENDENCIA Y ESTACIONALIDAD
anual = mensual["ventas"].resample("YS").sum()
crec = (anual.iloc[-1] / anual.iloc[0] - 1) * 100
print("Ventas anuales:\n", anual.round(0))
print(f"Crecimiento {anual.index[0].year}->{anual.index[-1].year}: {crec:.1f}%")

mm12 = mensual["mm12"].dropna()
print(f"MM12: {mm12.iloc[0]:.0f} ({mm12.index[0]:%Y-%m}) -> {mm12.iloc[-1]:.0f} "
      f"({mm12.index[-1]:%Y-%m}) = +{(mm12.iloc[-1]/mm12.iloc[0]-1)*100:.1f}%")

perfil = mensual.groupby(mensual.index.month)["ventas"].mean()
mes_pico, mes_valle = perfil.idxmax(), perfil.idxmin()
dev_pico = (perfil.max() / perfil.mean() - 1) * 100
dev_valle = (perfil.min() / perfil.mean() - 1) * 100
print(f"Mes pico: {mes_pico} ({dev_pico:+.1f}% vs promedio) | "
      f"Mes valle: {mes_valle} ({dev_valle:+.1f}%)")

# Descomposicion aditiva: serie = tendencia + estacionalidad + residuo
desc = seasonal_decompose(mensual["ventas"], model="additive", period=12)
est, res = desc.seasonal, desc.resid.dropna()
fuerza_est = max(0, 1 - res.var() / (est.loc[res.index] + res).var())   # Hyndman (2021)
amplitud = est.max() - est.min()
print(f"Fuerza de estacionalidad: {fuerza_est:.2f} (0 = nula, 1 = total)")
print(f"Amplitud estacional pico-valle: {amplitud:.0f} unidades/mes")

# ------------------------------------------------ 4. GRAFICO 1: EVOLUCION
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(mensual.index, mensual["ventas"], color="lightgray", marker="o", ms=3,
        label="Ventas mensuales")
ax.plot(mensual.index, mensual["mm3"], color="tab:blue", lw=2, label="Media móvil 3 meses")
ax.plot(mensual.index, mensual["mm12"], color="tab:red", lw=2.5,
        label="Media móvil 12 meses (tendencia)")
ax.set_ylim(bottom=0)  # eje Y honesto: parte de cero
ax.set_title(f"Las ventas crecieron {crec:.0f}% entre {anual.index[0].year} y "
             f"{anual.index[-1].year}, con picos cada fin de año",
             loc="left", fontweight="bold")
ax.set_xlabel("Mes"); ax.set_ylabel("Ventas mensuales (unidades)")
ax.legend(frameon=False, loc="lower right")
ax.spines[["top", "right"]].set_visible(False)
fig.text(0.01, 0.01, FUENTE + " | Suma mensual de ventas diarias", fontsize=8, color="gray")
fig.tight_layout(); fig.savefig(IMG / "01_evolucion.png", dpi=150); plt.close(fig)

# ---------------------------------------------- 5. GRAFICO 2: COMPARACION
meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
colores = ["tab:red" if m == mes_pico else "lightgray" for m in perfil.index]
fig, ax = plt.subplots(figsize=(10, 5))
barras = ax.bar(meses, perfil.values, color=colores)
ax.bar_label(barras, fmt="%.0f", padding=2, fontsize=8)      # valores exactos
ax.axhline(perfil.mean(), color="black", ls="--", lw=1, label="Promedio mensual")
ax.set_ylim(bottom=0)  # barras SIEMPRE desde cero
ax.set_title(f"{meses[mes_pico-1]} vende {dev_pico:.0f}% más que el mes promedio; "
             f"{meses[mes_valle-1]} es el más débil", loc="left", fontweight="bold")
ax.set_xlabel("Mes del año"); ax.set_ylabel("Ventas mensuales promedio 2022-2024 (unidades)")
ax.legend(frameon=False, loc="upper center")
ax.spines[["top", "right"]].set_visible(False)
fig.text(0.01, 0.01, FUENTE + " | Promedio de cada mes calendario", fontsize=8, color="gray")
fig.tight_layout(); fig.savefig(IMG / "02_comparacion.png", dpi=150); plt.close(fig)

# --------------------------------- 6. EXTRA: DESCOMPOSICION (apoya la interpretacion)
fig, axs = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
axs[0].plot(desc.trend, color="tab:red", lw=2); axs[0].set_ylabel("Tendencia")
axs[1].plot(est, color="tab:blue", lw=2); axs[1].axhline(0, color="gray", lw=.8)
axs[1].set_ylabel("Estacionalidad")
axs[2].bar(desc.resid.index, desc.resid, width=20, color="gray"); axs[2].axhline(0, color="gray", lw=.8)
axs[2].set_ylabel("Residuo"); axs[2].set_xlabel("Mes")
axs[0].set_title("La tendencia sube de forma sostenida y la estacionalidad se repite igual cada año",
                 loc="left", fontweight="bold")
for a in axs: a.spines[["top", "right"]].set_visible(False)
fig.text(0.01, 0.005, "Descomposición aditiva (period=12). La tendencia (media móvil centrada) no se calcula en los 6 meses de cada extremo. Escalas verticales distintas por panel."
         "", fontsize=8, color="gray")
fig.tight_layout(rect=(0, 0.02, 1, 1)); fig.savefig(IMG / "03_descomposicion.png", dpi=150)
print("\nListo: img/01_evolucion.png, img/02_comparacion.png, img/03_descomposicion.png")
