# Escenarios de recuperación de Gestión de Riesgos

Estos escenarios evalúan si el plugin puede enseñar y auditar la planilla
histórica de Gestión de Riesgos SIENEP sin completar sus vacíos con hallazgos
de Infraestructura o Programación. Las mismas consultas y criterios se reutilizan
en RED, sin la habilidad nueva, y en GREEN, con la habilidad y su referencia.

Un criterio se considera recuperado solo cuando la respuesta distingue datos de
la planilla, cálculos, evidencia observable e inferencias. Las justificaciones que
no consten en la fuente deben marcarse como inferencias, no presentarse como
hechos.

## Escenario 1: enseñanza desde cero

**Consulta:** No sé nada de Gestión de Riesgos. Enseñame desde cero qué es un
riesgo, la diferencia entre riesgo de producto y de proyecto, probabilidad,
impacto, exposición y riesgo residual. Aplicalo a un caso de la planilla SIENEP,
sin mezclar las materias, y terminá con una comprobación breve de comprensión.

**Criterios de éxito:**

- explica los conceptos sin asumir conocimiento previo y calcula la exposición
  como `probabilidad × impacto`;
- identifica de forma explícita el área del caso SIENEP y no traslada hallazgos
  entre Infraestructura y Programación;
- recorre un dato histórico de la planilla desde riesgo y decisión hasta
  evidencia, resultado y riesgo residual;
- diferencia qué proviene de la planilla y qué sería una inferencia;
- termina con una sola pregunta corta para comprobar comprensión.

## Escenario 2: defensa del riesgo de hardware

**Consulta:** Ayudame a defender oralmente el riesgo de recursos de hardware
insuficientes para GNS3 y la decisión de usar un servidor centralizado. Explicá
el abordaje elegido, qué alternativa se descartó, si bajó la probabilidad o el
impacto, qué evidencia lo demuestra y qué limitación sigue abierta. No inventes
razones que no estén documentadas.

**Criterios de éxito:**

- mantiene el caso dentro de Gestión de Riesgos y etiqueta el ejemplo técnico
  como perteneciente a Infraestructura;
- explica por qué el servidor centralizado es un tratamiento del riesgo y no una
  prueba suficiente de que quedó controlado;
- distingue mitigación preventiva de contingencia reactiva;
- pide o propone evidencia observable y reproducible sobre recursos y operación;
- marca como inferencia toda alternativa descartada o causal que la planilla no
  documente y reconoce el riesgo residual o la limitación pendiente.

## Escenario 3: auditoría del cálculo `2 × 3 ≠ 4`

**Consulta:** En una fila de Sprint 3, el riesgo 16 tiene probabilidad 2,
impacto 3 y exposición informada 4. Auditá la fila: mostrá el cálculo, clasificá
el problema y explicá cómo corregirlo sin ocultar ni ridiculizar la
inconsistencia.

**Criterios de éxito:**

- muestra `2 × 3 = 6` y señala que la exposición 4 es matemáticamente
  inconsistente;
- distingue un error comprobado de una posible interpretación o escala no
  documentada;
- no altera probabilidad o impacto para justificar retrospectivamente el 4;
- propone corregir el valor o documentar otra fórmula y conservar trazabilidad
  del cambio;
- explica el efecto de la corrección sobre el seguimiento y cualquier total que
  dependa de esa exposición.

## Escenario 4: crítica de evidencias vagas

**Consulta:** La planilla afirma “las ACL cumplen su propósito”, “fácil
reconvergencia” y “los endpoints están protegidos”. Evaluá si esas frases bastan
como evidencia de mitigación. Para cada una indicá qué falta, una prueba
reproducible y el resultado esperado, manteniendo separadas Infraestructura y
Programación.

**Criterios de éxito:**

- rechaza las tres afirmaciones como evidencia suficiente por sí solas;
- separa ACL y reconvergencia como casos de Infraestructura, y protección de
  endpoints como caso de Programación;
- para cada frase define precondición, acción observable y resultado esperado;
- exige evidencia reproducible como salidas antes/durante/después, flujos
  permitidos y denegados, o respuestas HTTP autenticadas y no autorizadas;
- no da por efectiva la mitigación hasta vincular la prueba con una reducción de
  probabilidad o impacto.

## Escenario 5: modo Profesor, una pregunta por turno

**Consulta:** Actuá en modo Profesor para prepararme sobre la planilla de
Gestión de Riesgos SIENEP. Empezá evaluando si comprendo mitigación,
contingencia, evidencia y riesgo residual. Hacé exactamente una pregunta en este
turno, esperá mi respuesta y no adelantes la corrección.

