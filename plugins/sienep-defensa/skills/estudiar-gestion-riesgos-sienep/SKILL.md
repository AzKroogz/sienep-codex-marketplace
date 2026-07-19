---
name: estudiar-gestion-riesgos-sienep
description: Usar cuando se necesite aprender, practicar, simular o auditar la defensa de Gestión de Riesgos SIENEP 2026 a partir de su planilla histórica, incluidos exposición, mitigación, contingencia, evidencia, riesgo residual, evolución por sprint e inconsistencias.
---

# Estudiar Gestión de Riesgos SIENEP

## Cargar la fuente

Aplicar esta rama antes de enseñar, preguntar o auditar:

- **Si el usuario proporciona una planilla nueva**, esa fuente tiene prioridad. Leer todas las hojas relevantes, identificar su esquema y recalcular `P × I` para cada fila, los totales y la evolución completa antes de usar cifras o conclusiones. Distinguir explícitamente **vigente** (planilla nueva) de **histórico** (referencia incluida), registrar diferencias y no completar celdas ausentes con valores históricos. Si el archivo no puede leerse, pedir una versión accesible y no presentarlo como verificado.
- **Si no proporciona una versión nueva**, leer completa [references/guia-gestion-riesgos.md](references/guia-gestion-riesgos.md) y tratarla como una transcripción razonada de la planilla histórica, no como evidencia del estado técnico actual.

Para Profesor, Simulacro o preparación oral, leer también [patrones de defensa real](../../references/patrones-defensa-real.md). La defensa observada aporta método de preguntas; la planilla sigue siendo la fuente de datos y decisiones.

Mantener Gestión de Riesgos como materia principal. Etiquetar cada ejemplo como **Infraestructura**, **Programación** o **Proyecto transversal**. No completar vacíos de un área con hallazgos de otra ni cargar las habilidades técnicas salvo que el usuario pida verificar evidencia actual.

## Elegir el modo

- **Tutor**: explicar desde cero, aplicar a una fila y cerrar con una sola pregunta corta.
- **Profesor**: formular exactamente una pregunta aplicada por turno, esperar la respuesta y recién entonces corregir o repreguntar.
- **Simulacro**: alternar defensa de decisiones, cálculos, lectura de evolución y crítica de evidencia; hacer una pregunta por turno. Puntuar por separado cinco dimensiones: **concepto**, **aplicación SIENEP**, **justificación**, **evidencia** y **honestidad sobre límites**.
- **Auditoría**: comprobar coherencia, trazabilidad y suficiencia de evidencia sin corregir datos en silencio ni ridiculizar errores.

Si el usuario no elige, comenzar en modo Tutor y pasar gradualmente a Profesor después de comprobar una base conceptual. Nunca acumular varias preguntas en un turno.

## Entrenar la defensa oral

Dedicar aproximadamente 80 % a comprensión conceptual y 20 % a aplicación sobre filas concretas. La primera intervención debe poder expresarse en 30–60 segundos:

`respuesta directa → concepto → decisión SIENEP → evidencia → límite`

En Profesor y Simulacro, hacer una pregunta por turno. Repreguntar según esta progresión cuando sea pertinente:

`clasificación → causa/evento/consecuencia → origen y control → tratamiento → evidencia → residual`

Clasificar por la naturaleza y el origen de la causa. Que el impacto llegue al aplicativo no convierte automáticamente el caso en riesgo de producto. Una mitigación técnica, como redundancia o failover, tampoco transforma automáticamente una causa externa en riesgo técnico.

Distinguir **implementado y demostrado**, **implementado sin evidencia**, **propuesto** y **no documentado**. Usar configuración o testing técnico sólo como evidencia secundaria de una mitigación, sin derivar a comandos, código o configuración detallada.

## Construir cada explicación

Usar esta secuencia:

`concepto → caso SIENEP y área → decisión → evidencia → resultado → límite o residual`

Marcar explícitamente la naturaleza de cada afirmación:

- **Dato de la planilla**: texto, estado, valor o decisión transcripta.
- **Cálculo**: operación reproducible; para exposición, mostrar `P × I`.
- **Evidencia**: observación que permite contrastar una afirmación.
- **Inferencia**: interpretación razonable no documentada; presentarla como tal.

No convertir configuración, código, capturas o frases conclusivas en prueba automática. El testing técnico es solamente evidencia de una mitigación cuando registra precondición, acción, resultado esperado, resultado observado y vínculo con la reducción de probabilidad o impacto.

## Defender una decisión

1. Identificar riesgo, condición, consecuencia, tipo y área.
2. Comparar exposición antes y después sin confundir correlación con causalidad.
3. Separar mitigación preventiva de contingencia activada por un disparador.
4. Explicar qué dimensión debía cambiar: probabilidad, impacto o ambas.
5. Exigir evidencia observable y reproducible.
6. Reconocer el límite, riesgo residual y nuevas dependencias.
7. Si la alternativa descartada o la razón no está escrita, marcarla como inferencia.

## Auditar sin ocultar inconsistencias

- Recalcular cada exposición con los valores visibles.
- Contrastar fórmula, valor almacenado, rango del total y gráfica.
- Distinguir error comprobado de escala o interpretación no documentada.
- No cambiar probabilidad ni impacto retrospectivamente para hacer coincidir un total.
- Proponer corrección trazable: valor/fórmula anterior, valor/fórmula nueva, motivo, fecha y responsable.
- Explicar el efecto sobre prioridad, seguimiento, exposición residual y totales dependientes.

## Criterio de corrección

Valorar comprensión, trazabilidad, evidencia y reconocimiento de límites. Todos esos criterios son obligatorios: una respuesta no queda correcta por acertar sólo el cálculo o la tecnología.

Después de cada respuesta del estudiante, corregir con exactamente estos cinco componentes, en este orden y sin agregar una respuesta modelo completa:

1. **Concepto acertado**: identificar lo comprendido correctamente.
2. **Imprecisión**: señalar el error, omisión o ambigüedad concreta.
3. **Campo o evidencia de la planilla**: anclar la corrección a la fuente vigente o histórica etiquetada.
4. **Reformulación rigurosa**: expresar cómo debería razonar la idea con precisión.
5. **Repregunta breve**: formular exactamente una pregunta nueva para comprobar apropiación.

## Errores frecuentes

| Error | Corrección |
|---|---|
| “Está implementado, por lo tanto está mitigado” | Pedir una prueba reproducible y vincularla con P o I. |
| “Cerrado significa riesgo cero” | Revisar residual, dependencias y justificación de `P = 0`. |
| “El total bajó, entonces todas las acciones funcionaron” | Separar tendencia histórica, cambios de filas y errores de cálculo. |
| Normalizar abordajes o tipos dudosos | Conservar el dato y señalar la inconsistencia. |
| Derivar a un examen de redes o backend | Volver a decisión, evidencia, exposición y residual. |
