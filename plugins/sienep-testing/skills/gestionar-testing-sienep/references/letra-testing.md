# Letra del área de Testing (UTEC – LTI – PFT SIENEP 2026)

Resumen del documento "UTEC-2026-S4-PFT-TESTING". Ante dudas, manda el PDF original.

Herramientas obligatorias: **TestLink** (diseño y ejecución) y **Mantis** (defectos).

## Artefactos

### Plan de Pruebas (PDF)
Apartados mínimos:
1. Alcance del documento.
2. Requerimientos involucrados.
3. Alcance de las pruebas.
4. Equipo de testing y roles.
5. Tipos de pruebas planificadas, cada uno detallado.
6. Ambientes de prueba y proceso de actualización.
7. Ciclo de vida de pruebas.
8. Ciclo de vida de defectos.
9. Cronograma detallado.
10. Métricas, con la justificación de su selección.
11. Identificación y ponderación de riesgos.
12. Herramientas.
13. Conclusiones.
14. Referencias bibliográficas.

Anexos sugeridos: informes de Mantis, reportes de TestLink, minutas, mitigación de riesgos.

### Casos de prueba (en TestLink)
- Diseño con **técnicas de diseño de casos** y casos de **usabilidad** (según lo visto en UX).
- Suite para la **aplicación web**.
- Suite para la **base de datos corporativa**.
- Suite para los **servicios del sistema**, con **al menos 2 assertions** en las suites y las ejecuciones.
- Ejecución:
  - Probar las funcionalidades desarrolladas.
  - Retest con fix y regresión.
  - Una ejecución completa sobre la versión final.
- Cantidades mínimas: **3 ejecuciones de funcionalidades** y **2 ejecuciones completas**.
- Cada **build** tiene que indicar su tipo: Funcionalidades / Regresión / Retest con Fix / Ejecución Completa.

### Defectos (en Mantis)
- Mínimo **20 defectos**, siguiendo el ciclo de vida del Plan de Pruebas.
- Las mejoras o funcionalidades deseables **no** cuentan.
- Si no se llega a 20, se justifica en el Informe de Resultados.

### Informe de Resultados (PDF)
- Cálculo de las métricas del Plan.
- Actividades realizadas y análisis de desvíos respecto al Plan.
- Conclusión sobre la calidad del producto.
- Anexos: reportes de Mantis y TestLink.

### Planilla de Riesgos
- La planilla y su seguimiento: evolución, cambios en cada etapa y acciones tomadas.

## Formato de entrega
- El Plan y el Informe van en PDF, con sus anexos también en PDF.
- Suites, casos y defectos se entregan **en las herramientas**, con los archivos en el formato que exporta cada una.
- Carpeta de los PDF: `Testing_<nombre_doc>_<n°_entrega>_<nombre_equipo>`.
