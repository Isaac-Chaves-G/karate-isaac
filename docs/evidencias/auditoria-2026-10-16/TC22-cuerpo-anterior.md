# TC22: Rechazar un contrato de entrada inválido - <caso>

Requisito: @REQ-CLI-05.

Archivo: `src/test/resources/features/climatizacion.feature`.

## Precondiciones y resultado esperado

Barista se reinicia y alcanza su estado inicial mediante `barista-state.feature`; no depende del caso anterior. Climatización recibe tres booleanos: temperatura alta, presencia y apertura prolongada.

```gherkin
Scenario Outline: Rechazar un contrato de entrada inválido - <caso>
Given path 'decision', 'climatizacion', 'evaluar'
    And request <payload>
    When method post
    Then status 400
    And match response.error == 'Se esperaban 3 valores booleanos'

    Examples:
      | caso             | payload                           |
      | campo ausente    | {}                                |
      | lista vacía      | { valores: [] }                   |
      | faltan valores   | { valores: [true, false] }        |
      | sobran valores   | { valores: [true,true,true,true] } |
      | valor nulo       | { valores: null }                 |
      | valor no booleano | { valores: [true, 'si', false] }  |
```

## Ejecución

Añade la etiqueta **ejecutar-prueba** a este issue, o abre Actions → Karate API → Run workflow y escribe `@GH-22`. Para repetir desde el issue, quita la etiqueta y vuelve a añadirla.

Local: `./gradlew clean test '-Dkarate.options=--tags @GH-22'`.

## Evidencia

El workflow publica el resultado y el enlace a la corrida en este issue, y actualiza `automated-passed` o `automated-failed`. Descarga `karate-reports-N` en Artifacts y abre `karate-summary.html`. Un fallo no demuestra por sí solo un bug: revisa la respuesta y las precondiciones.
