#!/usr/bin/env python3
"""Structural regression checks for the SIENEP risk-management skill."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/sienep-defensa/skills/estudiar-gestion-riesgos-sienep/SKILL.md"
SCENARIOS = ROOT / "tests/gestion-riesgos-scenarios.md"
MANIFEST = ROOT / "plugins/sienep-defensa/.codex-plugin/plugin.json"


def require_all(text: str, terms: list[str], context: str) -> None:
    missing = [term for term in terms if term not in text]
    assert not missing, f"{context}: faltan {missing}"


skill = SKILL.read_text(encoding="utf-8")
scenarios = SCENARIOS.read_text(encoding="utf-8")
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

require_all(
    skill.lower(),
    [
        "concepto acertado",
        "imprecisión",
        "campo o evidencia de la planilla",
        "reformulación rigurosa",
        "repregunta breve",
    ],
    "contrato de corrección",
)
require_all(
    skill.lower(),
    [
        "pasar gradualmente a profesor",
        "concepto",
        "aplicación sienep",
        "justificación",
        "evidencia",
        "honestidad sobre límites",
    ],
    "transición y rúbrica de Simulacro",
)
require_all(
    skill.lower(),
    [
        "tiene prioridad",
        "todas las hojas relevantes",
        "cada fila",
        "totales",
        "evolución",
        "vigente",
        "histórico",
    ],
    "prioridad de una planilla nueva",
)
require_all(
    scenarios,
    [
        "Escenario 6: corrección multiturmo y transición",
        "Escenario 7: rúbrica de Simulacro",
        "Escenario 8: prioridad de una planilla nueva",
        "Evidencia GREEN reproducible y versionada",
        "Resultado observado",
    ],
    "escenarios y evidencia GREEN",
)
assert "/tmp/green_riesgos" not in scenarios, "GREEN no debe depender de /tmp"

for field in ("description",):
    require_all(
        manifest[field].lower(),
        ["infraestructura", "programación", "gestión de riesgos"],
        f"plugin.json {field}",
    )
require_all(
    manifest["interface"]["shortDescription"].lower(),
    ["infraestructura", "programación", "riesgos"],
    "plugin.json shortDescription",
)

print("OK: estructura pedagógica, fuente nueva, GREEN durable y manifiesto")
