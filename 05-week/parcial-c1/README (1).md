# Parcial C1 - Ciencia de Datos

## Caso seleccionado

Para este trabajo se eligió una tienda de ropa llamada **ModaJoven**, que vende ropa casual para jóvenes. La tienda tiene un local físico donde se hacen las ventas del día a día, y además recibe pedidos a través de su página de Instagram y un formulario en su página web. El dueño quiere empezar a usar los datos que genera el negocio para tomar mejores decisiones, por ejemplo saber qué se vende más y qué se podría vender en el futuro.

## 1. Tipos de datos y su clasificación

| Tipo de dato | Ejemplo en ModaJoven | Clasificación |
|---|---|---|
| Registro de ventas del local | Excel con fecha, producto, talla, color, precio y cantidad vendida | Estructurado |
| Pedidos del formulario de la página web | Tiene campos como nombre y producto, pero también un espacio de comentario libre | Semiestructurado |
| Fotos de la ropa publicadas en Instagram | Imágenes de los productos que se suben a redes sociales | No estructurado |
| Comentarios de clientes en las publicaciones | Texto libre que escribe cada cliente opinando sobre la ropa | No estructurado |

## 2. Preguntas de analítica

**Pregunta descriptiva:** ¿Cuál fue la prenda más vendida en ModaJoven durante el último mes?

**Pregunta predictiva:** Según la tendencia de ventas, ¿cuántas unidades de esa prenda se deberían comprar para el próximo mes?

## 3. Diagrama del proceso de datos

```
Fuente  →  Almacenamiento  →  Análisis  →  Visualización
```

| Etapa | Cómo se aplica en ModaJoven |
|---|---|
| Fuente | Ventas del local, pedidos de la página web, comentarios en Instagram |
| Almacenamiento | Excel o una base de datos en la nube donde se guarda todo |
| Análisis | Se revisan las ventas para saber qué prendas y tallas se venden más |
| Visualización | Gráficas simples que muestran las ventas por mes o por producto |

## 4. Descriptive vs Predictive Analytics

Descriptive analytics looks at data from the past to understand what already happened, for example the sales from last month.

Predictive analytics uses that same data to try to guess what could happen in the future, like how many products the store will sell next month.
