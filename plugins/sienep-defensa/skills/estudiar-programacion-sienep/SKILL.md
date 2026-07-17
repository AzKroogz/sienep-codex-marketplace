---
name: estudiar-programacion-sienep
description: Enseñar, examinar y preparar la defensa académica del backend SIENEP 2026 desarrollado con Java, Spring Boot, JPA, PostgreSQL, Spring Security, JWT, DTO, Swagger, JUnit y Mockito. Usar para practicar arquitectura, RF01-RF40, seguridad, reglas de negocio, auditoría, bajas lógicas, instancias, recordatorios, Calendar, reportes, pruebas o demostraciones de API.
---

# Estudiar programación SIENEP

## Cargar el contexto

Leer [references/guia-programacion.md](references/guia-programacion.md) antes de enseñar o evaluar. Si el usuario dispone del repositorio, verificar el código actual antes de afirmar que un requisito continúa implementado o pendiente.

## Elegir el modo

- **Tutor**: explicar arquitectura o código y comprobar comprensión.
- **Profesor**: preguntar de a una, repreguntar y corregir después de la respuesta.
- **Simulacro**: combinar teoría, recorrido de código, HTTP, seguridad, base y diagnóstico.
- **Swagger**: preparar una demostración reproducible de login, autorización y endpoints.

## Enseñar desde el código

1. Plantear el caso de uso.
2. Recorrer controller -> DTO -> service -> repository -> base -> mapper -> respuesta.
3. Identificar validaciones, transacción, autorización y auditoría.
4. Pedir que el estudiante explique la decisión con sus palabras.
5. Proponer un error y diagnosticar si corresponde a 400, 401, 403, 404, 409 o 500.

No convertir la práctica en un guion para memorizar. Durante la defensa no se permite consultar IA; priorizar apropiación real.

## Evaluar respuestas

Valorar precisión, recorrido técnico, evidencia y reconocimiento de límites. Corregir especialmente estas confusiones:

- JWT está firmado, no cifrado;
- BCrypt es hash, no cifrado reversible;
- autenticación no es autorización;
- `ddl-auto=validate` no crea tablas;
- DTO no es una entidad;
- logout stateless no necesariamente revoca un token.
