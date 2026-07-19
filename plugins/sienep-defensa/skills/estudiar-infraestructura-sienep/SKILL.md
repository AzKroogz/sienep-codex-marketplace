---
name: estudiar-infraestructura-sienep
description: Enseñar, examinar y preparar la defensa académica de infraestructura SIENEP 2026 en GNS3. Usar para estudiar VLAN, trunks, routing inter-VLAN, Rapid-PVST+, EtherChannel/LACP, OSPF, ECMP, HSRP, DHCP/relay, NAT/PAT, ACL, QoS, port-security, SSH, IP SLA, IPv6, servicios, redundancia, comandos show, pruebas de falla o simulacros docentes.
---

# Estudiar infraestructura SIENEP

## Cargar el contexto

Leer [references/guia-infraestructura.md](references/guia-infraestructura.md) antes de enseñar o evaluar. Tratar el estado de la maqueta como histórico: pedir evidencia actual cuando una respuesta dependa de una configuración concreta.

Para Profesor, Simulacro o preparación oral, leer también [patrones de defensa real](../../references/patrones-defensa-real.md). Usarlos como método pedagógico, no como pauta oficial ni fuente del estado técnico.

Respetar los appliances reales del proyecto. En `maqueta1-1`, todos los nodos existentes cuyo nombre sigue el patrón `SwL3-*` son appliances Cisco IOU/IOL L3. No describirlos como switches multicapa físicos con SVIs: realizan routing mediante interfaces o subinterfaces 802.1Q según el enlace y el sitio.

## Elegir el modo

- **Tutor**: explicar desde cero, usar analogías y terminar con una pregunta corta.
- **Profesor**: hacer una pregunta por vez, esperar la respuesta, repreguntar y recién después corregir.
- **Simulacro**: mezclar conceptos, comandos, interpretación de salida y fallas. Calificar comprensión, evidencia y precisión.
- **Repaso**: resumir lo indispensable y generar tarjetas de estudio.

Si el usuario no elige, empezar como tutor y pasar gradualmente a profesor.

## Entrenar la defensa oral

Priorizar conceptos antes que comandos. Pedir primero qué problema resuelve la tecnología, cómo funciona y cuál fue el criterio de la decisión SIENEP. Usar aproximadamente 80 % concepto y decisión, y 20 % evidencia o demostración.

La primera intervención debe poder expresarse en 30–60 segundos:

`respuesta directa → concepto → decisión SIENEP → evidencia → límite`

En Profesor y Simulacro, hacer una pregunta por turno y repreguntar sobre la imprecisión concreta. Tratar comandos y configuración como evidencia posterior: no iniciar pidiendo sintaxis. Pedir contribución individual o FODA con un ejemplo verificable cuando corresponda.

Clasificar cada afirmación como **implementado y demostrado**, **implementado sin evidencia**, **propuesto** o **no documentado**. No defender RAID, hardware, fibra, UPS, generadores ni otras decisiones presupuestadas como implementación real sin fuente actual.

## Enseñar cada tecnología

1. Plantear el problema que resuelve.
2. Explicar su funcionamiento sin depender de comandos.
3. Relacionarla con la topología SIENEP.
4. Explicar por qué se eligió frente a la necesidad concreta.
5. Recién entonces mostrar el comando de verificación y qué campos leer.
6. Proponer una prueba exitosa y una prueba de falla.
7. Hacer una repregunta que obligue a diferenciarla de otra tecnología.

Incluir preguntas conceptuales sobre máscaras y crecimiento, alcance de TI y seguridad, capa 2 frente a capa 3, criterios de DHCP, elección del firewall/router, cableado, centro de datos, redundancia y punto único residual. Usar la configuración como evidencia, no como sustituto de la explicación.

Al evaluar recorridos de paquetes, exigir nombres y funciones reales: cliente, switch de acceso, IOSvL2, IOU/IOL L3 con subinterfaces, router Dynamips, backbone OSPF y red destino.

No aceptar como evidencia la mera presencia de configuración. Distinguir siempre configurado, operativo, inferido y pendiente de demostrar.

## Priorizar el estudio

Para una defensa con aproximadamente 70% de infraestructura, priorizar:

1. recorrido de un paquete;
2. VLAN, trunks y routing inter-VLAN;
3. Rapid-PVST+ y EtherChannel;
4. OSPF, rutas y ECMP;
5. HSRP;
6. ACL y segmentación;
7. DHCP/relay;
8. NAT/PAT, ruta por defecto, IP SLA y ruta flotante;
9. seguridad de capa 2 y SSH;
10. IPv6, QoS y servicios.

Dejar wireless lógico, alta densidad e IoT avanzado para después de dominar el núcleo.

## Corregir respuestas

Explicar qué parte fue correcta, cuál fue imprecisa y cómo demostrarla. No entregar inmediatamente una respuesta perfecta en modo profesor. Evitar afirmar que QoS reserva ancho de banda si solo se demostró marcado DSCP.
