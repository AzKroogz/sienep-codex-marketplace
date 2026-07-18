# Enriquecer la guía de infraestructura SIENEP — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrar de forma curada los requisitos y devoluciones de SIENEP 2026 en la referencia de estudio de infraestructura.

**Architecture:** Mantener `SKILL.md` como flujo pedagógico y ampliar una única referencia de dominio para evitar rutas de carga adicionales. Tratar todo estado de la maqueta como histórico y exigir evidencia actual antes de afirmar operación.

**Tech Stack:** Markdown, manifiesto de plugin Codex, Git y GitHub CLI.

## Global Constraints

- No copiar configuraciones completas ni datos sensibles de los PDF.
- Diferenciar requisito obligatorio, recomendación y objetivo de nivel superior.
- Etiquetar las devoluciones y estados operativos como históricos.
- Priorizar evidencia operativa sobre mera presencia de configuración.

---

### Task 1: Escenarios de recuperación

**Files:**
- Create: `tests/infraestructura-guide-scenarios.md`
- Modify: none
- Test: revisión de respuestas de agentes contra la guía anterior y la actualizada

**Interfaces:**
- Consumes: requisitos y brechas definidos en el diseño aprobado.
- Produces: cinco consultas con criterios de éxito observables.

- [ ] **Step 1: Escribir escenarios antes de cambiar la referencia**

Incluir consultas sobre niveles 3–5, cuatro puntos de control, estado histórico, guion sin repeticiones y brechas finales.

- [ ] **Step 2: Ejecutar una consulta base con la guía anterior**

Registrar qué criterios nuevos no puede recuperar el agente con precisión.

- [ ] **Step 3: Confirmar el fallo esperado**

La línea base debe omitir al menos uno de estos elementos: matriz por nivel, cuatro puntos de control, Keepalived, Excel obligatorio para nivel 4 o configuración básica de appliances.

- [ ] **Step 4: Commit**

```bash
git add tests/infraestructura-guide-scenarios.md
git commit -m "test: add infrastructure guide retrieval scenarios"
```

### Task 2: Ampliar la referencia curada

**Files:**
- Modify: `plugins/sienep-defensa/skills/estudiar-infraestructura-sienep/references/guia-infraestructura.md`
- Test: `tests/infraestructura-guide-scenarios.md`

**Interfaces:**
- Consumes: escenarios de Task 1 y fuentes evaluadas en el diseño.
- Produces: secciones Markdown recuperables por tema y nivel.

- [ ] **Step 1: Incorporar alcance y entregables por nivel**

Agregar VLSM, DMZ, requisitos de niveles 3–5, documentación Excel y archivos `.txt` sin duplicar el núcleo tecnológico.

- [ ] **Step 2: Incorporar el protocolo de evidencia**

Agregar cuatro puntos de control, identificación de appliances, configuración básica, pruebas antes/durante/después y economía de demostraciones NAT.

- [ ] **Step 3: Incorporar disponibilidad de servidores y brechas históricas**

Agregar bonding/Keepalived, autenticación OSPF recomendada y matriz histórica de demostrado, observado con brechas y pendiente de evidencia actual.

- [ ] **Step 4: Ampliar preguntas docentes**

Agregar preguntas de justificación, interpretación y falla vinculadas al nuevo material.

- [ ] **Step 5: Ejecutar los escenarios y confirmar recuperación**

Cada respuesta debe incluir la clasificación normativa correcta, una prueba operativa y la advertencia histórica cuando corresponda.

- [ ] **Step 6: Commit**

```bash
git add plugins/sienep-defensa/skills/estudiar-infraestructura-sienep/references/guia-infraestructura.md
git commit -m "docs: enrich SIENEP infrastructure defense guide"
```

### Task 3: Validar y publicar

**Files:**
- Verify: `.codex-plugin/plugin.json`
- Verify: `plugins/sienep-defensa/skills/estudiar-infraestructura-sienep/SKILL.md`
- Verify: `plugins/sienep-defensa/skills/estudiar-infraestructura-sienep/references/guia-infraestructura.md`

**Interfaces:**
- Consumes: rama con guía y escenarios completos.
- Produces: pull request fusionado en `main`.

- [ ] **Step 1: Ejecutar validación estructural y de formato**

```bash
git diff --check origin/main...HEAD
python3 -m json.tool .codex-plugin/plugin.json
```

Resultado esperado: cero errores y JSON válido.

- [ ] **Step 2: Revisar el diff contra el diseño**

Confirmar ausencia de configuraciones completas, datos sensibles, afirmaciones actuales sin evidencia y duplicación innecesaria.

- [ ] **Step 3: Enviar la rama y abrir el pull request**

```bash
git push -u origin docs/enriquecer-guia-infraestructura
gh pr create --base main --head docs/enriquecer-guia-infraestructura
```

- [ ] **Step 4: Fusionar el pull request**

```bash
gh pr merge --squash --delete-branch
```

- [ ] **Step 5: Verificar el estado remoto**

```bash
gh pr view --json state,mergedAt,mergeCommit,url
```

Resultado esperado: estado `MERGED` y commit de fusión presente.
