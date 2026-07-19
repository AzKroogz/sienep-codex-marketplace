# Escenarios de defensa conceptual SIENEP

Estos escenarios congelan patrones pedagógicos derivados de una defensa académica anterior. No convierten esa defensa en pauta oficial ni reemplazan las fuentes vigentes de cada proyecto.

## Escenario 1: máscaras antes de comandos

**Consulta:** En modo Profesor de Infraestructura, preguntame por qué usamos máscaras distintas. No empieces pidiendo comandos.

**Debe:** formular una sola pregunta conceptual sobre capacidad, segmentación o crecimiento; pedir evidencia sólo después de comprender el criterio.

## Escenario 2: RAID propuesto

**Respuesta estudiantil:** Implementamos RAID 5 porque nos daba redundancia.

**Debe:** contrastar la afirmación con la fuente actual y clasificarla como implementada y demostrada, implementada sin evidencia, propuesta o no documentada; no aceptar una posibilidad de diseño como hecho.

## Escenario 3: validación negativa de API

**Consulta:** Enseñame cómo defender una validación de fecha desde Programación.

**Debe:** explicar primero regla de negocio, capa responsable y respuesta HTTP; luego proponer una entrada inválida reproducible en Swagger como evidencia.

## Escenario 4: endpoint afirmado

**Respuesta estudiantil:** El endpoint está protegido porque tiene `@PreAuthorize`.

**Debe:** distinguir configuración presente de comportamiento demostrado y pedir casos sin token, sin permiso y autorizado sin perder el foco conceptual.

## Escenario 5: inundación y producto

**Consulta:** Si una inundación del centro de datos deja fuera de servicio la API, ¿es automáticamente riesgo de producto?

**Debe:** responder que el efecto sobre el aplicativo no determina por sí solo la categoría; separar causa externa o técnica, consecuencia y objeto afectado.

## Escenario 6: ISP y failover

**Respuesta estudiantil:** Como tenemos dos ISP y failover, la caída del proveedor es un riesgo técnico.

**Debe:** explicar que una respuesta técnica no cambia automáticamente el origen externo de la causa; después preguntar por evidencia y residual.

## Escenario 7: respuesta oral breve

**Consulta:** Haceme una pregunta de defensa y corregí mi respuesta si me voy por las ramas.

**Debe:** exigir una primera respuesta de 30–60 segundos con veredicto, concepto, decisión SIENEP, evidencia y límite; formular una sola pregunta por turno.

## Escenario 8: contribución y FODA

**Respuesta estudiantil:** Todos hicimos de todo y el equipo trabajó muy bien.

**Debe:** pedir una contribución concreta o un elemento FODA con ejemplo verificable y evitar aceptar una respuesta colectiva evasiva.

## Protocolo RED/GREEN

1. Ejecutar las consultas contra los skills anteriores al cambio y registrar las omisiones.
2. Ejecutar `python3 tests/validate_defensa_real_skills.py`; en RED debe fallar por ausencia del contrato común.
3. Aplicar el mismo conjunto a los skills modificados sin alterar criterios.
4. Confirmar en GREEN una pregunta por turno, prioridad conceptual y evidencia secundaria.
