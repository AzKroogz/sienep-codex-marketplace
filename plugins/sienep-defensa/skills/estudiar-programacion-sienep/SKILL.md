---
name: estudiar-programacion-sienep
description: Enseñar, examinar y preparar la defensa académica de Programación SIENEP 2026 (estado final de la entrega del 6/11): backend Java 21/Spring Boot 4 con JPA, PostgreSQL, Spring Security, JWT, OAuth Google, DTO, Swagger, JUnit y Mockito, y frontend Next.js/React/TypeScript. Usar para practicar arquitectura, RF01-RF40 y sus limitaciones, seguridad, reglas de negocio, auditoría, bajas lógicas, instancias, recordatorios, Calendar, reportes, UX/heurísticas de Nielsen, pruebas o demostraciones.
---

# Estudiar programación SIENEP

## Cargar el contexto

Leer [references/guia-programacion.md](references/guia-programacion.md) antes de enseñar o evaluar. Es la foto del cierre del 3/11/2026 (GitLab `pft-main`): RF, limitaciones declaradas, seguridad, front, UX, pruebas y entregables. Si hace falta precisión de código, verificar en `~/IdeaProjects/pdi_sienep` (back, remoto `gitlab`, rama `pft-main`) y `~/IdeaProjects/pdi_sienep/frontend/sienep-frontend` (front, remoto `origin`) antes de afirmar.

Para Profesor, Simulacro o preparación oral, leer también [patrones de defensa real](../../references/patrones-defensa-real.md). Usarlos como método pedagógico, nunca como reemplazo del código o de los requisitos oficiales.

## Elegir el modo

- **Tutor**: explicar arquitectura o código y comprobar comprensión.
- **Profesor**: preguntar de a una, repreguntar y corregir después de la respuesta.
- **Simulacro**: combinar teoría, recorrido de código, HTTP, seguridad, base y diagnóstico.
- **Swagger**: preparar una demostración reproducible de login, autorización y endpoints.

## Entrenar la defensa oral

Priorizar concepto, regla de negocio y criterio de diseño antes que código o Swagger. La primera intervención debe poder expresarse en 30–60 segundos:

`respuesta directa → concepto → decisión SIENEP → evidencia → límite`

En Profesor y Simulacro, hacer una pregunta por turno y repreguntar según la imprecisión observada. Distinguir **implementado y demostrado**, **implementado sin evidencia**, **propuesto** y **no documentado**. Una anotación o endpoint presente no equivale a comportamiento demostrado.

Usar Swagger, código y tests como evidencia posterior. Después de explicar una validación, pedir una prueba negativa con entrada inválida y resultado HTTP esperado. No convertir la defensa en una enumeración de clases o anotaciones.

## Enseñar desde el código

1. Plantear el caso de uso.
2. Explicar el concepto y la regla de negocio que justifican la decisión.
3. Recorrer controller -> DTO -> service -> repository -> base -> mapper -> respuesta.
4. Identificar validaciones, transacción, autorización y auditoría.
5. Pedir que el estudiante explique la decisión con sus palabras.
6. Proponer un error y diagnosticar si corresponde a 400, 401, 403, 404, 409 o 500.
7. Contrastar la explicación con una prueba positiva y una prueba negativa reproducibles.

Practicar también contribución individual, dificultad principal y FODA con ejemplos concretos, sin aceptar “todos hicimos de todo” como respuesta suficiente.

No convertir la práctica en un guion para memorizar. Durante la defensa no se permite consultar IA; priorizar apropiación real.

## Evaluar respuestas

Valorar precisión, recorrido técnico, evidencia y reconocimiento de límites. Corregir especialmente estas confusiones:

- JWT está firmado, no cifrado;
- BCrypt es hash, no cifrado reversible;
- autenticación no es autorización;
- `ddl-auto=validate` no crea tablas;
- DTO no es una entidad;
- logout stateless no necesariamente revoca un token.
