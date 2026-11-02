-- =====================================================================
-- Optimizacion SQL (PostgreSQL 16): ventas mensuales de un anio
-- Indicador relacionado con el analisis en Python: suma mensual de ventas
-- (equivale a serie.resample("MS").sum()).
-- Prueba: tabla `ventas` de 3.000.000 filas (ver setup_datos.sql).
-- =====================================================================

-- ---------- ANTES: NO sargable ----------
-- EXTRACT(YEAR FROM fecha) aplica una funcion a la columna filtrada: el motor
-- debe evaluarla fila por fila, no puede usar un indice sobre `fecha`
-- y recorre toda la tabla (Seq Scan sobre 3M de filas).
SELECT EXTRACT(MONTH FROM fecha) AS mes,
       SUM(monto)                AS ventas
FROM   ventas
WHERE  EXTRACT(YEAR FROM fecha) = 2024
GROUP  BY EXTRACT(MONTH FROM fecha);

-- ---------- DESPUES: sargable + indice cubriente ----------
-- 1) Indice con `fecha` como clave de busqueda e INCLUDE (monto): el indice
--    contiene todas las columnas que la consulta necesita (indice "cubriente").
CREATE INDEX idx_ventas_fecha_monto ON ventas (fecha) INCLUDE (monto);
VACUUM ANALYZE ventas;   -- actualiza visibility map (necesario para Index Only Scan) y estadisticas

-- 2) Predicado como rango sobre la columna "desnuda" + date_trunc para agrupar.
SELECT date_trunc('month', fecha) AS mes,
       SUM(monto)                 AS ventas
FROM   ventas
WHERE  fecha >= DATE '2024-01-01'
  AND  fecha <  DATE '2025-01-01'     -- limite superior exclusivo: incluye todo 31-dic
GROUP  BY 1
ORDER  BY 1;

-- ---------- Evidencia ----------
-- EXPLAIN (ANALYZE, BUFFERS) <consulta>;
-- Resultados completos en evidencia_explain.txt
