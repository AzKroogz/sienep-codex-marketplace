#!/usr/bin/env python3
"""Regresión estructural del patrón conceptual de defensa en los tres skills."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/sienep-defensa"
SKILLS = {
    "infraestructura": PLUGIN / "skills/estudiar-infraestructura-sienep/SKILL.md",
    "programación": PLUGIN / "skills/estudiar-programacion-sienep/SKILL.md",
    "riesgos": PLUGIN / "skills/estudiar-gestion-riesgos-sienep/SKILL.md",
}
REFERENCE = PLUGIN / "references/patrones-defensa-real.md"


def require_all(text: str, terms: list[str], context: str) -> None:
    missing = [term for term in terms if term not in text]
    assert not missing, f"{context}: faltan {missing}"


common = [
    "respuesta directa",
    "concepto",
    "decisión sienep",
    "evidencia",
    "límite",
    "30–60 segundos",
    "una pregunta por turno",
    "implementado y demostrado",
    "implementado sin evidencia",
    "propuesto",
    "no documentado",
    "patrones-defensa-real.md",
]

texts = {name: path.read_text(encoding="utf-8").lower() for name, path in SKILLS.items()}
for name, content in texts.items():
    require_all(content, common, name)

require_all(
    texts["infraestructura"],
    ["conceptos antes", "comandos", "criterio", "configuración como evidencia"],
    "infraestructura conceptual",
)
require_all(
    texts["programación"],
    ["regla de negocio", "swagger", "prueba negativa", "comportamiento demostrado"],
    "programación conceptual",
)
require_all(
    texts["riesgos"],
    ["80 %", "causa", "origen", "extern", "mitigación técnica"],
    "riesgos conceptuales",
)

reference = REFERENCE.read_text(encoding="utf-8").lower()
require_all(
    reference,
    ["observación pedagógica", "no es una pauta oficial", "infraestructura", "programación", "gestión de riesgos", "foda"],
    "referencia compartida",
)
assert "nativostec" not in reference, "la referencia debe permanecer anonimizada"
assert ".mkv" not in reference, "no debe incluirse la ruta del video"

print("OK: los tres skills incorporan el patrón conceptual de defensa real")
