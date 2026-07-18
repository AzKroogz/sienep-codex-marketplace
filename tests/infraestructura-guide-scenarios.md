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
- clasifica VLSM como requisito general obligatorio, una zona DMZ como requisito
  obligatorio de la topología y la autenticación OSPF como opcional/recomendada;
- identifica Excel como documentación obligatoria para nivel 4 y menciona los
  archivos de configuración requeridos;
- propone al menos una evidencia operativa, además del entregable documental,
  e identifica explícitamente como flujo denegado el acceso no autorizado desde
  la DMZ hacia la LAN interna.

## Escenario 2: cuatro puntos de control y appliances

**Consulta:** Prepará el control inicial de la maqueta. Explicá los cuatro
puntos de control, cómo identificar los modelos de appliances y qué
configuración básica debe comprobarse antes de evaluar las funciones de red.

**Criterios de éxito:**

- enumera y nombra los cuatro puntos de control del recorrido: origen (tráfico
  emitido por el cliente), gateway de origen (entrada y decisión de
  routing/política), borde o tránsito (salida y, si corresponde, traducción NAT)
  y destino (tráfico recibido o rechazo esperado);
- exige identificar el modelo o imagen de cada appliance relevante;
- comprueba como configuración básica concreta `hostname`, banner legal,
  contraseña de consola, contraseña o autenticación de VTY y `enable secret`;
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

**Consulta:** Identificá los requisitos, entregables, recomendaciones y brechas
históricas que pueden afectar la defensa y armá un plan de cierre priorizado.
Incluí STP, IPv6, HSRP, Keepalived, Excel y configuración básica de appliances.

**Criterios de éxito:**

- clasifica STP como requisito de nivel 3 con una brecha histórica en su prueba
  de reconvergencia, e IPv6 como requisito general con evidencia histórica
  pendiente;
- clasifica HSRP como capacidad implementada históricamente pero pendiente de
  evidencia final, y Keepalived como recomendación de disponibilidad de
  servidores con brecha histórica en la demostración de failover;
- clasifica Excel como entregable obligatorio de nivel 4 y la configuración
  básica de appliances como brecha histórica de demostración que debe cubrir
  `hostname`, banner, consola, VTY y `enable secret`;
- no presenta el inventario ni la comprobación básica de appliances como
  requisitos normativos de la pauta;
- asigna a cada elemento una evidencia verificable y un resultado esperado sin
  presentar como actual un dato histórico;
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

## Resultado GREEN contra la guía ampliada

Fecha de ejecución: 2026-07-17. Se conservaron las consultas y se contrastaron
exclusivamente con la guía ampliada.

| Escenario | Recuperación confirmada | Resultado |
|---|---|---|
| 1. Niveles 3–5 | Matriz y clasificación normativa; VLSM, DMZ, OSPF, Excel/`.txt`, evidencia operativa y denegación DMZ hacia LAN interna. | GREEN |
| 2. Puntos de control | Cuatro controles, modelo/imagen, cinco comprobaciones básicas y distinción entre configuración, operación y evidencia actual. | GREEN |
| 3. Estado histórico | Tres estados históricos, cautela de vigencia, HSRP frente a bonding/Keepalived y prueba de falla. | GREEN |
| 4. Guion eficiente | Antes/durante/después, reutilización trazable, economía NAT, restauración y recuperación. | GREEN |
| 5. Brechas finales | Clasificaciones y evidencias para STP, IPv6, HSRP, Keepalived, Excel y appliances; el control de appliances queda explícitamente no normativo. | GREEN |

**Confirmación GREEN:** los cinco escenarios recuperan todos sus criterios sin
convertir recomendaciones o controles preparatorios en requisitos obligatorios
ni presentar observaciones históricas como estado actual.
