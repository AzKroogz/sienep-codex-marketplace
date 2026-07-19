# Diseño: educar los tres skills desde una defensa real

## Objetivo

Actualizar los tres skills de `sienep-defensa` para reproducir el patrón de evaluación observado en una defensa académica de 2025: conceptos primero, decisiones SIENEP después y evidencia sólo cuando sostenga la explicación.

La preparación no se centrará en memorizar comandos, código o respuestas. Cada skill deberá comprobar que el estudiante entiende el problema, puede justificar la decisión y reconoce límites.

## Fuente y límites

El video y su transcripción son material de terceros y no se incorporarán al repositorio. Se agregará una referencia breve, anonimizada y derivada del análisis, etiquetada como observación pedagógica de una defensa anterior, no como requisito oficial de SIENEP 2026.

Las fuentes vigentes de cada proyecto continuarán determinando hechos técnicos y académicos. El video sólo informará la forma de enseñar, preguntar, repreguntar y administrar la defensa.

## Contrato pedagógico transversal

Los tres skills aplicarán esta estructura oral:

`respuesta directa → concepto → decisión SIENEP → evidencia → límite`

- La primera respuesta debe poder expresarse en 30–60 segundos.
- Profesor y Simulacro harán exactamente una pregunta por turno.
- La repregunta atacará la imprecisión concreta de la respuesta anterior.
- Antes de solicitar una demostración, se comprobará el concepto y el criterio de decisión.
- Se distinguirá `implementado y demostrado`, `implementado sin evidencia`, `propuesto` y `no documentado`.
- Las respuestas largas que no contesten primero recibirán corrección sobre claridad y manejo del tiempo.

La evaluación conservará las rúbricas propias de cada skill. La claridad y el tiempo serán retroalimentación oral, no una nota técnica inventada.

## Infraestructura

### Prioridad

Aproximadamente 80 % concepto y decisión, 20 % evidencia o demostración. El estudiante debe explicar qué problema resuelve una tecnología, cómo funciona y por qué fue elegida en SIENEP antes de recordar comandos.

### Preguntas derivadas

- criterio para elegir máscaras y efecto sobre capacidad, segmentación y crecimiento;
- necesidad y riesgo de que TI alcance distintas redes;
- diferencia conceptual entre capa 2 y capa 3;
- criterio para usar DHCP y dimensionar rangos;
- funciones y razones para elegir un firewall/router como pfSense;
- criterio de RAID, cableado, fibra y ubicación del centro de datos;
- redundancia implementada, punto único restante y tecnología más difícil.

Los comandos `show`, capturas y configuraciones aparecerán como evidencia posterior. No se iniciará el examen pidiendo sintaxis.

## Programación

### Prioridad

El estudiante explicará primero el concepto, la regla de negocio y el recorrido lógico. Swagger, código y pruebas confirmarán después la afirmación.

### Preguntas derivadas

- qué problema resuelve una validación y dónde pertenece;
- diferencia entre autenticación y autorización, JWT firmado y cifrado, DTO y entidad;
- por qué se eligió baja lógica, auditoría, `ddl-auto=validate` o separación controller/service/repository;
- qué debería ocurrir ante una entrada inválida y por qué corresponde determinado estado HTTP;
- cómo distinguir funcionalidad demostrada, implementación parcial y diseño futuro;
- cómo responder cuando una demostración falla sin ocultar el límite.

Las pruebas negativas observadas en la defensa se usarán como patrón: el docente puede pedir un caso inválido concreto para verificar que la explicación coincide con el comportamiento.

## Gestión de Riesgos

### Prioridad

Aproximadamente 80 % comprensión conceptual y 20 % aplicación a filas de la planilla. El foco será producto/proyecto, técnico, externo, personas, calidad, causa, evento, consecuencia, exposición, tratamiento, evidencia y residual.

### Pregunta y repregunta

La progresión preferida será:

`clasificación → causa/evento/consecuencia → control de la causa → tratamiento → evidencia → residual`

La categoría se justificará por naturaleza y origen. Que un evento afecte al aplicativo no basta para llamarlo riesgo de producto. Una mitigación técnica tampoco cambia automáticamente una causa externa.

Las configuraciones y pruebas técnicas sólo comprobarán mitigaciones. La pregunta será qué evidencia demostraría reducción de probabilidad o impacto, no qué comandos se usaron.

## Patrones generalizados de la defensa observada

1. El docente parte de una afirmación o fila concreta, no pide recitar toda la materia.
2. Una respuesta inicial genera una repregunta conceptual más profunda.
3. Se valora poder mostrar evidencia, pero después de entender la decisión.
4. Una propuesta hipotética no puede defenderse como implementación real.
5. Las fallas en vivo no son necesariamente definitivas si el equipo las reconoce y se recupera.
6. Exceder el tiempo perjudica incluso una entrega técnicamente prolija.
7. Pueden preguntar contribución individual, dificultad principal y FODA del equipo/proyecto.

## Cambios previstos

- Añadir el contrato pedagógico a los tres `SKILL.md`, adaptado a cada materia.
- Crear una única referencia transversal anonimizada con patrones de preguntas y manejo oral.
- Enlazarla desde los tres skills para Profesor, Simulacro o preparación de defensa.
- Ampliar escenarios y el validador durable para cubrir los tres ámbitos.
- Mantener las guías técnicas actuales como fuentes separadas.
- Actualizar el cachebuster del manifiesto para reinstalar el plugin.

## Escenarios de prueba

Antes de modificar los skills se agregarán escenarios que fallen con la conducta actual:

1. Infraestructura: explicar máscaras conceptualmente antes de pedir evidencia.
2. Infraestructura: distinguir implementación real de RAID propuesto.
3. Programación: explicar una validación y luego demostrar un caso negativo.
4. Programación: distinguir endpoint demostrado de funcionalidad afirmada.
5. Riesgos: clasificar una inundación que afecta indirectamente al aplicativo.
6. Riesgos: explicar por qué failover no cambia el origen de una caída de ISP.
7. Transversal: respuesta directa de 30–60 segundos y una repregunta por turno.
8. Transversal: contribución individual o FODA sin discursos evasivos.

## Criterios de aceptación

- Los tres skills enseñan conceptos antes de comandos, código o demostraciones.
- Las preguntas se aplican a decisiones verificadas de cada proyecto.
- Profesor y Simulacro hacen una sola pregunta por turno y repreguntan según la respuesta.
- Se aplica `respuesta directa → concepto → decisión → evidencia → límite`.
- Se diferencia implementación demostrada, implementación sin evidencia, propuesta y ausencia documental.
- Gestión de Riesgos conserva su énfasis conceptual 80/20.
- No se incorpora el video ni la transcripción de terceros.
- Los escenarios nuevos y validaciones existentes pasan.
- La versión reinstalada coincide con la fuente fusionada en `main`.
