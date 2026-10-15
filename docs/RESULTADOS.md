# Resultados de ejecución

Ejecución local real del 15 de octubre de 2026, Windows, JDK 21.0.7, Gradle 8.14.3, Karate 1.4.1, contra la API pública indicada en la guía.

Comando: `gradlew.bat clean test --console=plain`.

| Módulo | Ejecuciones | Correctas | Fallidas |
|---|---:|---:|---:|
| Barista Bot | 30 | 30 | 0 |
| Climatización, reglas funcionales | 8 | 8 | 0 |
| Climatización, entradas inválidas | 6 | 5 | 1 |
| Total | **44** | **43** | **1** |

Los 22 casos se ejecutaron. 21 casos completos pasan; TC22 tiene cinco ejemplos correctos y uno fallido. Ningún caso se omitió. El runner JUnit agrupa toda la suite en un método: su «1 test failed» no significa que se ejecutó un solo escenario; el desglose real está en los reportes Karate/Cucumber.

Gradle termina con código 1 porque conserva el fallo real de TC22. El reporte HTML se genera igualmente. Ver [DEFECTOS.md](DEFECTOS.md).

Evidencia conservada:

- `evidencias/resultados.json`: conteo por caso, errores y lista de casos sin evidencia (vacía).
- `evidencias/features.barista.xml` y `features.climatizacion.xml`: XML original generado por Karate.
- `evidencias/karate-summary-json.txt`: resumen original del framework.
- `evidencias/TC22-reproduccion.json`: repetición independiente del payload problemático.

Los resultados locales no sustituyen una ejecución de Actions. Sus enlaces verificados se registran en ENTREGA.md tras la publicación.
