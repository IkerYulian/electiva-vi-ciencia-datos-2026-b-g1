# Semana 4 – Inventario de datos y ciclo de vida del proyecto



## 1. Problema y pregunta de datos

**Proceso de negocio:** Mantenimiento de maquinaria en una línea de producción industrial.

**Problema:** Las máquinas de la línea de ensamble presentan fallas inesperadas que generan paros no planificados, afectando la producción y aumentando los costos de reparación de emergencia.

**Pregunta de datos:** ¿Es posible predecir con anticipación qué máquinas tienen mayor probabilidad de fallar en los próximos 7 días, usando datos históricos de sensores y mantenimiento, para programar mantenimiento preventivo antes de que ocurra la falla?

## 2. Inventario de datos

| # | Fuente / Campo | Tipo | Descripción |
|---|-----------------|------|-------------|
| 1 | Registros de mantenimiento (BD relacional) | Estructurado | Fecha, máquina, tipo de falla, técnico, tiempo de reparación |
| 2 | Órdenes de producción (ERP) | Estructurado | Máquina asignada, turno, cantidad producida, tiempos de parada |
| 3 | Sensores IoT de vibración y temperatura | Semiestructurado | Lecturas en formato JSON / series de tiempo cada pocos segundos por máquina |
| 4 | Datos climáticos de la planta (API externa) | Semiestructurado | Temperatura y humedad ambiente en formato JSON |
| 5 | Manuales técnicos de las máquinas | No estructurado | Documentos PDF con especificaciones y umbrales de operación |
| 6 | Reportes de los operarios | No estructurado | Texto libre describiendo anomalías observadas durante el turno |
| 7 | Imágenes de inspección visual | No estructurado | Fotos/video de piezas desgastadas tomadas en inspecciones periódicas |

## 3. Tipo de analítica

Este proyecto recorre las cuatro etapas de la analítica:

- **Descriptiva:** dashboards con historial de fallas por máquina y línea (qué ha pasado).
- **Diagnóstica:** análisis de correlación entre variables de sensores y fallas pasadas (por qué pasó).
- **Predictiva:** modelos de machine learning (clasificación o series de tiempo) que estiman la probabilidad de falla en los próximos días (qué va a pasar).
- **Prescriptiva:** recomendación de cuándo y en qué máquina programar mantenimiento preventivo, priorizando por riesgo y costo (qué se debería hacer).

El objetivo final del proyecto es **prescriptivo** (recomendar una acción concreta de mantenimiento), pero para llegar ahí es necesario construir primero las capas descriptiva, diagnóstica y predictiva.

**¿Es un caso de Big Data? Sí.** Se justifica con las V's:

- **Volumen:** miles de lecturas de sensores por segundo, multiplicadas por decenas de máquinas.
- **Velocidad:** los datos de sensores llegan en tiempo real / streaming continuo.
- **Variedad:** conviven datos estructurados (BD, ERP), semiestructurados (JSON de sensores) y no estructurados (texto, imágenes, PDF).
- **Veracidad:** los sensores pueden generar ruido o lecturas erróneas que deben limpiarse antes de analizar.
- **Valor:** predecir fallas a tiempo reduce paros no planificados y costos de reparación de emergencia.

## 4. Ciclo de vida del proyecto

```mermaid
flowchart LR
    A["Pregunta:<br/>¿Qué máquinas fallarán<br/>en los próximos 7 días?"] --> B["Obtener:<br/>Extraer datos de sensores,<br/>ERP y mantenimiento"]
    B --> C["Limpiar:<br/>Filtrar ruido de sensores,<br/>unificar formatos y unir fuentes"]
    C --> D["Analizar:<br/>Modelos predictivos de<br/>probabilidad de falla"]
    D --> E["Visualizar:<br/>Dashboard de riesgo<br/>por máquina"]
    E --> F["Decidir:<br/>Programar mantenimiento<br/>preventivo priorizado"]
```

1. **Pregunta:** definir qué se quiere predecir (probabilidad de falla por máquina).
2. **Obtener:** extraer datos de las 7 fuentes del inventario.
3. **Limpiar:** eliminar valores atípicos de sensores, estandarizar unidades, unir tablas por máquina y fecha.
4. **Analizar:** entrenar y validar el modelo predictivo.
5. **Visualizar:** mostrar el riesgo de falla en un tablero para los supervisores de mantenimiento.
6. **Decidir:** priorizar y programar el mantenimiento preventivo según el riesgo estimado.

## Problem & Data (English – required section, min. 5 sentences)

Manufacturing lines often experience unplanned equipment downtime caused by unexpected mechanical failures, which increases repair costs and disrupts production schedules. This project aims to determine whether it is possible to predict, in advance, which machines are most likely to fail within the next seven days by analyzing historical maintenance and sensor data. The data required includes structured maintenance and production records, semi-structured IoT sensor readings such as vibration and temperature, and unstructured sources like technician notes, equipment manuals, and inspection images. Because sensors continuously generate large volumes of data at high speed from many machines, this project qualifies as a Big Data problem. The analytics approach will move from descriptive dashboards of past failures to predictive models that estimate failure probability, and finally to prescriptive recommendations for scheduling preventive maintenance.

