# Lista de entrega

| Exigencia | Evidencia | Estado |
|---|---|---|
| Un ejercicio por bloque | Barista Bot y Climatización, elecciones del estudiante | Implementado |
| Al menos diez escenarios con issues | 22 escenarios, 44 ejecuciones, issues #1–#22 y tags GH reales | Publicados y verificados |
| Todas las transiciones válidas y negativas | Matriz 5×6, 8 válidas y 22 inválidas | 30/30 pasan localmente |
| Tabla de decisión | Ocho combinaciones, cuatro acciones | 8/8 pasan localmente |
| Reportes | HTML Karate, JSON Cucumber y XML | Generados; 43 pasan y 1 falla |
| Repositorio | https://github.com/Isaac-Chaves-G/karate-isaac | Publicado en main |
| Actions y ejecución por issue | ci.yml, filtro GH-N y label ejecutar-prueba | Suite remota ejecutada; GH-1 probado individualmente; disparo por clic en label pendiente de comprobar |
| Actualizar issues | Comentario y labels automated-passed/automated-failed por caso | 22 comentarios verificados; 21 casos pasan y TC22 falla |
| GitHub Project vinculado | Project personal #3 creado por el estudiante | Incorporación de los 22 casos y enlace al repositorio pendientes de confirmar |
| Sustentación oral | SUSTENTACION.md | Preparada |

El pipeline original encontrado en Descargas está preservado en `materiales/ci-profesora.yml`; las adaptaciones del pipeline activo están explicadas en el README. No se han alterado los PDF originales.

Enlaces:

- [Repositorio](https://github.com/Isaac-Chaves-G/karate-isaac).
- [22 issues](https://github.com/Isaac-Chaves-G/karate-isaac/issues).
- [Publicación exitosa de los casos](https://github.com/Isaac-Chaves-G/karate-isaac/actions/runs/38814281639).
- [Suite remota y reporte](https://github.com/Isaac-Chaves-G/karate-isaac/actions/runs/38814432411).
- [Project #3 proporcionado por el estudiante](https://github.com/users/Isaac-Chaves-G/projects/3/views/1).

El estudiante autorizó el acceso al navegador. El controlador falló al inicializarse con «failed to write kernel assets: El sistema no puede encontrar la ruta especificada»; falló también después de reiniciarlo y con el controlador alternativo. No se pudo inspeccionar ni modificar el Project desde esa herramienta. La consulta sin sesión devuelve HTTP 404, lo que no demuestra que el Project no exista.

Para incorporar todos los casos de una vez: abrir Issues del repositorio, seleccionar la casilla superior de los 22 issues, abrir Projects y elegir el Project #3. Si no aparece en Projects del repositorio, usar Link a project allí. [Procedimiento oficial de GitHub](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-items-in-your-project/adding-items-to-your-project).