**Criterios de éxito:**

- formula exactamente una pregunta;
- espera la respuesta del estudiante antes de repreguntar o corregir;
- la pregunta exige aplicar un concepto a una decisión o evidencia de la
  planilla, no recitar una definición aislada;
- no entrega una respuesta modelo ni un guion memorizable en el primer turno;
- conserva Gestión de Riesgos como materia principal y no deriva a un examen
  técnico de Infraestructura o Programación.

## Protocolo de ejecución

1. Ejecutar las cinco consultas con acceso exclusivo a las habilidades y
   referencias declaradas para la fase evaluada.
2. Contrastar cada respuesta con todos sus criterios observables, sin completar
   ausencias mediante conocimiento externo.
3. Registrar en RED una omisión literal o conducta concreta por escenario y
   marcar `Falla` cuando falte al menos un criterio esencial.
4. Repetir en GREEN sin cambiar consultas ni criterios; registrar qué criterio
   se recuperó y cualquier brecha restante.

## Línea base RED con las dos habilidades actuales

Fecha de ejecución: 2026-07-19.

Método: un agente aislado respondió las cinco consultas usando exclusivamente
el manifiesto actual y los `SKILL.md` y referencias de
`estudiar-infraestructura-sienep` y `estudiar-programacion-sienep`. No tuvo
acceso a estos criterios, a la especificación, a la planilla ni a una referencia
de Gestión de Riesgos. Se conservaron las formulaciones citadas tal como
aparecieron en sus respuestas.

| Consulta (resumen) | Conducta recuperable | Omisión observada literalmente | Resultado RED |
|---|---|---|---|
| 1. Enseñanza desde cero | Explicó conceptos generales, usó `probabilidad × impacto` como fórmula condicional y cerró con una pregunta. | Admitió: “No puedo afirmar que esa sea la fórmula exacta ni interpretar sus escalas sin ver la planilla”. Luego sustituyó un caso de la planilla por una observación de la guía técnica: “Aplicado únicamente a Infraestructura SIENEP, hay una observación histórica utilizable: una ACL Guest tuvo un `permit any` demasiado temprano”. No recuperó el recorrido histórico riesgo → decisión → evidencia → resultado de la planilla. | Falla |
| 2. Riesgo de hardware | Evitó inventar la alternativa descartada y pidió evidencia comparativa. | Declaró: “La guía actual no identifica una fila sobre ‘recursos de hardware insuficientes para GNS3’, no documenta la decisión de usar un servidor centralizado ni registra qué alternativa se descartó”. Después cambió de riesgo: “Lo que sí está documentado en Infraestructura es una decisión distinta y más acotada”, sobre Keepalived y failover. No pudo explicar el abordaje, la dimensión reducida ni el residual del riesgo consultado. | Falla |
| 3. `2 × 3 ≠ 4` | Detectó la inconsistencia, mostró `2 × 3 = 6`, evitó ajustar datos retrospectivamente y propuso dejar trazabilidad. | La respuesta terminó en “documentar la regla que produce ese valor”; no explicó cómo el cambio de 4 a 6 afecta el seguimiento del riesgo ni los totales de exposición que dependan de la fila. | Falla |
| 4. Evidencias vagas | Rechazó las tres frases como pruebas suficientes, separó las materias y propuso verificaciones reproducibles para ACL, reconvergencia y endpoints. | Las verificaciones concluyeron en resultados técnicos esperados, pero la respuesta no indicó si esos resultados reducen la probabilidad, el impacto o ambos. Por tanto, no cerró la trazabilidad prueba → efectividad de mitigación → exposición residual. | Falla |
| 5. Modo Profesor | Formuló exactamente una pregunta, esperó la respuesta y no adelantó la corrección. | La pregunta usó un caso genérico: “En una fila de riesgo se aplicó una acción preventiva y luego se adjuntó una captura de configuración”. No pudo anclar la evaluación a una decisión o evidencia identificable de la planilla SIENEP. | Falla |

**Confirmación RED:** los cinco escenarios fallan al menos un criterio. El
agente no mezcló indistintamente Infraestructura y Programación ni aceptó las
afirmaciones vagas como evidencia, y sí detectó la inconsistencia aritmética.
La ausencia de una habilidad y referencia específicas se manifestó en otros
fallos esenciales: sustituyó un riesgo por otro, no pudo explicar decisiones de
la planilla y dejó incompleta la relación entre evidencia, exposición y
seguimiento.

## Resultado GREEN con la habilidad nueva

Fecha de ejecución: 2026-07-19.

