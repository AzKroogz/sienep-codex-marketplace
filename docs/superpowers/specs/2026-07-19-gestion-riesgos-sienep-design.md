# Diseño: tercera habilidad de Gestión de Riesgos SIENEP

**Fecha:** 2026-07-19
**Plugin:** `sienep-defensa`
**Habilidad propuesta:** `estudiar-gestion-riesgos-sienep`

## Objetivo

Agregar al plugin una tercera habilidad dedicada a la materia Gestión de Riesgos. Debe enseñar los conceptos desde cero, aplicarlos a la planilla real de SIENEP y preparar al equipo para explicar y justificar sus decisiones durante la defensa.

El testing técnico no será un eje independiente. Solo se tratará cuando una prueba constituya evidencia de que una mitigación, contingencia o control funciona.

## Límites del alcance

- Mantener Gestión de Riesgos separada de las habilidades de Infraestructura y Programación.
- Usar ejemplos de ambos proyectos únicamente como casos de riesgo claramente identificados por área.
- No trasladar hallazgos técnicos entre GNS3 y el backend.
- No asumir que cada dato de la planilla es correcto o defendible.
- No convertir la preparación en un guion para memorizar.
- No modificar la planilla original como parte de esta mejora.

## Fuente y portabilidad

La fuente analizada es `/home/nicolas/Descargas/Planilla de Gestión de Riesgos .xlsx`, con hojas para Sprint 2, Sprint 3, Sprint 4, Sprint 5, evolución de exposición total y lista de valores.

El plugin no dependerá de esa ruta local. Incorporará una referencia Markdown con el modelo conceptual, la evolución observada, los riesgos relevantes y las inconsistencias detectadas. Cuando exista una planilla más reciente, la habilidad deberá tratar la referencia como histórica y volver a verificar el archivo suministrado.

## Estructura propuesta

```text
plugins/sienep-defensa/
├── .codex-plugin/plugin.json
└── skills/
    ├── estudiar-infraestructura-sienep/
    ├── estudiar-programacion-sienep/
    └── estudiar-gestion-riesgos-sienep/
        ├── SKILL.md
        ├── agents/openai.yaml
        └── references/guia-gestion-riesgos.md
```

El manifiesto del plugin se actualizará para presentar las tres áreas, agregar Gestión de Riesgos a sus palabras clave y ofrecer un inicio rápido específico para esa defensa.

## Modos de interacción

### Tutor

Explicar desde cero y avanzar de concepto general a caso SIENEP. Cada bloque terminará con una comprobación breve de comprensión.

### Profesor

Formular una pregunta por vez, esperar la respuesta, repreguntar sobre la justificación o evidencia y corregir después del intento del estudiante.

### Simulacro

Recrear una defensa oral combinando definiciones, lectura de la planilla, decisiones por sprint, inconsistencias y preguntas de seguimiento. Evaluar comprensión, aplicación, justificación, evidencia y reconocimiento de límites.

### Auditoría de planilla

Revisar consistencia matemática y semántica: exposición, estados, abordajes, mitigación, contingencia, disparadores, seguimiento, evidencia y continuidad del mismo riesgo entre sprints.

Si el usuario no elige un modo, comenzar como Tutor y pasar gradualmente a Profesor.

## Contenido conceptual

La guía deberá enseñar:

1. riesgo como evento incierto expresado mediante condición y consecuencia;
2. diferencia entre riesgo de producto y riesgo de proyecto;
3. probabilidad, impacto, exposición y riesgo residual;
4. estados identificado, planificado, materializado y cerrado;
5. abordajes asumir, reducir, compartir, transferir y eliminar;
6. diferencia entre mitigación preventiva y contingencia reactiva;
7. función del disparador, responsable y fecha comprometida;
8. seguimiento por sprint y justificación de cambios;
9. diferencia entre afirmación, evidencia observable y prueba reproducible;
10. trazabilidad entre riesgo, acción, resultado y exposición posterior.

## Método para explicar decisiones

Cada explicación de defensa seguirá este contrato:

```text
Concepto
→ aplicación concreta en SIENEP
→ decisión tomada y alternativa descartada
→ evidencia observable
→ resultado sobre probabilidad o impacto
→ limitación, inconsistencia o mejora pendiente
```

La habilidad deberá explicar tanto las decisiones defendibles como las débiles. No inventará justificaciones ausentes en la planilla; las marcará como inferencia o pedirá al equipo que reconstruya la decisión con evidencia.

## Lectura inicial de la planilla

