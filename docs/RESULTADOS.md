# Resultados de ejecución

## Resultado final local del 16 de octubre de 2026

Después de corregir el filtro y retirar la expectativa sin especificación, `gradlew.bat clean test --console=plain` terminó **BUILD SUCCESSFUL**. Se ejecutaron **43 pruebas, 43 correctas y 0 fallidas**, agrupadas en 22 casos; no faltó evidencia de ningún caso.

| Alcance final | Ejecuciones | Correctas | Fallidas |
|---|---:|---:|---:|
| Barista Bot | 30 | 30 | 0 |
| Climatización, reglas funcionales | 8 | 8 | 0 |
| Climatización, rechazo estructural adicional | 5 | 5 | 0 |
| Total | **43** | **43** | **0** |

Evidencia final: `evidencias/auditoria-2026-10-16/final/resultados-suite.json`, los XML originales de ambos módulos y `karate-summary-json.txt`. Esta ejecución no convierte en aprobada la prueba retirada: la suite anterior tenía 44 ejecuciones y la actual tiene 43.

También pasan 10 pruebas de soporte: 8 sobre selección de tags y 2 sobre sincronización de cuerpos de issues, incluida la conservación de notas manuales. La publicación de la revisión en GitHub y su ejecución remota se verifican por separado.

## Auditoría del 16 de octubre de 2026

Se revisaron todas las expectativas contra las reglas de los materiales: 30 pares estado/evento de Barista y las 8 combinaciones de Climatización. La primera repetición local de la suite original produjo **43 correctas y 1 fallida, sin casos sin evidencia**. TC13 ejecutó sus **5 ejemplos correctamente**. Este resultado histórico corresponde al alcance anterior de 44 ejecuciones.

El fallo de GitHub con `@tc13` del 15 de octubre ocurrió en **Resolver y validar tag**; el paso **Ejecutar Karate** quedó omitido. El selector admitía solo `TC` en mayúsculas. Se corrigió la normalización sin distinguir mayúsculas y minúsculas y se agregaron 8 pruebas del selector que cubren los 22 casos, sus issues, filtros de módulo, nombres inválidos y entradas vacías. `@tc13`, `Tc13` y `TC13` ahora seleccionan `@TC13`; un caso inexistente sigue rechazándose. Una ejecución individual usando `normalize_tag('@tc13')` confirmó **5 correctas y 0 fallidas** con Gradle exitoso.

Al revisar el único fallo, se encontró que exigir HTTP 400 para `[true, "si", false]` no tenía una fuente contractual independiente. Se retiró únicamente ese ejemplo de TC22 y se conservó su reproducción como observación exploratoria pendiente de especificación. No se cambió la aserción a 200 ni se marcó el ejemplo como omitido. La suite final tiene **43 ejecuciones**; las 38 ejecuciones de reglas funcionales mantienen su cobertura completa. La atribución anterior de este fallo como bug confirmado se corrige en [DEFECTOS.md](DEFECTOS.md).

Evidencia nueva en `evidencias/auditoria-2026-10-16/`: `resultados-suite.json`, los dos XML originales, `karate-summary-json.txt`, `resultados-TC13.json` y los pasos del fallo remoto anterior en `ci-selector-anterior.json`. La validación de la versión corregida en GitHub se registra por separado una vez finalizada; la ejecución local no la sustituye.

## Ejecución inicial

Ejecución local real del 15 de octubre de 2026, Windows, JDK 21.0.7, Gradle 8.14.3, Karate 1.4.1, contra la API pública indicada en la guía.

Comando: `gradlew.bat clean test --console=plain`.

| Módulo | Ejecuciones | Correctas | Fallidas |
|---|---:|---:|---:|
| Barista Bot | 30 | 30 | 0 |
| Climatización, reglas funcionales | 8 | 8 | 0 |
| Climatización, entradas inválidas | 6 | 5 | 1 |
| Total | **44** | **43** | **1** |

Los 22 casos se ejecutaron. 21 casos completos pasan; TC22 tiene cinco ejemplos correctos y uno fallido. Ningún caso se omitió. El runner JUnit agrupa toda la suite en un método: su «1 test failed» no significa que se ejecutó un solo escenario; el desglose real está en los reportes Karate/Cucumber.

En esta ejecución histórica, Gradle terminó con código 1 por la aserción de TC22 que luego se determinó que carecía de especificación. El reporte HTML se generó igualmente. Ver la revisión de alcance en [DEFECTOS.md](DEFECTOS.md).

Evidencia conservada:

- `evidencias/resultados.json`: conteo por caso, errores y lista de casos sin evidencia (vacía).
- `evidencias/features.barista.xml` y `features.climatizacion.xml`: XML original generado por Karate.
- `evidencias/karate-summary-json.txt`: resumen original del framework.
- `evidencias/TC22-reproduccion.json`: repetición independiente del payload problemático.

## Verificación histórica en GitHub Actions

[Ejecución remota original](https://github.com/Isaac-Chaves-G/karate-isaac/actions/runs/38814432411): 43 ejecuciones correctas y 1 fallida, coincidiendo con el resultado local anterior. Los 22 issues recibieron comentarios: 21 casos con `automated-passed` y TC22 con `automated-failed` (cinco ejemplos pasaron y uno falló). El paso de actualización de issues y el de subida de reportes finalizaron correctamente. Este FAILED conserva una aserción histórica cuyo requisito se revisó; no prueba un bug de la API.

Artefacto: `karate-reports-2`. La verificación de comentarios y metadatos se conserva en `evidencias/ci-verificacion.json`.

Se ejecutó además `gradlew.bat clean test '-Dkarate.options=--tags @GH-1'`: seleccionó solo TC01, que pasó. Esta comprobación valida el filtro de números reales usado por el workflow; no se presenta como una ejecución disparada por un clic en Labels. El reporte completo de 44 ejecuciones se archivó antes de esta prueba individual.
