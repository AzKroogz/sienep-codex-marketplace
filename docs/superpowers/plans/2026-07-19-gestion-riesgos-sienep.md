# Gestión de Riesgos SIENEP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Agregar al plugin `sienep-defensa` una tercera habilidad portátil que enseñe y evalúe Gestión de Riesgos desde cero usando la planilla SIENEP como caso histórico verificable.

**Architecture:** La habilidad tendrá un `SKILL.md` corto para el flujo pedagógico y una referencia extensa con conceptos, evolución por sprint, casos e inconsistencias. Un archivo de escenarios documentará RED y GREEN; el manifiesto expondrá la tercera materia sin fusionar sus hallazgos con Infraestructura o Programación.

**Tech Stack:** Codex Skills Markdown, YAML de interfaz, JSON de plugin, validadores Python de `skill-creator` y `plugin-creator`, Git/GitHub.

## Global Constraints

- Gestión de Riesgos es una materia independiente; testing técnico solo aparece como evidencia.
- Mantener separados los hallazgos de Infraestructura GNS3 y Programación Spring Boot.
- Tratar cifras y estados extraídos de la planilla como históricos y recalcular ante una versión nueva.
- Enseñar decisiones y exigir evidencia; no ofrecer un guion para memorizar.
- No modificar `/home/nicolas/Descargas/Planilla de Gestión de Riesgos .xlsx`.

---

### Task 1: Escenarios RED de recuperación y conducta

**Files:**
- Create: `tests/gestion-riesgos-scenarios.md`

**Interfaces:**
- Consumes: plugin actual con dos habilidades y especificación aprobada.
- Produces: cinco consultas, criterios observables y resultados RED/GREEN reutilizables.

- [ ] **Step 1: Definir los escenarios antes de crear la habilidad**

Incluir escenarios para: enseñanza desde cero; defensa del riesgo de hardware; detección de `2 × 3 ≠ 4`; crítica de evidencias vagas; y modo Profesor con una pregunta por turno.

- [ ] **Step 2: Ejecutar RED sin la habilidad nueva**

Despachar un agente con el plugin actual y la consulta de auditoría. Registrar literalmente si mezcla materias, acepta afirmaciones como evidencia, omite inconsistencias o no puede explicar decisiones de la planilla.

Expected: al menos un criterio esencial falla porque no existe una habilidad ni referencia de Gestión de Riesgos.

- [ ] **Step 3: Registrar la línea base**

Agregar a `tests/gestion-riesgos-scenarios.md` una tabla con consulta, omisión observada y resultado `Falla`.

- [ ] **Step 4: Commit**

```bash
git add tests/gestion-riesgos-scenarios.md docs/superpowers/plans/2026-07-19-gestion-riesgos-sienep.md
git commit -m "test: define risk management skill scenarios"
```

### Task 2: Habilidad y guía de Gestión de Riesgos

**Files:**
- Create: `plugins/sienep-defensa/skills/estudiar-gestion-riesgos-sienep/SKILL.md`
- Create: `plugins/sienep-defensa/skills/estudiar-gestion-riesgos-sienep/agents/openai.yaml`
- Create: `plugins/sienep-defensa/skills/estudiar-gestion-riesgos-sienep/references/guia-gestion-riesgos.md`
- Modify: `tests/gestion-riesgos-scenarios.md`

**Interfaces:**
- Consumes: planilla histórica, criterios RED y separación de contextos.
- Produces: `$estudiar-gestion-riesgos-sienep` con modos Tutor, Profesor, Simulacro y Auditoría.

- [ ] **Step 1: Crear `SKILL.md` mínimo**

El flujo deberá: cargar la referencia; elegir modo; enseñar `concepto → SIENEP → decisión → evidencia → resultado → límite`; formular una pregunta por vez; y distinguir dato, cálculo, evidencia e inferencia.

- [ ] **Step 2: Crear la referencia completa**

Incluir definiciones, matriz de campos, exposición `P × I`, evolución `65 → 31 → 28 → 24`, riesgos 1–16, decisiones defendibles, inconsistencias, evidencia fuerte y banco graduado de preguntas.

- [ ] **Step 3: Crear metadatos de interfaz**

```yaml
interface:
  display_name: "Estudiar Gestión de Riesgos SIENEP"
  short_description: "Prepara la defensa de gestión de riesgos"
  default_prompt: "Usa $estudiar-gestion-riesgos-sienep para enseñarme desde cero y examinarme sobre la planilla de riesgos SIENEP."
```

- [ ] **Step 4: Ejecutar GREEN con la habilidad**

Repetir los escenarios con un agente que reciba la habilidad y referencia nuevas. Confirmar que explica desde cero, mantiene áreas separadas, detecta inconsistencias, exige evidencia y pregunta de a una.

- [ ] **Step 5: Registrar GREEN y ajustar brechas observadas**

Actualizar `tests/gestion-riesgos-scenarios.md` con criterios recuperados y cualquier corrección mínima requerida.

- [ ] **Step 6: Validar la habilidad y commit**

```bash
python3 /home/nicolas/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/sienep-defensa/skills/estudiar-gestion-riesgos-sienep
git add plugins/sienep-defensa/skills/estudiar-gestion-riesgos-sienep tests/gestion-riesgos-scenarios.md
git commit -m "feat: add SIENEP risk management tutor"
```

### Task 3: Integración, cachebuster y publicación

**Files:**
- Modify: `plugins/sienep-defensa/.codex-plugin/plugin.json`

**Interfaces:**
- Consumes: tercera habilidad validada.
- Produces: plugin descubrible, instalable y publicado mediante PR a `main`.

- [ ] **Step 1: Actualizar presentación del plugin**

Agregar `gestion-de-riesgos` a `keywords`, mencionar las tres materias en descripción larga y reemplazar un prompt inicial por `Enseñame Gestión de Riesgos desde cero usando nuestra planilla.` Mantener un máximo de tres prompts.

- [ ] **Step 2: Actualizar cachebuster con el helper**

```bash
python3 /home/nicolas/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py plugins/sienep-defensa
```

- [ ] **Step 3: Ejecutar validación completa**

```bash
python3 /home/nicolas/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/sienep-defensa
python3 /home/nicolas/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/sienep-defensa/skills/estudiar-gestion-riesgos-sienep
git diff --check
```

Expected: ambos validadores terminan con éxito y `git diff --check` no produce salida.

- [ ] **Step 4: Commit de integración**

```bash
git add plugins/sienep-defensa/.codex-plugin/plugin.json
git commit -m "chore: expose risk management skill"
```

- [ ] **Step 5: Publicar y fusionar**

Pushear `agent/add-risk-management-skill`, crear una PR lista para revisión contra `main`, verificar sus checks y fusionarla por merge commit o squash según permita el repositorio.

- [ ] **Step 6: Verificar `main` remoto**

Confirmar mediante GitHub que la PR está fusionada y que `main` contiene los archivos de la tercera habilidad.
