# Hallazgo de contrato: falta de validación de booleanos

**Caso:** TC22, ejemplo «valor no booleano». Módulo: Climatización.

**Clasificación:** hallazgo reproducible de validación de entrada. La regla CLI-05 es una expectativa técnica adicional del contrato de tres booleanos; no es una regla funcional nueva atribuida al enunciado. No se afirma que la profesora haya inyectado este defecto ni que otorgue bonus.

## Reproducción

Enviar `POST /api/decision/climatizacion/evaluar` con `Content-Type: application/json`:

```json
{"valores":[true,"si",false]}
```

Esperado: HTTP 400 y rechazo de la entrada porque el segundo elemento es texto. La API utiliza el mensaje «Se esperaban 3 valores booleanos» al rechazar estructuras inválidas.

Observado: HTTP **200** con:

```json
{"valores":[true,"si",false],"accion":null,"reglaIndex":null,"noDefinida":true}
```

El servicio permite que un dato ajeno al dominio booleano llegue al evaluador y produzca una combinación sin regla, en lugar de rechazarlo como entrada inválida. Cinco variantes malformadas restantes sí devuelven 400.

**Evidencia:** fallo real en `evidencias/features.climatizacion.xml`, resumen `evidencias/resultados.json` y reproducción HTTP independiente `evidencias/TC22-reproduccion.json`.

**Tratamiento:** conservar la aserción `status 400`. El fallo no debe convertirse en éxito modificando la expectativa a 200. Si el responsable de la API especifica que admite tipos no booleanos, se deberá revisar expresamente el contrato y documentar esa decisión.
