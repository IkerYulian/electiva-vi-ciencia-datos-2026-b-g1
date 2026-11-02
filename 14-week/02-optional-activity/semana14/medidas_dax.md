# Medidas DAX relacionadas con el indicador (ventas mensuales y su media móvil)

Estas dos medidas reproducen en Power BI lo que `serie_temporal.py` calcula con
`resample("MS").sum()` y `rolling(3).mean()`.

## Modelo de datos

| Tabla | Origen | Columnas |
|---|---|---|
| `Ventas` | `datos_diarios.csv` | `fecha` (fecha), `ventas` (decimal) |
| `Calendario` | DAX (abajo) | `Fecha`, `Anio`, `Mes`, `AnioMes` |

Relación: `Calendario[Fecha]` 1 → * `Ventas[fecha]`. Marcar `Calendario` como **tabla de fechas**
(Herramientas de tabla → Marcar como tabla de fechas → `Fecha`).

```dax
Calendario =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2022, 1, 1 ), DATE ( 2024, 12, 31 ) ),
    "Anio", YEAR ( [Date] ),
    "Mes", MONTH ( [Date] ),
    "AnioMes", FORMAT ( [Date], "YYYY-MM" )
)
```
> Renombra la columna `[Date]` a `Fecha` después de crearla. El calendario empieza en la
> primera fecha con datos para que la media móvil quede en blanco los 2 primeros meses, igual que en pandas.

## Medida 1 — Ventas Totales (métrica base)

```dax
Ventas Totales = SUM ( Ventas[ventas] )
```

Suma las ventas en el contexto de filtro actual. Con `Calendario[AnioMes]` en el eje de un
gráfico, devuelve la suma mensual (equivale a `resample("MS").sum()`).

## Medida 2 — Ventas MM 3M (media móvil de 3 meses)

```dax
Ventas MM 3M =
VAR UltimaFecha = MAX ( 'Calendario'[Fecha] )
VAR Ventana =
    DATESINPERIOD ( 'Calendario'[Fecha], UltimaFecha, -3, MONTH )
VAR MesesEnVentana =
    CALCULATE (
        DISTINCTCOUNT ( 'Calendario'[AnioMes] ),
        REMOVEFILTERS ( 'Calendario' ),
        Ventana
    )
VAR VentasVentana =
    CALCULATE ( [Ventas Totales], REMOVEFILTERS ( 'Calendario' ), Ventana )
RETURN
    IF ( MesesEnVentana = 3, DIVIDE ( VentasVentana, 3 ) )
```

### Explicación

1. `UltimaFecha` toma el último día del mes visible en el contexto (p. ej. 31-dic-2024).
2. `DATESINPERIOD(..., -3, MONTH)` construye la ventana de 3 meses que termina en esa fecha
   (1-oct a 31-dic).
3. `REMOVEFILTERS('Calendario')` elimina el filtro del mes actual; sin él, el visual
   restringiría la medida a un solo mes y la media móvil sería simplemente `Ventas Totales / 3`.
   La ventana se calcula en variables (antes de quitar filtros), por eso sigue anclada al mes visible.
4. `MesesEnVentana = 3` evita el defecto de dividir siempre entre 3: en los primeros 2 meses
   no hay ventana completa y la medida devuelve **BLANK**, igual que `rolling(3)` devuelve `NaN`.
5. `DIVIDE` evita errores de división por cero.

### Validación cruzada con Python (usando `datos_diarios.csv`)

| Mes | `Ventas Totales` | `Ventas MM 3M` | Valor en `serie_mensual.csv` |
|---|---|---|---|
| Ene-2022 | 3 834,8 | BLANK | mm3 = vacío |
| Mar-2022 | 3 280,3 | 3 460,0 | mm3 = 3460.0 |
| Dic-2024 | 5 542,3 | 5 251,1 | mm3 = 5251.1 |

Si tu tarjeta/visual muestra estos valores, la medida es correcta.

> **Nota honesta:** las medidas DAX no se pudieron ejecutar en este entorno (requieren Power BI Desktop).
> Los valores de la tabla provienen del cálculo equivalente en pandas; compruébalos en tu informe.
