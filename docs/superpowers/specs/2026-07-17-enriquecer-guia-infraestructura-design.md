# Diseño: enriquecer la guía de infraestructura SIENEP

## Objetivo

Incorporar a la habilidad de estudio la información útil de los documentos de requisitos y devoluciones del proyecto SIENEP 2026, manteniendo una referencia breve, pedagógica y segura frente a configuraciones históricas.

## Fuentes evaluadas

- `Detalle Infraestructura Proyecto de Semestre 3 - SIENEP 2026.pdf`: requisitos, niveles de evaluación, tecnologías, comandos, pruebas y entregables.
- `Contexto de devoluciones, configuraciones,verificaciones de infraestructura.pdf`: devoluciones de los sprints, fortalezas demostradas, brechas pendientes y configuraciones históricas de la maqueta.

Los volcados completos de configuración no se copiarán. Solo se conservarán patrones reutilizables y hechos necesarios para preparar la defensa. Todo estado operativo extraído de devoluciones o configuraciones se etiquetará como histórico y requerirá evidencia actual.

## Cambios de contenido

La referencia `guia-infraestructura.md` se ampliará con:

1. Una matriz compacta de alcance por niveles 3, 4 y 5.
2. Requisitos omitidos o poco desarrollados: VLSM, DMZ, modelos de appliances, configuración básica, cuatro puntos de control, tolerancia a fallos de servidores, autenticación OSPF, documentación Excel y archivos de configuración.
3. Un guion eficiente de demostración que evite repetir pruebas equivalentes y priorice evidencia operativa.
4. Una matriz de estado histórico: demostrado, observado con brechas y pendiente de verificar actualmente.
5. Preguntas docentes que exijan justificar decisiones, interpretar salidas y diseñar pruebas de falla.

## Límites

- No reproducir configuraciones completas ni datos sensibles.
- No afirmar que una función continúa operativa solo porque aparece configurada en los PDF.
- No convertir recomendaciones opcionales en requisitos obligatorios.
- No duplicar explicaciones ya presentes; ampliar únicamente donde las fuentes aportan precisión.
- Mantener `SKILL.md` enfocado en el método de enseñanza y concentrar el dominio en la referencia.

## Validación

La actualización se verificará con escenarios de consulta que comprueben que un tutor pueda:

- distinguir requisitos obligatorios, opcionales y de nivel superior;
- proponer evidencia operativa y no solo comandos de configuración;
- señalar el carácter histórico de las devoluciones;
- construir un guion de defensa sin demostraciones repetitivas;
- recuperar brechas concretas como STP, IPv6, HSRP, Keepalived y Excel.

También se ejecutarán comprobaciones estructurales del manifiesto y de los archivos de la habilidad antes de publicar la rama.

## Publicación

El cambio se realizará en `docs/enriquecer-guia-infraestructura`, se enviará al remoto, se abrirá un merge request o pull request contra `main` y se fusionará una vez que las validaciones sean satisfactorias.
