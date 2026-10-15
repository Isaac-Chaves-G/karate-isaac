# Taller backend con Karate: Barista Bot y Climatización

Proyecto individual de Isaac Chaves. Una sola entrega integra la guía técnica y el taller: **22 escenarios y 44 ejecuciones**, incluidos los ejemplos de los `Scenario Outline`.

- Bloque 1: Barista Bot, 8 transiciones válidas y 22 inválidas (todas las celdas de 5 estados × 6 eventos).
- Bloque 2: Climatización, las 8 combinaciones de 3 condiciones y 6 entradas malformadas adicionales.
- Requisitos y cobertura: [DISEÑO.md](docs/DISEÑO.md).
- Casos e issues: [TRAZABILIDAD.md](docs/TRAZABILIDAD.md).
- Resultados verificados: [RESULTADOS.md](docs/RESULTADOS.md).
- Explicación para la sustentación: [SUSTENTACION.md](docs/SUSTENTACION.md).

## Ejecución local

Requisitos: JDK 21 y acceso a Internet. Gradle 8.14.3 se descarga con el wrapper incluido; no se necesita instalar Gradle, navegador, Selenium ni escribir Step Definitions.

Desde esta carpeta, en PowerShell:

```powershell
$env:JAVA_HOME = 'C:\Program Files\Java\jdk-21'
.\gradlew.bat clean test
.\gradlew.bat clean test '-Dkarate.options=--tags @TC01'
.\gradlew.bat clean test '-Dkarate.options=--tags @barista'
.\gradlew.bat clean test '-Dkarate.options=--tags @climatizacion'
.\gradlew.bat clean test '-Dkarate.options=--tags @smoketest'
```

En Git Bash/Linux: `bash ./gradlew clean test '-Dkarate.options=--tags @TC01'`.

Abrir `target/karate-reports/karate-summary.html`. Cada escenario muestra petición, respuesta y aserción. `clean` elimina la evidencia anterior; cada ejecución genera un reporte nuevo. Un filtro sin casos **falla**, evitando verdes falsos.

La URL está centralizada en `karate-config.js`. Para otra instancia compatible: `-Dapi.baseUrl=https://SERVIDOR/api`.

## Ejecutar desde GitHub Issues

1. Abre [los issues del repositorio](https://github.com/Isaac-Chaves-G/karate-isaac/issues).
2. Elige `[TCxx]` y añade la etiqueta **ejecutar-prueba**.
3. Abre [Actions → Karate API](https://github.com/Isaac-Chaves-G/karate-isaac/actions/workflows/ci.yml). El título de la ejecución identifica el caso.
4. Al terminar, el issue recibe un comentario con PASSED/FAILED, el enlace a la corrida y `automated-passed` o `automated-failed`. Los demás labels se conservan.
5. Descarga `karate-reports-N` en **Artifacts**, extrae el ZIP y abre el `karate-summary.html` dentro de `target/karate-reports`.
6. Para repetir, retira `ejecutar-prueba` y vuelve a añadirla.

Alternativa de la guía: **Actions → Karate API → Run workflow → testTag**, escribir `@GH-N` usando el número real del issue. También admite `TC01`, `barista`, `climatizacion`, `smoketest`, con o sin `@`. Vacío ejecuta todos.

`Publicar casos Karate` crea/reutiliza 22 issues, añade `@GH-N` a los escenarios y guarda el mapa. Al finalizar correctamente, dispara la suite con la trazabilidad actualizada. No inventa números ni usa tokens personales guardados en archivos.

## Estructura y decisiones técnicas

```text
src/test/java/runner/ApiTest.java       JUnit inicia Karate y propaga fallos
src/test/resources/karate-config.js    URL, headers y timeouts
src/test/resources/features/          Barista y Climatización
src/test/resources/helpers/           Preparación verificada del robot
scripts/catalog.py                   Catálogo y cuerpos de los issues
scripts/publish_cases.py             Publicación y tags reales
scripts/report_results.py            Resultado por caso a partir de Cucumber JSON
.github/workflows/ci.yml             Suite, filtro, evidencia y actualización de issues
```

Se conserva Karate **1.4.1** y Logback **1.5.6**, como en la guía. JDK 21, Gradle 8.14.3 y JUnit Platform Launcher 1.9.3 completan la configuración. El runner se llama `ApiTest` para evitar el conflicto entre una clase propia `Runner` y `com.intuit.karate.Runner` presente en el ejemplo.

Cada ejecución de Barista reinicia y establece su precondición mediante eventos válidos. `parallel(1)` y la concurrencia serial de Actions evitan que las ejecuciones de este repositorio se interfieran. La API no entrega un identificador de sesión: otras personas que prueben la misma instancia podrían alterar su estado. No ejecutar localmente mientras corre la suite remota.

Una transición inválida responde **HTTP 200**, `valida: false` y conserva el estado; por eso validar únicamente el código HTTP sería insuficiente. Climatización recibe booleanos, no grados ni minutos: este contrato no permite verificar directamente los límites numéricos de los sensores.

## Adaptación de los materiales

El `ci.yml` encontrado en Descargas se conserva sin cambios en `docs/materiales/ci-profesora.yml`. El pipeline activo mantiene JDK 21, Gradle, filtro `testTag` y artefactos. Añade selección desde issues, comentarios/resultados por caso, permisos mínimos y rutas correctas de resultados Gradle (`build/test-results`). Se fijó Ubuntu 24.04 para no cambiar de sistema base durante la entrega.

La guía usa tanto `@Issue-N` como `@GH-N`; se unificó en **@GH-N**, que es el formato explicado en su flujo de actualización. Los marcadores `[cite: 2]` de los ejemplos son texto del PDF, no sintaxis Karate. El pipeline original no incluye la actualización de issues descrita en la guía; se implementó aquí.

El tablero **GitHub Project** exigido por el taller es adicional a los issues: ver [ENTREGA.md](docs/ENTREGA.md) para su estado. No se da por creado solamente porque existan los issues.

Fuentes técnicas: [Karate 1.4.1](https://github.com/karatelabs/karate/tree/v1.4.1), [autenticación nativa de Actions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).
