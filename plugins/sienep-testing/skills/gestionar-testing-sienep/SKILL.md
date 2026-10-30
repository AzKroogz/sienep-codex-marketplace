---
name: gestionar-testing-sienep
description: Usar al trabajar en el testing de SIENEP 2026 (Proyecto Final de Tecnicatura): diseñar, auditar, crear o corregir casos de prueba en TestLink (suites web, base de datos y servicios/API), planillas de técnicas (clases de equivalencia, valores límite, tablas de decisión), planes, builds y ejecuciones, defectos en Mantis, o revisar qué falta para cumplir la letra del área de Testing.
---

# Testing SIENEP 2026

Guía para el trabajo de testing del equipo: qué pide la letra, cómo se comporta el programa real, cómo operar TestLink y en qué estado quedó el trabajo.

## Antes de empezar

1. Leer [estado-testing.md](references/estado-testing.md): qué está hecho, qué falta y las decisiones ya tomadas. No repetir auditorías cerradas.
2. Si la tarea toca casos o planillas, leer [comportamiento-programa.md](references/comportamiento-programa.md).
3. Verificar el estado real antes de afirmar: exportar la suite de TestLink y leer el código (`develop` del frontend y del backend). La memoria y esta guía son contexto, no verificación.

## Reglas

1. **Los casos prueban el programa real.** Cada caso se contrasta con el código y la pantalla real: botones, campos, mensajes, límites y permisos. No se crean casos sobre funciones que no existen (ejemplo: "motivo de derivación", desbloqueo de cuentas por un administrador).
2. **Que un caso falle está bien.** Si el caso describe bien una regla y el sistema no la cumple, se deja fallar y va a Mantis. Si el caso está mal escrito (navegación inexistente, dato imposible de ingresar), se corrige el caso.
3. **La planilla tiene el comportamiento real del programa.** Si un caso espera otra cosa, la diferencia se anota en el contraste; no se ajusta la planilla al caso.
4. **Suite de servicios:** cada caso lleva **al menos 2 assertions** numeradas en el resultado esperado ("Assertion 1: …"): código HTTP + algo del body o del efecto.
5. **Editar un caso existente = versión nueva** del mismo caso (mismo ID). La versión nueva queda en **Final** y la anterior en **Obsoleto**. No se borran casos ni versiones.
6. **Los casos nuevos se cargan en Final.**
7. **No se ingresan credenciales ni contraseñas** contra el sistema desplegado: la ejecución en producción la hace el equipo. TestLink se opera con la sesión que abre el usuario.
8. **Cambios en TestLink o Mantis** (crear, importar, cambiar estados): con pedido explícito del usuario y verificados después de hacerlos.

## Flujos

| Tarea | Cómo | Referencia |
|---|---|---|
| Saber qué falta para cumplir la letra | Comparar artefacto por artefacto | [letra-testing.md](references/letra-testing.md) |
| Auditar casos contra el programa | Exportar la suite → leer cada caso → contrastar con el código → clasificar (coincide / espera otra cosa / pasos a corregir / fuera del programa) | [comportamiento-programa.md](references/comportamiento-programa.md) |
| Crear casos | XML de importación → importar en la suite del módulo → verificar pasos y estado | [testlink-operaciones.md](references/testlink-operaciones.md) |
| Corregir casos | XML con `externalid` → importar con "ID externo" + "Crear una nueva versión" → nueva = Final, vieja = Obsoleto | [testlink-operaciones.md](references/testlink-operaciones.md) |
| Planillas de técnicas | Una por módulo, con pestañas por técnica y casos de TestLink | [planillas-tecnicas.md](references/planillas-tecnicas.md) |
| Planes, builds y ejecuciones | Builds con el tipo en el nombre | [letra-testing.md](references/letra-testing.md) |

## Errores comunes

| Error | Corrección |
|---|---|
| Escribir pasos con botones que no existen ("Nuevo estudiante") | Leer la pantalla en el código: el alta es Configuración → Usuarios → Nueva cuenta |
| Esperar un mensaje "superó el máximo" en un campo con `maxLength` | El navegador no deja escribir de más: el resultado es "no permite escribir más de N caracteres" |
| Esperar mensajes propios en campos vacíos | Los campos usan `required` nativo: el navegador frena el envío |
| Usar fechas con segundos o fechas pasadas en recordatorios | `datetime-local` no tiene segundos; la fecha debe ser futura: se crea el día anterior |
| Cédula con puntos y guion | El campo exige 8 dígitos (41234563) |
| Buscar el estado de la baja en `estudiantes` | Está en `usuarios.estado_usuario` |
| Crear casos repetidos al importar | Importar con "no importar si tiene el mismo nombre" para casos nuevos |
| Sobrescribir la versión vigente | Siempre crear una versión nueva y dejar la anterior en Obsoleto |
