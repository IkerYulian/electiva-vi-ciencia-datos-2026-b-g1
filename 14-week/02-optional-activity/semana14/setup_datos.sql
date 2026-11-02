-- Tabla de transacciones de prueba: 3 millones de filas entre 2020 y 2024
DROP TABLE IF EXISTS ventas;
CREATE TABLE ventas (
    id        bigserial PRIMARY KEY,
    fecha     date          NOT NULL,
    cliente   int           NOT NULL,
    monto     numeric(10,2) NOT NULL
);

SELECT setseed(0.42);
INSERT INTO ventas (fecha, cliente, monto)
SELECT DATE '2020-01-01' + (random() * 1825)::int,      -- 2020-01-01 .. 2024-12-30
       (random() * 5000)::int,
       round((random() * 200 + 10)::numeric, 2)
FROM generate_series(1, 3000000);

ANALYZE ventas;
