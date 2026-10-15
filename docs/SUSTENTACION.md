# Cómo explicar y demostrar el taller

## Recorrido de ejecución

1. El comando Gradle `test` inicia JUnit 5.
2. `ApiTest` busca los archivos de `classpath:features`, aplica el filtro de tags y ejecuta un solo hilo.
3. Antes de cada escenario, `karate-config.js` entrega URL, headers y tiempos de espera.
4. El `.feature` arma una petición con `path` y `request`; `method` la envía.
5. `status` verifica HTTP y `match` verifica los valores de negocio de la respuesta.
6. Karate genera HTML, JSON Cucumber y XML JUnit. El runner falla si no hay escenarios o hay errores.
7. En Actions, el JSON permite agrupar todos los ejemplos de un TC. Un ejemplo fallido marca el issue completo como fallido.

## Explicación con TC06

TC06 comprueba que perder ingredientes mientras se calienta el agua detiene el proceso. El helper reinicia a En Espera, envía Iniciar Pedido y Terminar Molienda, verificando cada paso. El caso envía Sin Ingredientes y exige Error de Insumos, `valida: true` e Interrumpir flujo. Finalmente consulta el estado para comprobar que quedó guardado.

La precondición no depende de ejecutar TC01 y TC02 previamente: por eso TC06 puede lanzarse solo desde GitHub.

## Explicación con TC21

El payload `[true, true, true]` representa temperatura alta, personas y apertura prolongada. Aunque temperatura y presencia normalmente encenderían el aire, las ventanas tienen prioridad. La respuesta debe ser Apagar sistema de climatización y emitir alerta sonora, regla 0. Así se verifica la prioridad y no únicamente HTTP 200.

## Conceptos que pueden preguntar

- **Feature:** agrupa el comportamiento de un módulo; hay exactamente dos módulos seleccionados.
- **Scenario:** caso concreto. **Scenario Outline:** plantilla que se ejecuta una vez por fila de Examples.
- **Background:** preparación común de cada ejecución. Los helpers evitan repetir rutas de preparación extensas.
- **Tag @REQ-BAR-05:** requisito. **@TC06:** identificador estable de caso. **@GH-N:** número real del issue. Cada uno cumple una función distinta.
- **Prueba negativa:** pasa cuando el sistema rechaza correctamente algo inválido. No equivale a prueba fallida.
- **Estado vs decisión:** Barista depende del estado anterior; Climatización decide a partir de tres entradas de la petición.
- **Cobertura:** Barista 5×6=30 pares, 8 válidos+22 inválidos; Climatización 2³=8 combinaciones, aunque solo hay cuatro acciones/reglas simplificadas.
- **44 ejecuciones vs 22 issues:** cada outline es un caso con múltiples datos. El issue agrupa todos sus ejemplos.
- **Karate vs Serenity:** Karate ya implementa HTTP y aserciones; no necesita Step Definitions, Actor, Tasks ni navegador.

## Demostración en clase

1. Abrir un issue y localizar su tag `@GH-N` en el `.feature`.
2. Añadir `ejecutar-prueba` o lanzar Run workflow con ese tag.
3. Ver el comentario, el estado automatizado y el reporte con request/response.
4. Explicar la expectativa usando DISEÑO.md, no decir simplemente «el programa devuelve eso».
5. Si piden cambiar un dato, explicar qué cambia en la tabla antes de editar. Cambiar V de false a true obliga a esperar la alerta, aunque T y P sean true.

Si falla una prueba, revisar primero si falló la preparación, la conexión, el código HTTP o la aserción de negocio. Solo la última con evidencia reproducible permite argumentar un defecto funcional.
