# Git Marketplace Updates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Permitir que el equipo actualice el plugin SIENEP desde GitHub sin depender de un clon local desactualizado.

**Architecture:** El README usará una fuente Git para instalaciones nuevas y documentará actualización, migración y verificación. Un validador Python protegerá los comandos esenciales del flujo.

**Tech Stack:** Markdown, Python 3 y Codex plugin CLI.

## Global Constraints

- Marketplace: `sienep-equipo`.
- Repositorio: `AzKroogz/sienep-codex-marketplace`.
- Rama: `main`.
- Plugin: `sienep-defensa@sienep-equipo`.
- Abrir un hilo nuevo después de reinstalar.

---

### Task 1: Regresión RED

**Files:**
- Create: `tests/validate_marketplace_update_docs.py`
- Test: `README.md`

- [ ] Escribir un validador que exija instalación Git, upgrade, reinstalación, migración, verificación y nuevo hilo.
- [ ] Ejecutar `python3 tests/validate_marketplace_update_docs.py` y confirmar que falla por el flujo local actual.
- [ ] Commit: `test: exigir actualizaciones del marketplace Git`.

### Task 2: Documentación GREEN

**Files:**
- Modify: `README.md`
- Test: `tests/validate_marketplace_update_docs.py`

- [ ] Reemplazar la instalación principal basada en clon por `codex plugin marketplace add AzKroogz/sienep-codex-marketplace --ref main`.
- [ ] Agregar actualización normal, migración desde marketplace local, alternativa local y solución de problemas.
- [ ] Ejecutar el validador nuevo y las regresiones existentes.
- [ ] Commit: `docs: habilitar actualizaciones del marketplace Git`.

### Task 3: Publicación

**Files:**
- Modify: `plugins/sienep-defensa/.codex-plugin/plugin.json`

- [ ] Actualizar cachebuster y validar el plugin.
- [ ] Ejecutar todos los validadores y `git diff --check`.
- [ ] Crear PR, fusionar a `main`, actualizar el checkout local y reinstalar el plugin.
- [ ] Verificar `HEAD == origin/main` y versión instalada.
