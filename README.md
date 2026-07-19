# SIENEP Codex Marketplace

Marketplace privado del equipo SIENEP 2026 para estudiar y practicar las defensas de infraestructura GNS3 y programación Spring Boot.

Incluye el plugin `sienep-defensa` con los skills:

- `$estudiar-infraestructura-sienep`
- `$estudiar-programacion-sienep`
- `$estudiar-gestion-riesgos-sienep`

El material resume conocimiento producido por el equipo. No incluye credenciales, tokens, proyectos portables, imágenes propietarias ni los PDF originales de la consigna.

## Instalación recomendada para el equipo

Cada integrante debe tener Codex instalado y acceso al repositorio privado en GitHub. Registrar el repositorio como marketplace Git permite que Codex refresque su snapshot sin depender de un clon manual.

```bash
codex plugin marketplace add AzKroogz/sienep-codex-marketplace --ref main
codex plugin add sienep-defensa@sienep-equipo
```

Después de instalar, abrir un hilo nuevo para que Codex cargue los skills.

## Actualizar el plugin

Actualizar primero el snapshot del marketplace Git y después reinstalar el plugin:

```bash
codex plugin marketplace upgrade sienep-equipo
codex plugin add sienep-defensa@sienep-equipo
codex plugin list
```

`marketplace upgrade` obtiene el `main` más reciente. `plugin add` instala la versión indicada por el nuevo manifiesto. Son dos pasos distintos y ambos son necesarios.

En la salida de `codex plugin list`, comprobar que `sienep-defensa@sienep-equipo` figure como `installed, enabled` y revisar su versión. Después abrir un hilo nuevo; un hilo que ya estaba abierto puede conservar los skills anteriores.

## Migrar una instalación basada en un clon local

Las instrucciones antiguas registraban una carpeta clonada como marketplace. Verificar la fuente actual:

```bash
codex plugin marketplace list
```

Si la raíz de `sienep-equipo` apunta a una carpeta personal como `/home/.../sienep-codex-marketplace`, migrarla una sola vez:

```bash
codex plugin marketplace remove sienep-equipo
codex plugin marketplace add AzKroogz/sienep-codex-marketplace --ref main
codex plugin add sienep-defensa@sienep-equipo
```

Luego usar siempre el procedimiento de `Actualizar el plugin` y abrir un hilo nuevo.

## Conservar deliberadamente un clon local

Quien desarrolla el marketplace puede mantener la fuente local. En ese caso, `marketplace upgrade` no actualiza la carpeta: hay que actualizar Git y reinstalar.

```bash
cd /ruta/al/sienep-codex-marketplace
git pull --ff-only origin main
codex plugin add sienep-defensa@sienep-equipo
codex plugin list
```

Si la versión no cambia, comprobar que el `git pull` se ejecutó en el mismo directorio mostrado por `codex plugin marketplace list`.

## Ejemplos

```text
Usá $estudiar-infraestructura-sienep en modo profesor y examiname sobre OSPF.
```

```text
Usá $estudiar-programacion-sienep para enseñarme el recorrido de una petición JWT.
```

```text
Usá $estudiar-gestion-riesgos-sienep para recorrer nuestra planilla desde cero.
```

```text
Hacé un simulacro de defensa con 70% infraestructura y 30% programación.
```