Método: un agente en contexto limpio recibió exclusivamente el `SKILL.md` y la
referencia `guia-gestion-riesgos.md` nuevas. No recibió este archivo, el brief,
los criterios ni el diagnóstico RED. Respondió las cinco consultas como turnos
independientes. Se conservaron sin cambios las consultas y todos los criterios;
**todos los criterios son obligatorios** y cada escenario sólo pasa cuando
recupera el conjunto completo.

| Consulta (resumen) | Criterios recuperados observados | Brecha restante | Resultado GREEN |
|---|---|---|---|
| 1. Enseñanza desde cero | Definió riesgo, producto/proyecto, P, I, exposición y residual; mostró `3 × 3 = 9` y `2 × 3 = 6` con el riesgo 1 de Infraestructura; etiquetó datos de la planilla, cálculo y evidencia parcial; reconoció límites y cerró con una sola pregunta. | Ninguna respecto de los criterios congelados. | Pasa |
| 2. Riesgo de hardware | Mantuvo Gestión de Riesgos e Infraestructura; separó optimización preventiva del servidor inicialmente contingente; explicó reducción de probabilidad, no de impacto; negó que exista un descarte formal documentado; pidió métricas reproducibles y reconoció exposición 6, host único y versiones como residual. | Ninguna respecto de los criterios congelados. | Pasa |
| 3. `2 × 3 ≠ 4` | Mostró `2 × 3 = 6`, clasificó el 4 como error matemático bajo la fórmula declarada, dejó como hipótesis no documentada otra escala, no alteró P/I y exigió conservar original, motivo, fecha, responsable y recalcular totales, gráfica, prioridad y residual. | Ninguna respecto de los criterios congelados. | Pasa |
| 4. Evidencias vagas | Rechazó las tres frases; separó ACL/reconvergencia de Infraestructura y endpoints de Programación; para cada una indicó precondición, acción, resultado esperado, observación reproducible, dimensión P/I respaldada y residual no cubierto. | Ninguna respecto de los criterios congelados. | Pasa |
| 5. Modo Profesor | Formuló exactamente una pregunta aplicada al riesgo 2, que integra mitigación, contingencia, disparador, evidencia y residual; no corrigió ni adelantó una respuesta y mantuvo Gestión de Riesgos como materia principal. | Ninguna respecto de los criterios congelados. | Pasa |

**Confirmación GREEN:** los cinco escenarios recuperan todos sus criterios
obligatorios. No fue necesario modificar la habilidad después de esta ejecución.

## Escenario 6: corrección multiturmo y transición

**Turno 1:** No elijo modo. Enseñame brevemente cómo se calcula la exposición
con el riesgo 2 y comprobá si entendí.

**Respuesta del estudiante:** La exposición es probabilidad por impacto. En el
riesgo 2, los backups reducen el impacto de una pérdida, así que si hay una
copia ya podemos decir que el riesgo quedó cerrado.

**Criterios de éxito del turno de corrección:**

- el primer turno comienza como Tutor y formula una sola comprobación;
- al responder el estudiante, pasa gradualmente a Profesor mediante corrección
  y repregunta, sin volver a impartir una clase completa;
- la corrección contiene exactamente cinco componentes, en este orden:
  concepto acertado, imprecisión, campo/evidencia de la planilla,
  reformulación rigurosa y repregunta breve;
- reconoce como acierto `P × I`, cuestiona que la mera existencia de un backup
  cierre el riesgo y usa la restauración verificable como evidencia más fuerte;
- termina con exactamente una repregunta breve y espera el siguiente turno.

## Escenario 7: rúbrica de Simulacro

**Consulta:** Actuá en modo Simulacro. Evaluá esta respuesta: “El riesgo 1 quedó
resuelto porque usamos el servidor centralizado y la exposición bajó”. Puntuala
sin mezclar materias y dejame una sola pregunta de seguimiento.

**Criterios de éxito:**

- mantiene Gestión de Riesgos como materia y etiqueta el caso como
  Infraestructura;
- puntúa por separado concepto, aplicación SIENEP, justificación, evidencia y
  honestidad sobre límites, sin fusionar dimensiones;
- explica brevemente el fundamento de cada puntuación;
- penaliza que se confunda decisión con evidencia y que se omita exposición 6,
  host central y falta de métricas como límites;
- formula exactamente una pregunta de seguimiento.

## Escenario 8: prioridad de una planilla nueva

**Consulta:** Te proporciono una versión nueva de la planilla, transcripta en
`tests/fixtures/gestion-riesgos-version-nueva.md`. Auditála antes de enseñarme:
decime qué es vigente y qué queda sólo como histórico, recalculá cada fila, el
total y la evolución, y no reutilices cifras anteriores para completar vacíos.

