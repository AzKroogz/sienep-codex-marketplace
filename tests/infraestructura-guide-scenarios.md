# Escenarios de recuperación de la guía de infraestructura

Estos escenarios evalúan respuestas generadas usando únicamente
`plugins/sienep-defensa/skills/estudiar-infraestructura-sienep/references/guia-infraestructura.md`.
Un criterio se considera recuperado solo si la respuesta puede sostenerlo con la
guía, sin inventar datos ni convertir recomendaciones en requisitos.

## Escenario 1: alcance por niveles 3, 4 y 5

**Consulta:** Compará los requisitos de infraestructura para alcanzar los
niveles 3, 4 y 5. Indicá qué es obligatorio en cada nivel, qué es recomendado y
qué evidencia o entregable debe presentarse.

**Criterios de éxito:**

- presenta una matriz o comparación inequívoca por nivel;
- clasifica VLSM, DMZ y autenticación OSPF sin confundir obligación,
  recomendación y objetivo de nivel superior;
- identifica Excel como documentación obligatoria para nivel 4 y menciona los
  archivos de configuración requeridos;
- propone al menos una evidencia operativa, además del entregable documental.

## Escenario 2: cuatro puntos de control y appliances

**Consulta:** Prepará el control inicial de la maqueta. Explicá los cuatro
puntos de control, cómo identificar los modelos de appliances y qué
configuración básica debe comprobarse antes de evaluar las funciones de red.

**Criterios de éxito:**

- enumera los cuatro puntos de control con su propósito observable;
- exige identificar el modelo o imagen de cada appliance relevante;
- recupera la configuración básica que debe revisarse;
- distingue presencia de configuración, estado operativo y evidencia actual.

## Escenario 3: estado histórico y disponibilidad

**Consulta:** Resumí qué capacidades de la maqueta fueron demostradas, cuáles
se observaron con brechas y cuáles siguen pendientes de verificación. Incluí
HSRP, STP, IPv6 y disponibilidad de servidores con bonding y Keepalived.

**Criterios de éxito:**

- separa demostrado, observado con brechas y pendiente de verificar;
- etiqueta el estado como histórico y pide evidencia actual antes de afirmar
  que una capacidad continúa operativa;
- diferencia la redundancia de gateway de HSRP de la disponibilidad de servidor
  mediante bonding y Keepalived;
- incluye una prueba operativa o de falla para la afirmación principal.

## Escenario 4: guion de defensa sin repeticiones

**Consulta:** Diseñá un guion breve para demostrar la infraestructura en la
defensa. Cubrí estado, conectividad, políticas y recuperación ante fallas sin
repetir pruebas equivalentes, especialmente las de NAT.

**Criterios de éxito:**

- ordena evidencia antes, durante y después de una prueba de falla;
- reutiliza una prueba cuando permite demostrar más de un criterio sin perder
  trazabilidad;
- evita repetir traducciones NAT equivalentes y explica qué demuestra cada
  salida elegida;
- restaura el estado y verifica la recuperación al cerrar la demostración.

## Escenario 5: brechas finales y plan de cierre

**Consulta:** Identificá las brechas finales que pueden afectar la defensa y
armá un plan de cierre priorizado. Incluí STP, IPv6, HSRP, Keepalived, Excel y
configuración básica de appliances.

**Criterios de éxito:**

- recupera las seis brechas solicitadas sin presentar como actual un dato
  histórico;
- asigna a cada brecha una evidencia verificable y un resultado esperado;
- diferencia requisitos de nivel, recomendaciones y pendientes técnicos;
- prioriza por impacto en evaluación y dependencia para la demostración.

## Línea base contra la guía anterior

Fecha de ejecución: 2026-07-17.

Método: se respondió cada consulta usando exclusivamente la guía anterior y se
contrastó la respuesta recuperable con los criterios anteriores. No se usaron
los PDF fuente ni conocimiento externo para completar ausencias.

| Escenario | Respuesta recuperable de la guía anterior | Criterios nuevos no recuperables con precisión | Resultado |
|---|---|---|---|
| 1. Niveles 3–5 | Permite describir el núcleo obligatorio y algunas evidencias generales. | No define una matriz por nivel, VLSM, DMZ, autenticación OSPF, Excel obligatorio para nivel 4 ni archivos de configuración. | Falla |
| 2. Puntos de control | Aporta comandos de verificación y una secuencia general de evidencia. | No enumera cuatro puntos de control, modelos de appliances ni su configuración básica. | Falla |
| 3. Estado histórico | Advierte que ciertos riesgos son históricos y menciona HSRP, STP e IPv6 de forma conceptual. | No clasifica capacidades por estado ni explica bonding o Keepalived para disponibilidad de servidores. | Falla |
| 4. Guion eficiente | Ofrece una secuencia de siete pasos para una demostración y exige restaurar y verificar. | No propone economía de demostraciones ni evita explícitamente repeticiones equivalentes de NAT. | Falla |
| 5. Brechas finales | Enumera algunos riesgos históricos y pendientes generales. | No recupera como conjunto STP, IPv6, HSRP, Keepalived, Excel y configuración básica de appliances, ni los vincula con nivel y plan de cierre. | Falla |

**Confirmación RED:** los cinco escenarios fallan al menos un criterio. La línea
base omite todos los indicadores mínimos señalados por el plan: matriz por
nivel, cuatro puntos de control, Keepalived, Excel obligatorio para nivel 4 y
configuración básica de appliances.
