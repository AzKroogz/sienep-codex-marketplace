# SIENEP Codex Marketplace

Marketplace privado del equipo SIENEP 2026 para estudiar y practicar las defensas de infraestructura GNS3 y programación Spring Boot.

Incluye el plugin `sienep-defensa` con los skills:

- `$estudiar-infraestructura-sienep`
- `$estudiar-programacion-sienep`

El material resume conocimiento producido por el equipo. No incluye credenciales, tokens, proyectos portables, imágenes propietarias ni los PDF originales de la consigna.

## Instalación para el equipo

Cada integrante debe tener acceso al repositorio privado y Codex instalado.

```bash
git clone https://github.com/AzKroogz/sienep-codex-marketplace.git
cd sienep-codex-marketplace
codex plugin marketplace add "$PWD"
codex plugin add sienep-defensa@sienep-equipo
```

Después de instalar, abrir un hilo nuevo para que Codex cargue los skills.

## Ejemplos

```text
Usá $estudiar-infraestructura-sienep en modo profesor y examiname sobre OSPF.
```

```text
Usá $estudiar-programacion-sienep para enseñarme el recorrido de una petición JWT.
```

```text
Hacé un simulacro de defensa con 70% infraestructura y 30% programación.
```
