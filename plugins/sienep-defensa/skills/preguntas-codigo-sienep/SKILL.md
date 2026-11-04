---
name: preguntas-codigo-sienep
description: Banco de preguntas de defensa sobre el código de Programación SIENEP 2026 (backend Spring Boot y frontend Next.js, rama pft-main), con respuesta modelo de 30 segundos, ubicación exacta en el código, repreguntas y trampas típicas. Usar para simulacros de defensa oral, repasar por módulo, practicar "mostrame dónde está en el código", o cuando el usuario pida preguntas posibles del docente sobre seguridad, JWT, OAuth, estudiantes, instancias, recordatorios, Calendar, roles, reportes, auditoría, front, base de datos, pruebas o trabajo en equipo.
---

# Preguntas de defensa sobre el código SIENEP

Objetivo: que el estudiante pueda explicar y mostrar su código **sin IA** durante la defensa. Cada pregunta del banco trae una respuesta modelo, la ubicación en el código, repreguntas y la trampa típica.

## Fuente

- Bancos por área (leer solo el que se va a practicar):
  - [references/01-seguridad.md](references/01-seguridad.md): login, JWT, logout, OAuth, primer acceso, errores HTTP.
  - [references/02-estudiantes-instancias.md](references/02-estudiantes-instancias.md): validaciones, transacciones, Specification, baja lógica, datos sensibles, instancias, clonación, ID.
  - [references/03-recordatorios-admin-reportes.md](references/03-recordatorios-admin-reportes.md): recurrencia, Calendar, notificaciones, auditoría, roles, categorías, reportes.
  - [references/04-front-bd-pruebas-equipo.md](references/04-front-bd-pruebas-equipo.md): front, base de datos y migraciones, pruebas, despliegue, preguntas de equipo.
- Contexto general y limitaciones: skill `estudiar-programacion-sienep` (`references/guia-programacion.md`).
- Rutas del back relativas a `src/main/java/com/sienep/pdi_sienep3/` en `~/IdeaProjects/pdi_sienep` (remoto `gitlab`, rama `pft-main`). Rutas del front relativas a `~/IdeaProjects/pdi_sienep/frontend/sienep-frontend` (remoto `origin`, rama `pft-main`).
- El banco es una foto del 3/11/2026. Si el usuario pregunta por un detalle que no está, o duda de una línea, abrir el archivo (`git show gitlab/pft-main:<ruta>`) antes de afirmar. No inventar métodos ni números.

## Modos

- **Simulacro** (por defecto si pide "preguntame"):
  1. Elegir una pregunta, mezclando áreas, y hacerla tal como la haría un docente, sin pistas.
  2. Esperar la respuesta. No mostrar la respuesta modelo antes.
  3. Corregir en este orden: qué estuvo bien, qué faltó o fue impreciso, la respuesta modelo de 30 segundos y una repregunta.
  4. Máximo dos repreguntas sobre el mismo tema; después cambiar de área.
  5. Cada 5 preguntas, cerrar con: dominadas, flojas y qué repasar.
- **Repaso por módulo:** mostrar pregunta + respuesta modelo + dónde está en el código, de a 3 o 4 por vez, y pedir que la diga con sus palabras.
- **"Mostrame dónde está":** pedir que encuentre en el IDE dónde se hace algo (por ejemplo, "¿dónde se invalida el token al cerrar sesión?"). Validar con la ruta del banco.
- **Trampas:** hacer solo las preguntas con trampa típica, para entrenar las confusiones frecuentes.

## Cómo evaluar

Formato de respuesta esperado, en 30 a 60 segundos:

`respuesta directa → concepto → decisión SIENEP → evidencia (código o prueba) → límite`

- Exigir que responda primero el veredicto. Si narra sin responder: "Decime primero la respuesta en una frase."
- Una anotación o clase existente no es una explicación: pedir qué problema resuelve.
- Pedir una prueba negativa cuando corresponda: "¿Qué entrada la hace fallar y qué código HTTP devuelve?"
- Si nombra una limitación declarada (RF05, RF14, RF15, RF22, RF31, RF33, RNF01…), valorarlo: suma credibilidad.
- Ante "todos hicimos de todo", pedir una contribución individual concreta.
- No dar el guion para memorizar: el objetivo es que lo entienda. Si se traba, dar una pista (el concepto), no la respuesta.
