#!/usr/bin/env python3
"""Comprueba que el plugin sienep-testing esté completo para Codex y Claude Code."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/sienep-testing"
SKILL = PLUGIN / "skills/gestionar-testing-sienep"

marketplaces = {
    ROOT / ".agents/plugins/marketplace.json": "sienep-testing",
    ROOT / ".claude-plugin/marketplace.json": "sienep-testing",
}
for manifiesto, plugin in marketplaces.items():
    datos = json.loads(manifiesto.read_text(encoding="utf-8"))
    nombres = [p["name"] for p in datos["plugins"]]
    assert plugin in nombres, f"{manifiesto.name}: falta {plugin}"

for manifiesto in [PLUGIN / ".codex-plugin/plugin.json", PLUGIN / ".claude-plugin/plugin.json"]:
    datos = json.loads(manifiesto.read_text(encoding="utf-8"))
    assert datos["name"] == "sienep-testing", manifiesto

texto = (SKILL / "SKILL.md").read_text(encoding="utf-8")
assert texto.startswith("---\nname: gestionar-testing-sienep\n"), "frontmatter incorrecto"
for seccion in ["## Reglas", "## Flujos", "## Errores comunes"]:
    assert seccion in texto, f"falta la sección {seccion}"
for idea in ["programa real", "al menos 2 assertions", "versión nueva", "Obsoleto", "credenciales"]:
    assert idea in texto, f"falta la regla: {idea}"

referencias = ["letra-testing.md", "comportamiento-programa.md", "testlink-operaciones.md", "planillas-tecnicas.md", "estado-testing.md"]
for referencia in referencias:
    assert (SKILL / "references" / referencia).exists(), f"falta {referencia}"
    assert referencia in texto, f"SKILL.md no enlaza {referencia}"

assert (SKILL / "agents/openai.yaml").exists(), "falta agents/openai.yaml"

for archivo in [SKILL / "SKILL.md", *sorted((SKILL / "references").glob("*.md"))]:
    contenido = archivo.read_text(encoding="utf-8")
    assert "~/Escritorio" not in contenido, f"{archivo.name}: ruta personal"
    assert "/home/" not in contenido, f"{archivo.name}: ruta personal"
    for prohibido in ["contraseña:", "password=", "Bearer ey"]:
        assert prohibido not in contenido, f"{archivo.name}: posible credencial ({prohibido})"

print("OK: plugin sienep-testing completo y sin rutas personales ni credenciales")
