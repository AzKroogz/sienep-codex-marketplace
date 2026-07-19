#!/usr/bin/env python3
"""Comprueba que el README permita instalar y actualizar desde Git."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")


def require(term: str, context: str) -> None:
    assert term in README, f"{context}: falta {term!r}"


require(
    "codex plugin marketplace add AzKroogz/sienep-codex-marketplace --ref main",
    "instalación desde Git",
)
require(
    "codex plugin marketplace upgrade sienep-equipo",
    "actualización del snapshot Git",
)
require(
    "codex plugin marketplace remove sienep-equipo",
    "migración desde marketplace local",
)
require("codex plugin marketplace list", "diagnóstico de la fuente")
require("git pull --ff-only origin main", "alternativa para clones locales")
require("codex plugin list", "verificación de versión")
require("hilo nuevo", "recarga de skills")
require("$estudiar-gestion-riesgos-sienep", "catálogo completo de skills")

assert README.count("codex plugin add sienep-defensa@sienep-equipo") >= 2, (
    "la instalación y la actualización deben reinstalar el plugin"
)
assert 'codex plugin marketplace add "$PWD"' not in README, (
    "la instalación principal no debe registrar un clon local"
)

print("OK: README documenta instalación Git, actualización y migración")
