# Defensa Real SIENEP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Incorporar a los tres skills del plugin el patrón conceptual, oral y basado en repreguntas observado en una defensa real.

**Architecture:** Una referencia transversal anonimizada concentra los patrones derivados del video. Cada `SKILL.md` conserva su dominio y añade un contrato pedagógico adaptado; un validador estructural y escenarios versionados protegen el comportamiento común.

**Tech Stack:** Markdown, YAML/JSON del plugin, Python 3 para regresiones estructurales y CLI de Codex para validación/instalación.

## Global Constraints

- Enseñar conceptos antes de comandos, código o demostraciones.
- Usar `respuesta directa → concepto → decisión SIENEP → evidencia → límite`.
- Profesor y Simulacro formulan exactamente una pregunta por turno.
- Distinguir implementado y demostrado, implementado sin evidencia, propuesto y no documentado.
- Gestión de Riesgos conserva aproximadamente 80 % comprensión conceptual y 20 % aplicación.
- No incorporar el video ni su transcripción al repositorio.
- No mezclar hechos de Infraestructura, Programación y Gestión de Riesgos.

---

### Task 1: Escenarios RED transversales

**Files:**
- Create: `tests/defensa-real-scenarios.md`
- Create: `tests/validate_defensa_real_skills.py`

**Interfaces:**
- Consumes: los tres `SKILL.md` existentes.
- Produces: validación estructural ejecutable con Python y escenarios manuales congelados.

- [ ] **Step 1: Escribir escenarios fallidos**

Crear ocho escenarios: máscaras antes de comandos, RAID implementado/propuesto, validación negativa de API, endpoint afirmado/demostrado, inundación y producto, ISP/failover, respuesta breve y contribución/FODA.

- [ ] **Step 2: Escribir el validador estructural**

Comprobar en los tres skills los términos `respuesta directa`, `concepto`, `decisión`, `evidencia`, `límite`, `30–60 segundos`, `una pregunta por turno`, las cuatro categorías de estado de evidencia y el enlace a la referencia transversal. Añadir controles específicos por dominio.

- [ ] **Step 3: Ejecutar RED**

Run: `python3 tests/validate_defensa_real_skills.py`

Expected: `AssertionError` indicando que falta el contrato de defensa real.

- [ ] **Step 4: Commit RED**

```bash
git add tests/defensa-real-scenarios.md tests/validate_defensa_real_skills.py
git commit -m "test: definir entrenamiento desde defensa real"
```

### Task 2: Referencia pedagógica compartida

**Files:**
- Create: `plugins/sienep-defensa/references/patrones-defensa-real.md`

**Interfaces:**
- Consumes: análisis local del video, sin copiar transcripción ni identidades.
- Produces: patrones conceptuales, preguntas por materia y contrato oral enlazable por los tres skills.

- [ ] **Step 1: Escribir la referencia mínima**

Incluir jerarquía de fuentes, secuencia oral, repreguntas, evidencia secundaria, control de tiempo, errores observados y bancos conceptuales separados para Infraestructura, Programación y Riesgos.

- [ ] **Step 2: Confirmar privacidad y alcance**

Run: `rg -n 'NativosTec|\.mkv|Transcripcion_Defensa' plugins/sienep-defensa/references/patrones-defensa-real.md`

Expected: sin coincidencias.

### Task 3: Integración GREEN en los tres skills

**Files:**
- Modify: `plugins/sienep-defensa/skills/estudiar-infraestructura-sienep/SKILL.md`
- Modify: `plugins/sienep-defensa/skills/estudiar-programacion-sienep/SKILL.md`
- Modify: `plugins/sienep-defensa/skills/estudiar-gestion-riesgos-sienep/SKILL.md`
- Test: `tests/validate_defensa_real_skills.py`

**Interfaces:**
- Consumes: `../../references/patrones-defensa-real.md` desde cada carpeta de skill.
- Produces: conducta conceptual consistente con especialización por materia.

- [ ] **Step 1: Actualizar Infraestructura**

Priorizar problema, funcionamiento y criterio SIENEP; dejar comandos y configuración como evidencia posterior; incorporar preguntas conceptuales derivadas.

- [ ] **Step 2: Actualizar Programación**

Priorizar concepto y regla de negocio; usar Swagger/código/pruebas negativas como evidencia; distinguir funcionalidad real de propuesta.

- [ ] **Step 3: Actualizar Gestión de Riesgos**

Aplicar proporción 80/20, clasificación por causa/origen y separación entre causa externa y mitigación técnica.

- [ ] **Step 4: Ejecutar GREEN**

Run: `python3 tests/validate_defensa_real_skills.py`

Expected: `OK: los tres skills incorporan el patrón conceptual de defensa real`.

- [ ] **Step 5: Ejecutar regresiones existentes**

Run: `python3 tests/validate_gestion_riesgos_skill.py`

Expected: `OK: estructura pedagógica, fuente nueva, GREEN durable y manifiesto`.

- [ ] **Step 6: Commit GREEN**

```bash
git add plugins/sienep-defensa tests
git commit -m "feat: educar los skills desde una defensa real"
```

### Task 4: Validación, cachebuster e integración

**Files:**
- Modify: `plugins/sienep-defensa/.codex-plugin/plugin.json`

**Interfaces:**
- Consumes: plugin validado en la rama.
- Produces: versión reinstalable, PR fusionada y `main` alineada.

- [ ] **Step 1: Validar los tres skills**

```bash
python3 /home/nicolas/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/sienep-defensa/skills/estudiar-infraestructura-sienep
python3 /home/nicolas/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/sienep-defensa/skills/estudiar-programacion-sienep
python3 /home/nicolas/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/sienep-defensa/skills/estudiar-gestion-riesgos-sienep
```

Expected: `Skill is valid!` en los tres casos.

- [ ] **Step 2: Actualizar cachebuster**

Run: `python3 /home/nicolas/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py plugins/sienep-defensa`

Expected: manifiesto actualizado.

- [ ] **Step 3: Validar plugin y diff**

```bash
python3 /home/nicolas/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/sienep-defensa
python3 tests/validate_defensa_real_skills.py
python3 tests/validate_gestion_riesgos_skill.py
git diff --check main...HEAD
```

Expected: todas las validaciones con exit code 0.

- [ ] **Step 4: Commit de integración**

```bash
git add plugins/sienep-defensa/.codex-plugin/plugin.json
git commit -m "chore: actualizar versión del plugin"
```

- [ ] **Step 5: Publicar e integrar**

Subir `feat/educar-riesgos-desde-defensa-real`, crear PR, fusionarla a `main`, actualizar el repositorio local y reinstalar `sienep-defensa@sienep-equipo`.

- [ ] **Step 6: Verificación posterior al merge**

Confirmar `HEAD == origin/main`, plugin instalado/habilitado, validadores en verde y coincidencia entre la fuente fusionada y el skill instalado.
