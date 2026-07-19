# Patrones conceptuales para una defensa SIENEP

## Alcance

Esta referencia resume una **observación pedagógica** de una defensa académica anterior. **No es una pauta oficial** ni prueba el estado de SIENEP 2026. Las guías y fuentes vigentes de Infraestructura, Programación y Gestión de Riesgos tienen prioridad para afirmar hechos.

## Patrón docente observado

La secuencia más frecuente fue:

1. elegir una afirmación, decisión o fila concreta;
2. pedir el concepto o criterio que la sostiene;
3. repreguntar sobre una imprecisión;
4. solicitar evidencia sólo si hace falta comprobar lo afirmado;
5. preguntar por consecuencia, alternativa o límite.

La defensa se debilitó cuando el estudiante narró mucho antes de contestar, confundió una propuesta con algo implementado o recordó una herramienta sin explicar la decisión.

## Contrato oral

Preparar una primera respuesta de 30–60 segundos:

`respuesta directa → concepto → decisión SIENEP → evidencia → límite`

- **Respuesta directa**: contestar el veredicto pedido.
- **Concepto**: definir el criterio relevante con palabras propias.
- **Decisión SIENEP**: aplicarlo al caso realmente verificado.
- **Evidencia**: indicar qué observación demostraría la afirmación.
- **Límite**: reconocer residual, alcance o dato no documentado.

La evidencia se clasifica como:

- **Implementado y demostrado**: existe el control y una prueba reproducible confirma el comportamiento.
- **Implementado sin evidencia**: el artefacto existe, pero falta demostrar el resultado.
- **Propuesto**: es una decisión de diseño o mejora futura, no una implementación actual.
- **No documentado**: la fuente no permite sostener la afirmación.

## Infraestructura

Preguntar primero por concepto y criterio:

- ¿Por qué se eligieron máscaras diferentes y qué efecto tienen sobre capacidad y crecimiento?
- ¿Qué beneficio y qué riesgo introduce que TI alcance varias redes?
- ¿Qué diferencia funcional existe entre capa 2 y capa 3?
- ¿Qué criterio determina qué segmentos usan DHCP y el tamaño de sus rangos?
- ¿Qué problema resuelve el firewall/router elegido y por qué es adecuado?
- ¿Qué redundancia existe y qué punto único permanece?
- ¿RAID, fibra, UPS o generador están implementados o sólo presupuestados/propuestos?

Después pedir evidencia: salida `show`, configuración, prueba de falla o recorrido. No comenzar por sintaxis ni aceptar configuración presente como operación demostrada.

## Programación

Preguntar primero por concepto, regla de negocio y responsabilidad:

- ¿Qué problema evita esta validación y en qué capa debe ejecutarse?
- ¿Por qué corresponde 400, 401, 403, 404 o 409?
- ¿Cuál es la diferencia entre autenticación y autorización?
- ¿Por qué usar DTO, baja lógica, auditoría o `ddl-auto=validate`?
- ¿Qué parte está implementada, cuál es parcial y cuál es diseño futuro?

Después pedir una prueba positiva y una **prueba negativa** en Swagger o tests. Una anotación, clase o endpoint existente no equivale por sí sola a comportamiento demostrado.

## Gestión de Riesgos

Preguntar por una fila concreta y avanzar según la respuesta:

`clasificación → causa/evento/consecuencia → control de la causa → tratamiento → evidencia → residual`

Patrones para comprobar:

- Que el aplicativo sufra el impacto no convierte automáticamente una inundación o falla del entorno en riesgo de producto.
- Una pauta difusa amenaza alcance y ejecución; debe razonarse desde el proyecto o entorno.
- La caída de un proveedor puede ser externa aunque se mitigue con una solución técnica como failover.
- La dificultad con una herramienta será de personas o técnica según la causa redactada, no sólo según una lista de categorías.
- Tener mitigación no elimina el residual ni cambia por sí solo la categoría.

La configuración técnica sólo evidencia el tratamiento. La explicación principal sigue siendo de Gestión de Riesgos: causa, exposición, decisión, dimensión reducida y residual.

## Repreguntas

Formular una pregunta por turno. Elegir la siguiente según la debilidad observada:

| Debilidad | Repregunta útil |
|---|---|
| Contestó con una herramienta | ¿Qué problema resolvía y por qué era adecuada? |
| Confundió efecto con categoría | ¿Dónde nace la causa y quién puede controlarla? |
| Afirmó implementación | ¿Qué fuente y qué resultado observado lo demuestran? |
| Dio evidencia sin concepto | ¿Qué decisión o dimensión sostiene esa prueba? |
| Omitió límites | ¿Qué escenario sigue abierto después del control? |
| Se extendió sin responder | Respondé primero el veredicto en una frase: ¿cuál es? |

## Fallas y tiempo

- Si una demostración falla, reconocerlo, explicar qué debía ocurrir y usar evidencia alternativa ya verificada. No inventar éxito.
- Cronometrar exposición y demostraciones. Mostrar todo no compensa una respuesta sin foco.
- En un FODA, exigir un ejemplo concreto por fortaleza, oportunidad, debilidad o amenaza.
- Ante “todos hicimos de todo”, pedir una contribución individual verificable y cómo se integra con el trabajo común.
