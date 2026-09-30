# Semana 5 - Modelo, consulta y limpieza de datos
# Caso: mantenimiento de maquinaria en una línea de producción
# Uso:  pip install pandas numpy   |   python analisis.py
import numpy as np
import pandas as pd

# ============ 1. CREAR Y CARGAR EL DATASET (CSV simulado y "sucio") ============
rng = np.random.default_rng(42)
n = 500
maquinas = {1: "Prensa A", 2: "Soldadora B", 3: "Cinta C", 4: "Robot D", 5: "Taladro E"}
fallas = ["Rodamiento", "Sobrecalentamiento", "Electrica", "Lubricacion"]

raw = pd.DataFrame({
    "registro_id": range(1, n + 1),
    "fecha": pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 700, n), unit="D"),
    "maquina_id": rng.integers(1, 6, n).astype(float),
    "tipo_falla": rng.choice(fallas, n),
    "tecnico": rng.choice(["Ana Ruiz", "Luis Mora", "Sara Paz"], n),
})
raw["maquina"] = raw["maquina_id"].map(maquinas)
es_rod = raw["tipo_falla"] == "Rodamiento"
raw["vibracion_mm_s"] = np.where(es_rod, rng.normal(8, 1.5, n), rng.normal(4, 1.5, n)).round(2)
raw["temperatura_c"] = np.where(raw["tipo_falla"] == "Sobrecalentamiento", rng.normal(85, 5, n), rng.normal(65, 6, n)).round(1)
raw["tiempo_reparacion_h"] = np.where(es_rod, rng.normal(5, 1.5, n), rng.normal(2.5, 1, n)).round(1).astype(object)

# Ensuciar los datos
raw["fecha"] = [f.strftime("%Y-%m-%d") if i % 3 else f.strftime("%d/%m/%Y") for i, f in enumerate(raw["fecha"])]
raw["maquina"] = [m if i % 3 == 0 else (m.lower() if i % 3 == 1 else f" {m.upper()} ") for i, m in enumerate(raw["maquina"])]
raw.loc[rng.choice(n, 25, replace=False), "tiempo_reparacion_h"] = None
raw.loc[rng.choice(n, 40, replace=False), "vibracion_mm_s"] = None
raw.loc[rng.choice(n, 25, replace=False), "temperatura_c"] = None
raw.loc[rng.choice(n, 30, replace=False), "tecnico"] = None
raw.loc[rng.choice(n, 10, replace=False), "maquina_id"] = None
raw.loc[rng.choice(n, 6, replace=False), "tiempo_reparacion_h"] = -1.0
idx = rng.choice(n, 40, replace=False)
raw.loc[idx, "tiempo_reparacion_h"] = raw.loc[idx, "tiempo_reparacion_h"].map(lambda v: f"{v} h" if pd.notna(v) else v)
raw = pd.concat([raw, raw.sample(20, random_state=1)])   # 20 duplicados
raw.to_csv("mantenimiento_raw.csv", index=False)

df = pd.read_csv("mantenimiento_raw.csv")


# ============ 2. LIMPIEZA (con reporte antes / después) ============
def reporte(d, titulo):
    print(f"\n=== {titulo} ===")
    print("Filas:", len(d), "| Duplicados:", d.duplicated().sum())
    print("Nulos por columna:")
    print(d.isna().sum()[d.isna().sum() > 0].to_string())
    print("Tipos:", d.dtypes.astype(str).to_dict())

reporte(df, "ANTES")
print("Nombres de máquina distintos:", df["maquina"].nunique())

# a) Duplicados
df = df.drop_duplicates()

# b) Formato de texto
df["maquina"] = df["maquina"].str.strip().str.title()
df["tecnico"] = df["tecnico"].fillna("Sin registro")

# c) Tipos: fecha (2 formatos), tiempo de reparación (texto "3.5 h")
f1 = pd.to_datetime(df["fecha"], format="%Y-%m-%d", errors="coerce")
f2 = pd.to_datetime(df["fecha"], format="%d/%m/%Y", errors="coerce")
df["fecha"] = f1.fillna(f2)
df["tiempo_reparacion_h"] = pd.to_numeric(df["tiempo_reparacion_h"].astype(str).str.replace(" h", ""), errors="coerce")
df.loc[df["tiempo_reparacion_h"] <= 0, "tiempo_reparacion_h"] = np.nan   # valores inválidos

# d) Nulos: eliminar si falta la máquina; imputar con la mediana por tipo de falla
df = df.dropna(subset=["maquina_id"])
df["maquina_id"] = df["maquina_id"].astype(int)
for col in ["vibracion_mm_s", "temperatura_c", "tiempo_reparacion_h"]:
    df[col] = df[col].fillna(df.groupby("tipo_falla")[col].transform("median"))

reporte(df, "DESPUÉS")
print("Nombres de máquina distintos:", df["maquina"].nunique())

# ============ 3. DOS CONSULTAS (filtro + agregación) ============
# Q1: ¿Qué máquinas acumulan más horas de paro en 2025?
q1 = (df[df["fecha"].dt.year == 2025]
      .groupby("maquina")
      .agg(fallas=("registro_id", "count"), horas_paro=("tiempo_reparacion_h", "sum"))
      .sort_values("horas_paro", ascending=False).round(1))
print("\n--- Q1: fallas y horas de paro por máquina (2025) ---\n", q1)

# Q2: ¿Qué tipo de falla ocurre con vibración alta (> 6 mm/s) y cuánto tarda en repararse?
q2 = (df[df["vibracion_mm_s"] > 6]
      .groupby("tipo_falla")
      .agg(casos=("registro_id", "count"), reparacion_prom_h=("tiempo_reparacion_h", "mean"))
      .sort_values("casos", ascending=False).round(2))
print("\n--- Q2: fallas con vibración > 6 mm/s ---\n", q2)