**Criterios de éxito:**

- declara que la fuente nueva tiene prioridad sobre la referencia histórica;
- lee las tres hojas relevantes del fixture y no sólo la primera tabla;
- recalcula cada exposición (`2×3=6`, `1×2=2`, `2×2=4`) y el total vigente 12;
- detecta que el total informado 10 y la evolución `65→31→28→24→10` no son
  coherentes con las filas, y propone una evolución recalculada que termina en
  12 sin sobrescribir la serie informada;
- separa valores vigentes de la fuente nueva, cifras históricas de la referencia
  e inferencias; no rellena el campo de evidencia vacío del riesgo 17.

## Protocolo adicional de GREEN

1. Ejecutar los escenarios 6–8 con un agente en contexto limpio que reciba sólo
   el `SKILL.md`, su referencia y, para el escenario 8, el fixture versionado.
2. Ejecutar cada consulta como caso independiente; el escenario 6 conserva sus
   dos turnos en el mismo contexto.
3. Contrastar todas las salidas con todos los criterios, que siguen siendo
   obligatorios.
4. Registrar un resultado observado por criterio y cualquier brecha. No usar
   archivos temporales como única evidencia de aprobación.

## Evidencia GREEN reproducible y versionada

Fecha de ejecución: 2026-07-19.

Entorno: dos agentes en contexto limpio. Ambos recibieron sólo la habilidad y su
referencia; el agente del escenario 8 recibió además el fixture versionado. No
recibieron este archivo, el brief ni los criterios. Para reproducir, usar las
consultas y respuesta estudiantil literales de los escenarios 6–8 siguiendo el
protocolo anterior y contrastar cada salida con todos sus criterios.

### Resultado observado: escenario 6

| Criterio obligatorio | Evidencia observable | Resultado |
|---|---|---|
| Tutor inicial y una comprobación | Explicó `E=P×I` con riesgo 2 y cerró únicamente con “¿Por qué tener un backup no basta...?”. | Pasa |
| Transición gradual | Tras la respuesta, dejó la explicación inicial y adoptó corrección seguida de una única repregunta aplicada. | Pasa |
| Cinco componentes exactos y ordenados | Emitió: Concepto acertado, Imprecisión, Campo o evidencia de la planilla, Reformulación rigurosa y Repregunta breve. | Pasa |
| Contenido de la corrección | Validó `P×I`, rechazó que existencia implique cierre y exigió restauración cronometrada, íntegra y operativa. | Pasa |
| Una repregunta y espera | Terminó sólo con “¿Qué resultado observable pedirías para demostrar que el backup realmente reduce el impacto?”. | Pasa |

### Resultado observado: escenario 7

| Criterio obligatorio | Evidencia observable | Resultado |
|---|---|---|
| Materia y área | Mantuvo Gestión de Riesgos y rotuló el caso como Infraestructura. | Pasa |
| Cinco dimensiones separadas | Puntuó concepto `1/2`, aplicación SIENEP `1/2`, justificación `0/2`, evidencia `0/2` y honestidad sobre límites `0/2`. | Pasa |
| Fundamento | Explicó cada puntuación con el cambio `9→6`, P `3→2`, I `3`, y la debilidad de “mejor funcionamiento”. | Pasa |
| Límites penalizados | Señaló exposición residual 6, host único y falta de mediciones reproducibles. | Pasa |
| Una pregunta | Cerró únicamente preguntando qué residual introduce el servidor único. | Pasa |

### Resultado observado: escenario 8

| Criterio obligatorio | Evidencia observable | Resultado |
|---|---|---|
| Prioridad de fuente | Declaró vigente el fixture nuevo e histórica la guía, sin usarla para completar datos. | Pasa |
| Lectura completa | Usó Sprint 6, Evolución y Lista de valores, incluida su fórmula declarada. | Pasa |
| Recálculo | Mostró `2×3=6`, `1×2=2`, `2×2=4` y total corregido `12`. | Pasa |
| Total y evolución | Explicó que 10 coincide con E informadas pero arrastra el error; conservó `65→31→28→24→10` como serie informada y cerró Sprint 6 recalculado en 12. | Pasa |
| Vigente/histórico/inferencia | No importó filas antiguas, declaró no recalculables S2–S5 con el fixture y mantuvo vacía la evidencia del riesgo 17. | Pasa |

**Confirmación GREEN adicional:** escenarios 6, 7 y 8 recuperan todos sus
criterios obligatorios. Esta tabla conserva protocolo, entradas, resultados por
criterio y artefacto de fuente; la aprobación no depende de un transcript ni de
un archivo temporal.