La exposición total informada evoluciona de 65 en Sprint 2 a 31 en Sprint 3, 28 en Sprint 4 y 24 en Sprint 5. La cantidad de riesgos pasa de 14 a 16 al incorporarse riesgos de seguridad/autorización del backend y trazabilidad del repositorio.

Casos útiles para enseñar decisiones:

- recursos insuficientes para GNS3 y uso de servidor centralizado;
- pérdida de configuraciones y recuperación mediante respaldos;
- compatibilidad de appliances;
- orden y validación de ACL;
- documentación desactualizada respecto de la topología;
- concentración de conocimiento en pocos integrantes;
- protección de endpoints sensibles por rol;
- reproducibilidad y trazabilidad mediante README, ramas y commits.

## Inconsistencias que deben convertirse en preguntas

- En Sprint 3, el riesgo 16 presenta probabilidad 2 e impacto 3, pero exposición 4 en lugar de 6.
- Algunos riesgos cerrados conservan exposición distinta de cero; otros usan exposición cero aunque probabilidad e impacto continúen distintos de cero.
- El riesgo 1 comienza como limitación de hardware y luego incorpora incompatibilidad por versiones de GNS3, que podría requerir un riesgo separado.
- El respaldo de archivos responde al riesgo de pérdida, pero no elimina por sí mismo errores de VLAN, trunks, OSPF, HSRP o Port-Channel.
- Expresiones como “las ACL cumplen su propósito”, “fácil reconvergencia” o “los endpoints están protegidos” no identifican una prueba observable y reproducible.
- Algunos abordajes cambian entre reducir, compartir o transferir sin explicar quién asume el riesgo ni qué mecanismo produce la transferencia.
- Ciertos seguimientos cambian el tema original del riesgo, debilitando la trazabilidad entre sprints.

La habilidad no deberá ridiculizar estos problemas. Los usará para practicar respuestas honestas: reconocer la inconsistencia, explicar el criterio correcto y proponer cómo documentarla mejor.

## Estrategia de preguntas

El banco cubrirá cuatro niveles:

1. **Definición:** explicar un concepto sin leer la planilla.
2. **Aplicación:** identificar sus campos en un riesgo concreto.
3. **Justificación:** defender por qué se eligió un abordaje o cambió la exposición.
4. **Crítica:** detectar incoherencias y proponer una corrección trazable.

Las repreguntas deberán variar entre:

- “¿Qué evidencia demuestra eso?”
- “¿Bajó la probabilidad, el impacto o ambos?”
- “¿Eso es mitigación o contingencia?”
- “¿Quién recibe el riesgo si lo transferimos?”
- “¿Por qué puede considerarse cerrado?”
- “¿Qué cambió realmente respecto del sprint anterior?”

## Corrección y evaluación

La corrección indicará:

- qué concepto estuvo bien;
- qué parte fue imprecisa;
- qué campo o evidencia de la planilla respalda la respuesta;
- cómo expresar la decisión con mayor rigor;
- una repregunta breve para comprobar apropiación.

En simulacro, la valoración separará cinco dimensiones: concepto, aplicación a SIENEP, justificación, evidencia y honestidad sobre límites. No se premiará una respuesta memorizada si no puede sostener una repregunta.

## Manejo de errores y datos faltantes

- Si una fórmula o dato no coincide, mostrar el cálculo y distinguir error comprobado de interpretación.
- Si falta evidencia, no inventarla: indicar qué evidencia sería necesaria.
- Si un seguimiento cambia la naturaleza del riesgo, señalarlo y proponer separar o reformular el riesgo.
- Si una decisión puede ser razonable pero no está documentada, etiquetarla como inferencia.
- Si se recibe una versión nueva de la planilla, recalcular evolución y consistencia antes de reutilizar cifras históricas.

## Validación

Antes de implementar la mejora se ejecutará un escenario de referencia sin la nueva habilidad para observar qué omite el plugin actual. Después se repetirá con la habilidad instalada.

La habilidad se considerará válida si el agente:

- explica los conceptos desde cero sin asumir conocimiento previo;
- mantiene separados los ejemplos de Infraestructura y Programación;
- formula una pregunta por vez en modo Profesor;
- exige evidencia antes de aceptar una mitigación como efectiva;
- detecta al menos las inconsistencias matemáticas y semánticas documentadas;
- no inventa razones ausentes en la planilla;
- ayuda a construir respuestas razonadas y no solo un guion memorizable.

También se validarán el `SKILL.md`, `agents/openai.yaml`, el manifiesto del plugin y el flujo de actualización/reinstalación del plugin local.
