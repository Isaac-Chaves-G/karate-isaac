# Observación exploratoria: elemento de texto en Climatización

**Clasificación revisada el 16 de octubre de 2026:** comportamiento reproducible pendiente de especificación; **no es un bug confirmado**. La clasificación anterior como fallo de contrato fue demasiado concluyente.

El ejemplo formaba parte de TC22 y exigía HTTP 400 para `[true, "si", false]`. No se encontró una fuente independiente que obligue a devolver ese código para un elemento de texto. La respuesta de otras entradas incorrectas no basta para establecer ese requisito.

## Fuentes revisadas

- *Taller de técnicas de prueba de caja negra – Parte 2*, páginas 1–2: define las cuatro acciones funcionales de Climatización, sin política HTTP para tipos malformados.
- *Guia Karate framework v3* y *Taller Automatización pruebas backend con Karate framework*: explican automatización, cobertura y trazabilidad; no especifican ese rechazo.
- `materiales/clima-definicion.json`: enumera las tres condiciones y cuatro reglas; no contiene un esquema ni códigos de error.
- [Página pública de Climatización](https://taller-de-tecnicas-de-prueba-de-caja.onrender.com/decision.html?slug=climatizacion): envía booleanos desde `checkbox.checked` y muestra «Combinación sin regla definida» cuando `noDefinida` es verdadero. No determina qué código devolver para texto.

## Reproducción histórica conservada

Solicitud: `POST /api/decision/climatizacion/evaluar`, `Content-Type: application/json`:

```json
{"valores":[true,"si",false]}
```

Respuesta observada: HTTP **200** con:

```json
{"valores":[true,"si",false],"accion":null,"reglaIndex":null,"noDefinida":true}
```

Evidencia original: `evidencias/TC22-reproduccion.json`, `evidencias/features.climatizacion.xml` y `evidencias/resultados.json`. La repetición previa a la corrección de alcance está en `evidencias/auditoria-2026-10-16/`. Los resultados históricos de 43 correctas y 1 fallida se conservan sin modificarlos.

## Decisión de alcance

Se retiró **solo este ejemplo** de la regresión de TC22. No se cambió su expectativa a 200 ni se agregó un tag para omitirlo. TC22 conserva cinco estructuras inválidas y sus aserciones originales. La suite final tiene **43 ejecuciones**, no 44 pruebas aprobadas. Las 38 ejecuciones de reglas funcionales conservan toda su cobertura.

Antes de reincorporar el ejemplo como prueba de aceptación, el responsable de la API debe especificar si un tipo no booleano se rechaza mediante HTTP 400 o se devuelve como combinación sin regla. Hasta entonces no se presenta esta observación como fallo funcional ni como candidato confirmado a bonus.
