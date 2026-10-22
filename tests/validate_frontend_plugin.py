#!/usr/bin/env python3
"""Comprueba que el plugin sienep-frontend esté completo para Codex y Claude Code."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/sienep-frontend"
SKILL = PLUGIN / "skills/construir-frontend-sienep"

for manifiesto in [
    ROOT / ".agents/plugins/marketplace.json",
    ROOT / ".claude-plugin/marketplace.json",
    PLUGIN / ".codex-plugin/plugin.json",
    PLUGIN / ".claude-plugin/plugin.json",
]:
    datos = json.loads(manifiesto.read_text(encoding="utf-8"))
    assert datos["name"] in ("sienep-equipo", "sienep-frontend"), manifiesto

texto = (SKILL / "SKILL.md").read_text(encoding="utf-8")
assert "## GUARDRAIL" in texto, "falta el guardrail"
assert "Herramientas permitidas" in texto, "falta la lista de herramientas"

for archivo in [SKILL / "SKILL.md", *sorted((SKILL / "references").glob("*.md"))]:
    contenido = archivo.read_text(encoding="utf-8")
    assert "~/Escritorio" not in contenido, f"{archivo.name}: ruta personal"
    assert "/home/" not in contenido, f"{archivo.name}: ruta personal"

for referencia in ["plan-reestructura.md", "registro-decisiones.md", "auditoria-frontend.md"]:
    assert (SKILL / "references" / referencia).exists(), f"falta {referencia}"

print("OK: plugin sienep-frontend completo y sin rutas personales")
