# Diseño: actualizaciones del marketplace SIENEP desde Git

## Problema

El README actual indica clonar el repositorio y registrar `$PWD` como marketplace local. Codex puede reinstalar desde esa carpeta, pero no puede refrescarla desde GitHub. Los compañeros quedan en una versión anterior si no ejecutan `git pull`, reinstalan el plugin y abren un hilo nuevo.

## Solución

La instalación recomendada registrará `AzKroogz/sienep-codex-marketplace` como marketplace Git siguiendo `main`. El flujo de actualización será:

1. `codex plugin marketplace upgrade sienep-equipo`;
2. `codex plugin add sienep-defensa@sienep-equipo`;
3. comprobar la versión con `codex plugin list`;
4. abrir un hilo nuevo.

El README conservará una sección de migración para instalaciones locales existentes: identificar la raíz con `codex plugin marketplace list`, retirar la fuente local, registrar la fuente Git y reinstalar el plugin. También documentará un flujo alternativo con `git pull` para quien decida conservar el clon local.

## Regresión

Un validador comprobará que la instalación principal usa la fuente Git, que existe el comando `marketplace upgrade`, que se reinstala el plugin, que se pide un hilo nuevo y que no vuelve a recomendarse `marketplace add "$PWD"` como instalación principal.

## Criterios de aceptación

- Un compañero nuevo puede instalar sin clonar manualmente el repositorio.
- Un compañero con marketplace Git puede refrescarlo con un comando de upgrade.
- Un compañero con clon local recibe una ruta de migración o actualización explícita.
- La documentación diferencia refrescar el marketplace de reinstalar el plugin.
- La versión se verifica desde `codex plugin list` y los cambios se prueban en un hilo nuevo.
