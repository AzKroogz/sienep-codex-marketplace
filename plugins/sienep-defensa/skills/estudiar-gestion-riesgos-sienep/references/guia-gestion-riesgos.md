# Guía de Gestión de Riesgos SIENEP

## Contenido

1. [Alcance y reglas de lectura](#alcance-y-reglas-de-lectura)
2. [Conceptos indispensables](#conceptos-indispensables)
3. [Campos de la matriz](#campos-de-la-matriz)
4. [Evolución histórica](#evolución-histórica)
5. [Catálogo de riesgos 1–16](#catálogo-de-riesgos-116)
6. [Decisiones defendibles](#decisiones-defendibles)
7. [Inconsistencias que deben reconocerse](#inconsistencias-que-deben-reconocerse)
8. [Qué cuenta como evidencia](#qué-cuenta-como-evidencia)
9. [Banco graduado de preguntas](#banco-graduado-de-preguntas)

## Alcance y reglas de lectura

Fuente histórica de solo lectura: `Planilla de Gestión de Riesgos .xlsx`, observada el 19 de julio de 2026. Contiene una gráfica, pestañas Sprint 2 a Sprint 5 y una lista de valores. Esta guía conserva sus datos aunque sean discutibles; no los reemplaza por el estado actual de GNS3 ni del backend.

Usar cuatro etiquetas:

- **Dato**: aparece en la planilla.
- **Cálculo**: resultado reproducible a partir de datos visibles.
- **Evidencia**: observación que contrasta una afirmación.
- **Inferencia**: interpretación no asentada expresamente.

Separar siempre:

- **Infraestructura**: GNS3, configuraciones, appliances, ACL, conectividad, documentación de red.
- **Programación**: backend, JWT, roles, endpoints, README y repositorio cuando corresponda.
- **Proyecto transversal**: tiempo, equipo, asignación, matriz, conocimiento y recursos compartidos.

Un ejemplo técnico sigue siendo un caso de Gestión de Riesgos. Los comandos de red, pruebas HTTP o tests automatizados sólo aportan evidencia; no sustituyen la explicación de decisión, exposición y residual.

## Conceptos indispensables

### Riesgo

Evento o condición incierta que, si ocurre, afecta un objetivo. Conviene redactarlo como **condición → consecuencia**. No es lo mismo que un problema ya ocurrido: `Materializado` indica que la incertidumbre se convirtió en incidencia o efecto observable, aunque la planilla usa estados con cierta inconsistencia.

### Riesgo de producto y de proyecto

- **Producto**: amenaza cualidades o funcionamiento del entregable, por ejemplo compatibilidad de appliances o autorización de endpoints.
- **Proyecto**: amenaza ejecución, coordinación, plazo, trazabilidad o capacidad de entrega, por ejemplo tiempo limitado o tareas sin responsable.

La clasificación describe qué objetivo recibe el efecto, no si la causa es “técnica”. Las filas 4 y 14 están rotuladas como producto aunque describen disponibilidad/abandono de integrantes; se conserva el dato y se señala que conceptualmente parecen riesgos de proyecto.

### Probabilidad, impacto y exposición

- **Probabilidad (P)**: posibilidad estimada de ocurrencia.
- **Impacto (I)**: gravedad de la consecuencia.
- **Exposición (E)**: prioridad cuantitativa usada por la matriz: `E = P × I`.

La lista de valores presenta `3 Alto`, `2 Medio`, `1 Bajo`, `0 Cerrado`. Es razonable leerla como escala ordinal para P e I, pero la planilla no documenta umbrales adicionales para clasificar el producto E; no inventarlos.

Ejemplo correcto: `P = 2`, `I = 3`, por tanto `E = 2 × 3 = 6`.

### Exposición inicial y riesgo residual

La exposición inicial se estima antes del tratamiento. El **riesgo residual** es lo que permanece después: puede conservar parte de P o I, introducir otra dependencia o carecer todavía de evidencia. “Cerrado” no demuestra por sí solo residual cero.

### Mitigación, contingencia y disparador

- **Mitigación preventiva**: se aplica antes de la materialización para reducir P, I o ambas.
- **Contingencia reactiva**: se ejecuta al cumplirse un disparador para limitar el daño o recuperar operación.
- **Disparador**: condición observable que activa la contingencia.

Ejemplo: optimizar RAM y validar por etapas es preventivo; mover la ejecución al servidor compartido ante lentitud puede funcionar como contingencia. Restaurar un backup después de pérdida es contingencia; generar y verificar backups antes es mitigación.

### Abordajes

La lista admite `Asumir`, `Reducir`, `Compartir`, `Transferir` y `Eliminar`.

- **Asumir**: aceptar la exposición y vigilarla.
- **Reducir**: disminuir P o I.
- **Compartir**: repartir responsabilidad o consecuencias con otras partes.
- **Transferir**: desplazar contractualmente u operativamente parte del riesgo a un tercero capaz de gestionarlo.
- **Eliminar**: quitar la causa o actividad que origina el riesgo.

No validar el nombre sólo porque figura en la celda: contrastarlo con la acción real.

### Estados y seguimiento

La lista incluye `Identificado`, `Planificado`, `Materializado` y `Cerrado`. Cada fila agrega responsable, fecha comprometida, seguimiento, cambio respecto del sprint anterior, evidencia y próximo monitoreo. Un buen seguimiento explica qué cambió, por qué cambia P o I, qué se observó y qué queda abierto.

La lista también enumera los macroprocesos `Setup`, `Prestación` y `Cierre`, aunque las matrices de sprint no incluyen una columna de macroproceso. No asignar cada riesgo a uno sin una regla documentada: cualquier mapeo sería inferencia.

## Campos de la matriz

| Campo | Pregunta que responde | Control de calidad |
|---|---|---|
| ID | ¿Qué riesgo seguimos? | Mantener identidad entre sprints. |
| Descripción | ¿Qué condición causa qué consecuencia? | Evitar frases sin consecuencia. |
| Tipo | ¿Afecta producto o proyecto? | Contrastar etiqueta con objetivo afectado. |
| Probabilidad | ¿Cuán posible es? | Justificar cambios con evidencia. |
| Impacto | ¿Cuán grave sería? | No bajarlo sólo porque no ocurrió. |
| Exposición | ¿Cuál es la prioridad `P × I`? | Recalcular siempre. |
| Estado | ¿En qué situación está? | No equiparar “cerrado” con “demostrado”. |
| Abordaje | ¿Qué estrategia se eligió? | Comparar nombre y acción real. |
| Plan de mitigación | ¿Qué se hace preventivamente? | Indicar dimensión objetivo. |
| Responsable/fecha | ¿Quién actúa y cuándo? | Evitar responsables vagos si se necesita rendición. |
| Contingencia | ¿Qué se hace si ocurre? | Debe responder al efecto real. |
| Disparador | ¿Cuándo se activa? | Debe ser observable y pertenecer a esa fila. |
| Seguimiento/cambio | ¿Qué pasó desde el sprint anterior? | Explicar causalidad, no sólo actividad. |
| Evidencia | ¿Cómo se comprueba? | Exigir artefacto y resultado reproducible. |
| Próximo monitoreo | ¿Cuándo se vuelve a evaluar? | Mantenerlo aun con residual. |

## Evolución histórica

La gráfica declara:

| Sprint | Exposición total publicada | Variación publicada |
|---|---:|---:|
| 2 | 65 | — |
| 3 | 31 | −34 |
| 4 | 28 | −3 |
| 5 | 24 | −4 |

**Dato**: la narrativa de la gráfica atribuye la reducción a respaldos, servidor GNS3 centralizado, validación de appliances, tableros, documentación y pruebas, y afirma que en Sprint 5 la mayoría de los riesgos fueron mitigados o cerrados.

**Inferencia defendible**: la tendencia publicada sugiere priorización y seguimiento progresivos.

**Límite obligatorio**: no afirmar que la reducción prueba causalidad o efectividad. Los detalles actuales de filas, fórmulas y valores cacheados no reproducen todos esos totales. Se puede defender la evolución como registro histórico y simultáneamente reconocer que necesita saneamiento y recálculo.

## Catálogo de riesgos 1–16

La notación `P/I/E` transcribe cada pestaña. `—` significa que la fila aún no existía.

| ID | Riesgo resumido | Tipo registrado / área | S2 → S3 → S4 → S5 (`P/I/E`) | Decisión, evidencia y límite principal |
|---:|---|---|---|---|
| 1 | Hardware insuficiente para topología GNS3 | Producto técnico / Infraestructura | `3/3/9 → 2/3/6 → 2/3/6 → 2/3/6` | Optimizar appliances/RAM; servidor compartido. “Mejor funcionamiento” es vago; queda capacidad, punto único y compatibilidad de versión. |
| 2 | Pérdida de configuraciones/archivos | Producto técnico / Infraestructura | `2/3/6 → 2/2/4 → 1/2/2 → 0/2/0` | Backups nube/local y restauración. La recuperación real es evidencia más fuerte; justificar `P=0`. |
| 3 | Tiempo limitado para implementar/probar/documentar | Proyecto / Transversal | `2/3/6 → 1/2/2 → 1/1/1 → 0/1/0` | Priorizar núcleo y entregables. Entregas cumplidas ayudan, pero no eliminan futuros plazos. |
| 4 | Ausencia o baja disponibilidad de integrante | Producto (discutible) / Transversal | `1/3/3 → 1/2/2 → 1/2/2 → 0/2/0` | Tareas claras, comunicación y redistribución. Participación observada no prueba imposibilidad futura. |
| 5 | Errores en VLAN, trunks, OSPF, HSRP o Port-Channel | Producto técnico / Infraestructura | `1/2/2 → 1/2/2 → 1/2/2 → 1/2/2` | Validación por etapas y reversión. “Fácil reconvergencia” no prueba eliminación; continúa materializado. |
| 6 | Appliances/imágenes incompatibles | Producto técnico / Infraestructura | `2/3/6 → 2/1/2 → 1/1/1 → 0/1/0` | Probar imágenes y disponer alternativas. Registrar versiones, arranque y comandos soportados. |
| 7 | Planilla desactualizada frente a topología | Proyecto / Infraestructura-Gestión | `2/2/4 → 1/2/2 → 1/1/1 → 0/1/0` | Actualizar tras cambios y por sprint. La propia evolución de pestañas es evidencia parcial. |
| 8 | ACL mal aplicada permite o bloquea tráfico | Producto técnico / Infraestructura | `2/2/4 → 2/1/2 → 2/1/2 → 2/1/2` | Probar flujos permitidos/denegados. “ACL cumplen su propósito” no basta. |
| 9 | Documentación de red diverge de configuración | Proyecto / Infraestructura | `2/2/4 → 1/2/2 → 1/2/2 → 1/2/2` | Actualizar y comparar. Una tabla “comprensible” no demuestra coincidencia con equipos. |
| 10 | Componentes sin responsable | Proyecto / Transversal | `2/2/4 → 2/1/2 → 2/1/2 → 2/1/2` | Tablero y responsables. El disparador de ACL fue copiado erróneamente en sprints posteriores. |
| 11 | Matriz sin evolución/acciones | Proyecto / Gestión | `2/3/6 → 2/2/4 → 2/2/4 → 2/2/4` | Una pestaña por sprint. La organización visible no garantiza exactitud matemática. |
| 12 | Conocimiento crítico concentrado | Producto técnico / Transversal | `2/3/6 → 2/2/4 → 1/2/2 → 1/2/0` | Documentar y explicar internamente. Autonomía debe demostrarse; E de S5 es inconsistente. |
| 13 | Costo/disponibilidad de recursos externos | Producto técnico / Transversal con caso Programación | `1/2/2 → 1/1/1 → 1/1/1 → 1/1/0` | Railway financiado y suscripciones. Disponibilidad operativa es evidencia parcial; E de S5 es inconsistente. |
| 14 | Abandono o reducción total de participación | Producto (discutible) / Transversal | `1/3/3 → 1/2/2 → 1/2/2 → 1/2/2` | Evitar dependencia individual y redistribuir. “Mismo equipo” no elimina el residual. |
| 15 | Endpoints sensibles con protección incompleta | Producto técnico / Programación | `— → 2/3/6 → 2/2/4 → 2/2/4` | Revisar `@PreAuthorize`, roles y accesos. “Endpoints protegidos” exige pruebas HTTP por actor. |
| 16 | README/repositorio no permiten verificar versión evaluada | Proyecto / Programación-Gestión | `— → 2/3/4 → 2/2/4 → 2/2/4` | Documentar ejecución, variables, ramas y commit. En S3, `2 × 3 ≠ 4`. |

## Decisiones defendibles

### Caso 1: hardware y servidor centralizado

- **Dato**: riesgo 1, Infraestructura; equipos de 16 GB; estado materializado; mitigación de appliances livianos y menor RAM por nodo.
- **Dato**: el servidor compartido figura primero entre contingencias y luego se informa como ejecutado; en S3 se afirma que no hubo fallas graves y que bajó la probabilidad.
- **Cálculo**: `9 → 6` porque P pasa de 3 a 2 e I queda en 3.
- **Decisión defendible**: centralizar en el equipo más capaz es un tratamiento operativo que busca reducir la probabilidad de lentitud o fallos de arranque. No reduce por sí mismo la gravedad si ese servidor falla.
- **Alternativa descartada**: la planilla no documenta una comparación ni descarte formal. Ejecutar por partes, simplificar y reasignar al equipo más potente aparecen como opciones de contingencia, no como alternativas evaluadas con razones.
- **Evidencia necesaria**: misma topología/carga, versiones registradas, CPU/RAM, nodos iniciados, tiempos y estabilidad antes/después; repetir en más de una ejecución.
- **Residual**: exposición registrada 6, dependencia de un host central, pérdida/cambio de versión y ausencia de evidencia cuantificada. Cambiar el abordaje a `Transferir` en S4/S5 es discutible porque no se identifica un tercero externo.

### Caso 2: respaldos

Generar copias verificadas reduce probabilidad o impacto de pérdida irreversible; restaurar tras el disparador es contingencia. La evidencia fuerte es una restauración cronometrada desde una copia identificada, con integridad y configuración operativa verificadas. “Hay backups” sólo prueba existencia.

### Caso 8: ACL

Ordenar reglas y probar flujos es mitigación preventiva. La configuración presente no demuestra comportamiento. El residual incluye reglas nuevas, aplicación en interfaz/dirección equivocada y regresiones.

### Caso 15: autorización del backend

`@PreAuthorize` y roles son controles preventivos. La prueba debe diferenciar autenticación de autorización y cubrir sin token, usuario autenticado sin permiso y actor autorizado. El resultado puede respaldar una reducción de probabilidad de acceso indebido, no demostrar impacto cero.

### Fórmula oral breve

“El dato histórico dice __. Elegimos __ para reducir [P/I]. Lo contrastamos con __. Observamos __. La exposición pasó de __ a __, pero queda __. Donde la planilla no documenta la razón, lo presento como inferencia.”

Usar esta estructura para razonar, no memorizarla como sustituto de comprensión.

## Inconsistencias que deben reconocerse

1. **Riesgo 16, Sprint 3**: `P=2`, `I=3`, `E informada=4`. El cálculo correcto es `2 × 3 = 6`. Es un error matemático comprobado bajo la fórmula declarada. Sólo sería otra escala si se documentara una fórmula distinta; no existe tal documentación.
2. **Riesgos 12 y 13, Sprint 5**: `1 × 2` y `1 × 1` deberían dar 2 y 1, pero E figura 0 mientras P no es 0.
3. **Totales y rangos**: Sprint 2 usa `SUM(G5:G18)` y reproduce 65. Sprint 3 y 4 muestran `SUM(G6:G19)`, que omite riesgo 1 y riesgo 16; el valor cacheado 31 de Sprint 3 tampoco incorpora coherentemente las filas actuales. Sprint 5 conserva un total antiguo 18 en otra celda y una fórmula completa `SUM(G5:G20)` con valor cacheado 24 que no coincide con los valores visibles actuales.
4. **Recuento actual**: sumar las E visibles produce 65, 47, 38 y 28. Recalcular además las filas inconsistentes produce 65, 49, 38 y 31. Ninguna serie sustituye silenciosamente la publicada `65 → 31 → 28 → 24`; hay que explicar qué se está midiendo.
5. **Estados frente a valores**: hay riesgos `Cerrado` con P mayor que cero en Sprint 4 y otros con P cero en Sprint 5 sin una regla documentada que justifique el cambio.
6. **Materializado frente a tratamiento**: varios riesgos siguen `Materializado` mientras el abordaje dice `Eliminar`; eliminar la causa y recuperarse del efecto no son equivalentes.
7. **Cambios de abordaje**: riesgo 1 pasa de `Reducir` a `Transferir`; riesgo 12 usa `Transferir` para nivelación interna; riesgos 2, 3, 8 y otros pasan a `Compartir` aunque las acciones descriptas parecen reducción o trabajo colaborativo. Conservar y cuestionar.
8. **Tipos discutibles**: riesgos 4 y 14 son etiquetados producto aunque su consecuencia principal es de continuidad del proyecto.
9. **Disparadores copiados**: riesgo 10 usa desde Sprint 3 el texto de acceso de red no autorizado, que pertenece conceptualmente a ACL; riesgo 11 usa luego un texto de diferencias de documentación.
10. **Evidencias conclusivas o vagas**: “mejor funcionamiento”, “fácil reconvergencia”, “ACL cumplen su propósito”, “endpoints están protegidos”, “ramas actualizadas” y “estado cerrado” afirman resultados sin protocolo reproducible.

Corrección defendible: conservar la versión original, registrar fórmula/valor anterior y nuevo, motivo, fecha y responsable, recalcular totales y gráfica, y explicar cualquier cambio de prioridad o seguimiento. Nunca ajustar P o I sólo para sostener un E histórico.

## Qué cuenta como evidencia

Una evidencia fuerte responde:

1. **Precondición**: versión, configuración, actor, carga y estado inicial.
2. **Acción**: operación exacta y reproducible.
3. **Resultado esperado**: criterio de aprobación definido antes.
4. **Resultado observado**: salida, métrica, respuesta o artefacto fechado.
5. **Trazabilidad**: riesgo, sprint, responsable y versión evaluada.
6. **Efecto**: explica si sustenta reducción de P, I o ambas.
7. **Límite**: qué escenario no cubre y cuál es el residual.

Aplicación a frases vagas:

| Frase | Área | Precondición y acción | Resultado esperado | Relación con el riesgo |
|---|---|---|---|---|
| “Las ACL cumplen su propósito” | Infraestructura | Registrar ACL, interfaz/dirección y matriz origen-destino-puerto; ejecutar flujos permitidos y denegados; capturar contadores/salidas antes y después. | Permitidos funcionan, denegados fallan y aumenta la entrada correcta, sin bloquear servicios necesarios. | Apoya reducción de P de regla incorrecta; no prueba que todo cambio futuro esté cubierto. |
| “Fácil reconvergencia” | Infraestructura | Registrar rutas/vecindades y tráfico estable; derribar enlace/nodo; medir pérdida y tiempo con salidas antes-durante-después. | Recuperación por camino alternativo dentro de un umbral acordado. | Principalmente reduce impacto/duración de una falla, no la probabilidad de que el enlace falle. |
| “Los endpoints están protegidos” | Programación | Fijar versión y matriz endpoint-permiso; enviar requests sin token, con rol sin permiso y con rol autorizado. | `401`, `403` y respuesta autorizada esperada, sin exposición de datos; conservar logs/tests. | Apoya reducción de P de acceso indebido; no demuestra impacto cero ni cobertura de endpoints no probados. |

El testing técnico sólo es evidencia de mitigación. Una prueba aprobada no cierra el riesgo hasta vincularse con la dimensión estimada y el residual.

## Banco graduado de preguntas

Formular sólo una por turno y esperar respuesta.

### Nivel inicial

1. En el riesgo 1 de Sprint 2, ¿cómo calculás la exposición y qué representa cada factor?
2. ¿Por qué el riesgo 3 es de proyecto y el riesgo 15 es de producto?
3. En el riesgo 2, ¿qué acción es preventiva y cuál es contingencia?
4. ¿Qué diferencia hay entre evidencia y una afirmación como “mejor funcionamiento”?

### Nivel intermedio

1. ¿Qué dimensión intenta reducir el servidor GNS3 centralizado y qué residual introduce?
2. ¿Cómo demostrarías que los backups del riesgo 2 permiten reducir el impacto?
3. ¿Qué falta para vincular una prueba de ACL con la exposición residual del riesgo 8?
4. ¿Por qué “mismo equipo durante el sprint” no basta para cerrar el riesgo 14?
5. ¿Qué cuestionarías del abordaje `Transferir` en el riesgo 12?

### Nivel avanzado

1. Auditá `P=2`, `I=3`, `E=4` del riesgo 16 sin cambiar retrospectivamente P o I.
2. Defendé la tendencia `65 → 31 → 28 → 24` y explicá simultáneamente por qué requiere saneamiento.
3. Diseñá evidencia para reconvergencia e indicá si afectaría P, I o ambas.
4. Compará el estado `Cerrado` del riesgo 6 con el estado `Materializado` del riesgo 5 usando evidencia y residual.
5. Explicá cómo corregir rangos de totales conservando trazabilidad y qué decisiones podrían cambiar.

### Modo auditor

1. ¿Qué celdas, fórmulas y totales dependen de la exposición del riesgo 16?
2. ¿Qué abordajes no coinciden claramente con las acciones descriptas?
3. ¿Qué disparadores parecen copiados de otra fila y cómo afecta eso a la contingencia?
4. ¿Cuál de las evidencias vagas convertirías primero en prueba reproducible y por qué?
