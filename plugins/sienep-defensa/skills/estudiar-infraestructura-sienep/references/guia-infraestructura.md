# Guía de infraestructura SIENEP

## Índice

1. Escenario
2. Núcleo obligatorio
3. Seguridad y servicios
4. Evidencias
5. Preguntas docentes
6. Riesgos históricos
7. Banco ampliado de preguntas
8. Plan de cierre

## Escenario

El campus SIENEP se representa con cinco sitios interconectados:

- A: administración, Data Center y POP;
- B: laboratorios de TI;
- C: aulas y biblioteca;
- D: cowork/BYOD;
- E: anfiteatro, eventos e IoT.

La defensa debe justificar disponibilidad, seguridad, segmentación y escalabilidad. El archivo portable de GNS3 y el video son excluyentes según la pauta resumida por el equipo.

### Alcance normativo y entregables

No confundir tres categorías: **obligatorio** es un requisito de la pauta;
**recomendado** mejora la solución pero no debe presentarse como requisito; y
**meta de nivel** indica qué debe integrarse para aspirar a esa calificación. Los
niveles son acumulativos: un nivel superior conserva los requisitos de los
anteriores.

| Alcance | Obligatorio o meta acumulativa | Entregable y evidencia operativa |
|---|---|---|
| General | Diseñar el direccionamiento con VLSM, incorporar IPv6 y separar los servicios expuestos en una zona DMZ de la LAN interna. La DMZ es requisito de topología, no una recomendación. | Tabla de subredes coherente con la maqueta; `show ip route`, `show ipv6 route` y una prueba de acceso permitido a DMZ junto con un intento interno denegado. |
| Nivel 3 | Demostrar el núcleo de VLAN/trunks, routing, seguridad y servicios; Rapid-PVST+ (STP) es requisito de este nivel. | Estado de VLAN/trunks/STP y conectividad o rechazo esperado; incluir una falla de enlace y observar reconvergencia. |
| Nivel 4 | Integrar y documentar el alcance previo. La documentación en Excel es obligatoria para este nivel. | Libro Excel con inventario, direccionamiento/VLSM, VLAN, enlaces y plan de pruebas; además, archivos `.txt` de configuración de los equipos requeridos, saneados y trazables al appliance. La documentación no sustituye las pruebas en vivo. |
| Nivel 5 | Defender de forma integrada disponibilidad, políticas, servicios y recuperación, justificando decisiones y verificando el comportamiento ante fallas. | Guion reproducible con estado antes/durante/después, resultados esperados, recuperación comprobada y los entregables acumulados. |

La autenticación de vecinos OSPF es **opcional/recomendada** como
endurecimiento; si se adopta, hay que demostrar vecindad válida y rechazo o
pérdida de adyacencia ante credenciales incompatibles sin revelar secretos.

## Núcleo obligatorio

### Appliances reales y sitio C

No deducir la función únicamente por el nombre mostrado en GNS3. Inventario histórico verificado:

- Todos los nodos existentes llamados `SwL3-*` en `maqueta1-1` son appliances Cisco IOU/IOL L3 (`node_type: iou`). Esto incluye los equipos de distribución/routing de los distintos sitios, aunque su nombre empiece por `Sw`.
- `SwL3-5`: appliance Cisco IOU/IOL de capa 3 (`node_type: iou`), no IOSvL2 ni un switch multicapa físico.
- `Switch-C-L2`: appliance QEMU con imagen IOSvL2.
- `SwAcc-C-1`: appliance IOU/IOL usado como acceso.
- `R-C`: router Cisco 3725 ejecutado por Dynamips.

Camino real del estudiante del sitio C:

```text
PC-C-Estudiantes
-> SwAcc-C-1
-> Switch-C-L2
-> SwL3-5 (IOU/IOL L3, router-on-a-stick)
-> R-C (Cisco 3725)
-> backbone OSPF
-> sitio A
-> red/DMZ del servidor SIENEP
```

`SwL3-5` recibe un trunk hacia el entorno de acceso y usa subinterfaces 802.1Q como gateways, por ejemplo la lógica:

```text
Ethernet0/1.20 -> VLAN Docentes
Ethernet0/1.30 -> VLAN Estudiantes
Ethernet0/1.60 -> VLAN Guest
Ethernet0/1.90 -> VLAN Gestión
```

La subinterfaz tiene `encapsulation dot1Q <vlan>` y una IP de la subred. Eso constituye router-on-a-stick. No describir este sitio como routing mediante SVI salvo evidencia distinta en la configuración actual.

### Recorrido de un paquete

```text
Host -> puerto access -> VLAN -> trunk -> SVI/gateway
-> ACL -> routing OSPF -> backbone -> red destino
```

Para el sitio C, sustituir `SVI/gateway` por `subinterfaz 802.1Q/gateway en SwL3-5`.

Hacia Internet:

```text
Host -> gateway -> ruta por defecto -> borde -> NAT/PAT -> ISP
```

### VLAN y routing inter-VLAN

- Una VLAN separa dominios de broadcast.
- Un access transporta una VLAN; un trunk transporta varias con 802.1Q.
- Una VLAN nativa segura y no utilizada reduce riesgos de tráfico sin etiqueta.
- El routing inter-VLAN puede hacerse mediante SVI o subinterfaces. En el sitio C auditado se hace mediante router-on-a-stick sobre el appliance IOU/IOL L3 `SwL3-5`.

Comandos: `show vlan brief`, `show interfaces trunk`, `show interfaces switchport`, `show ip interface brief`.

### Rapid-PVST+

- Evita loops de capa 2.
- Elige root bridge por prioridad y MAC.
- Mantiene caminos alternativos bloqueados y reconverge ante fallas.
- PortFast acelera puertos de usuario; BPDU Guard los protege de switches inesperados.

Comandos: `show spanning-tree`, `show spanning-tree vlan 10`, `show spanning-tree summary`.

### EtherChannel/LACP

- Agrupa enlaces físicos como un Port-Channel lógico.
- Aporta capacidad y tolerancia al fallo de un miembro.
- LACP negocia el canal; el balanceo usa hash.

Comandos: `show etherchannel summary`, `show interfaces port-channel`, `show interfaces trunk`.

### OSPF y ECMP

- OSPF es link-state y calcula rutas con SPF/Dijkstra.
- Área 0 funciona como backbone.
- Router ID identifica al router; interfaces pasivas anuncian LAN sin formar vecinos.
- ECMP instala caminos de igual costo.
- Ante una falla, OSPF actualiza la topología y recalcula rutas.

Comandos: `show ip ospf neighbor`, `show ip protocols`, `show ip route`, `traceroute`.

### HSRP

- Proporciona gateway virtual redundante.
- Un equipo queda active y otro standby.
- `priority` influye en la elección; `preempt` permite recuperar el rol.
- OSPF protege rutas entre routers; HSRP protege el gateway visto por los hosts.

Comando: `show standby brief`.

### DHCP y relay

DORA significa Discover, Offer, Request y Acknowledge. Los broadcasts no cruzan routers; `ip helper-address` reenvía la solicitud hacia el servidor central.

Comandos: `show ip dhcp binding`, `show ip dhcp pool`; en cliente, `ipconfig /all`.

### NAT/PAT

NAT traduce direcciones. PAT permite compartir una dirección usando puertos. Explicar inside local, inside global, ACL de redes traducibles y ruta por defecto.

Comandos: `show ip nat translations`, `show ip nat statistics`, `show ip route`.

### Redundancia

| Tecnología | Protege frente a |
|---|---|
| Rapid-PVST+ | fallo/camino alternativo de capa 2 |
| EtherChannel | fallo de un miembro del canal |
| OSPF | fallo de ruta o enlace de capa 3 |
| ECMP | disponibilidad de caminos de igual costo |
| HSRP | fallo del gateway |
| IP SLA + tracking | pérdida de alcance hacia Internet |
| Ruta flotante | necesidad de un camino de respaldo |

### Disponibilidad de servidores

La redundancia de gateway y la de servidor resuelven fallas distintas. HSRP
mantiene un gateway virtual para los hosts; no mantiene disponible una
aplicación. En servidores, **bonding** agrupa interfaces para tolerar la caída de
un enlace y **Keepalived** puede mover una IP virtual entre nodos. Bonding y
Keepalived son una recomendación de disponibilidad, no un requisito general.
Para sostener la afirmación hay que cortar el enlace o detener el nodo activo,
observar la IP/rol y el servicio desde un cliente, y luego restaurar y comprobar
la recuperación.

## Seguridad y servicios

### ACL

- Evaluación de arriba hacia abajo y primera coincidencia.
- `deny any` implícito al final.
- ACL extendida cerca del origen cuando sea práctico.
- Diferenciar `in` y `out` desde la perspectiva de la interfaz.

Políticas esperadas:

- Guest: Internet permitido, LAN interna denegada.
- Estudiantes: acceso limitado a servidores críticos.
- Administración: acceso autorizado al Data Center.
- IoT: solo servidor IoT; sin acceso libre a ADMIN.
- SSH: permitido desde MGMT y bloqueado desde Guest.

Comandos: `show access-lists`, `show ip interface`, `ping`, `traceroute`.

### Seguridad de capa 2

Port-security limita MAC; `restrict` descarta y contabiliza, `shutdown` pone el puerto en err-disabled. Deshabilitar DTP en trunks, puertos sin uso y usar VLAN aislada.

### SSH

Explicar hostname, dominio, claves, usuario local, VTY, ACL de origen y por qué Telnet no protege credenciales.

### QoS

Separar clasificación, marcado DSCP, colas, policing y shaping. QoS no crea ancho de banda. Marcar AF31/AF21 no demuestra por sí solo prioridad efectiva.

Comando: `show policy-map interface`; generar tráfico coincidente y leer contadores.

### IPv6

Explicar direcciones globales y link-local, Neighbor Discovery, ausencia de broadcast y dual stack. Comandos: `show ipv6 interface brief`, `show ipv6 route`.

## Evidencias

### Control inicial de la maqueta

Registrar el modelo o la imagen y la función de cada appliance relevante; no
inferir capacidades solo por el ícono o por una configuración guardada. En cada
router o switch comprobar la presencia de `hostname`, banner legal, contraseña
de consola, contraseña o autenticación de VTY y `enable secret`, sin exhibir
credenciales. Separar siempre:

- **presencia de configuración**: aparece en la configuración saneada;
- **estado operativo**: la interfaz, vecindad, rol o servicio está activo;
- **evidencia actual**: una salida y una prueba tomadas en la sesión vigente.

Para una prueba extremo a extremo, seguir cuatro puntos de control:

1. **Origen:** confirmar el tráfico emitido por el cliente y sus parámetros.
2. **Gateway de origen:** comprobar la entrada y la decisión de routing o política.
3. **Borde o tránsito:** comprobar la salida y, cuando corresponda, la traducción NAT.
4. **Destino:** confirmar tráfico recibido o el rechazo esperado.

Para cada demostración usar esta secuencia:

1. mostrar estado inicial;
2. formular resultado esperado;
3. ejecutar la prueba;
4. leer la salida relevante;
5. provocar la falla si corresponde;
6. comprobar convergencia;
7. restaurar y verificar.

Una prueba puede cubrir varios criterios si se declara qué evidencia corresponde
a cada uno y se conserva trazabilidad. Para NAT, elegir una traducción
representativa: estado/ruta antes, tráfico que cree la entrada, traducción y
contadores durante, y limpieza o recuperación después. No repetir pings ni
traducciones equivalentes si no prueban una política, protocolo o camino
distinto.

Pruebas fuertes: ping permitido/bloqueado, DHCP remoto, traducción NAT, vecino OSPF, failover HSRP, miembro LACP caído, enlace del anillo caído, SSH desde MGMT y denegación desde Guest.

## Preguntas docentes

1. ¿Cómo viaja un paquete desde C hasta el servidor SIENEP en A?
2. ¿Por qué una VLAN necesita gateway para hablar con otra?
3. ¿Por qué tener redundancia si STP bloquea un enlace?
4. ¿Qué diferencia hay entre EtherChannel y STP?
5. ¿Por qué OSPF y no solo rutas estáticas?
6. ¿Para qué HSRP si ya existe OSPF?
7. ¿Qué ocurre con una ACL mal ordenada?
8. ¿Por qué DHCP necesita relay?
9. ¿Cómo comparten Internet muchos hosts con una IP?
10. ¿Qué demuestra un contador QoS en cero?
11. ¿Por qué VLSM y una DMZ son decisiones distintas aunque ambas afecten el diseño IP?
12. ¿Qué salida permite distinguir una configuración OSPF presente de una adyacencia operativa?
13. ¿Cómo demostraría la reconvergencia de STP sin confundirla con el failover del gateway HSRP?
14. ¿Qué falla cubre bonding y cuál Keepalived? Diseñe una prueba antes/durante/después.
15. ¿Qué observa en cada uno de los cuatro puntos de control cuando una ACL bloquea el flujo?
16. ¿Qué evidencia mínima conservaría en Excel y en los `.txt`, y cuál todavía debe mostrarse en vivo?
17. ¿Cómo elegir una única prueba NAT que sea económica pero mantenga trazabilidad?

## Banco ampliado de preguntas

### Appliances y topología

1. ¿Qué tipo de appliance son todos los nodos `SwL3-*` de `maqueta1-1`?
2. ¿Por qué el nombre `SwL3-5` no alcanza para afirmar que usa SVIs?
3. ¿Qué diferencia hay entre `node_type: iou`, QEMU IOSvL2 y Dynamips Cisco 3725?
4. Ordená el camino real desde `PC-C-Estudiantes` hasta `R-C`.
5. ¿Qué función cumple `Switch-C-L2` y qué función cumple `SwL3-5`?
6. ¿Dónde termina el dominio de capa 2 del estudiante?

### Router-on-a-stick y 802.1Q

7. ¿Qué problema resuelve una subinterfaz por VLAN?
8. ¿Qué hace `encapsulation dot1Q 30`?
9. ¿La subinterfaz tiene una MAC distinta o reutiliza la interfaz física según la plataforma?
10. ¿Por qué la interfaz física del router-on-a-stick normalmente no recibe una IP de usuario?
11. ¿Qué ocurriría si la VLAN 30 no estuviera permitida en un trunk intermedio?
12. ¿Qué diferencia hay entre una subinterfaz y una SVI?
13. ¿Qué comando usarías para demostrar que existen las subinterfaces?
14. ¿Cómo demostrarías que `Ethernet0/1.30` funciona como gateway?

### Recorrido y seguridad

15. ¿En qué momento el host decide enviar el paquete al gateway?
16. ¿Qué direcciones cambian en cada salto: MAC, IP o ambas?
17. ¿Dónde conviene aplicar la ACL de Estudiantes y en qué dirección?
18. ¿Por qué el acceso a una DMZ no significa acceso irrestricto?
19. ¿Interviene NAT entre C y A? Justificá.
20. ¿Qué tabla consulta `SwL3-5` después de aceptar el paquete?
21. ¿Qué papel cumple `R-C` después de `SwL3-5`?
22. ¿Cómo sabe OSPF llegar a la red del servidor?

### Diagnóstico práctico

23. El estudiante llega al gateway pero no al servidor: ¿qué revisarías en orden?
24. No llega al gateway: ¿qué evidencias de VLAN/trunk/subinterfaz buscarías?
25. La ACL muestra cero matches: ¿qué hipótesis planteás?
26. OSPF tiene vecinos, pero no aparece la red destino: ¿qué puede faltar?
27. El ping funciona y HTTP no: ¿qué capas o políticas revisarías?
28. ¿Qué demostraría un traceroute que se detiene en `R-C`?

## Riesgos históricos

Esta matriz resume observaciones **históricas**, no el estado actual. Toda defensa
debe obtener evidencia nueva antes de afirmar que una capacidad continúa
operativa.

| Estado histórico | Capacidad u observación | Evidencia actual requerida |
|---|---|---|
| Demostrado históricamente | Existieron capacidades del núcleo y HSRP estuvo implementado. | Repetir estado y failover: `show standby brief`, caída controlada del activo, continuidad desde cliente, restauración y recuperación. HSRP sigue pendiente de evidencia final actual. |
| Observado con brechas | Una ACL Guest tuvo un `permit any` demasiado temprano; una ACL IoT permitió más destinos de los requeridos; QoS mostró marcado sin tráfico coincidente/prioridad efectiva. STP estaba presente, pero faltó demostrar su reconvergencia. La configuración básica de appliances no quedó demostrada de forma completa. Keepalived/bonding quedó con brecha en el failover de servidor. | Leer contadores y flujos permitido/denegado; generar tráfico QoS coincidente; cortar un enlace STP y medir la recuperación; mostrar saneados `hostname`, banner, consola, VTY y `enable secret`; provocar y revertir el failover Keepalived/bonding manteniendo el servicio. |
| Pendiente de evidencia actual | IPv6 fue requisito general con evidencia histórica pendiente; también quedaron pendientes wireless, alta densidad, redundancia de servidor y algunos servicios. | Para IPv6, verificar interfaces/rutas y conectividad extremo a extremo. Para el resto, definir estado inicial, estímulo, salida observable, resultado esperado y recuperación antes de atribuir cumplimiento. |

## Plan de cierre

Priorizar primero lo que bloquea la evaluación o las pruebas posteriores, sin
convertir el registro histórico en estado vigente:

1. **Base obligatoria:** inventariar modelo/imagen y validar configuración básica;
   cerrar VLSM, DMZ e IPv6. Resultado: inventario trazable, subredes sin solape,
   DMZ aislada y conectividad IPv6 verificable.
2. **Nivel 3:** probar reconvergencia STP. Resultado: camino alternativo activo y
   conectividad recuperada tras una falla controlada.
3. **Disponibilidad:** revalidar HSRP y luego, como recomendación independiente,
   bonding/Keepalived. Resultado: gateway y servicio sobreviven sus fallas
   respectivas y recuperan el estado restaurado.
4. **Nivel 4 y cierre documental:** completar Excel y `.txt` saneados, cotejarlos
   con la maqueta y enlazar cada fila del plan con una evidencia viva.
5. **Ensayo de nivel 5:** ejecutar el guion económico completo, registrar antes,
   durante y después, y eliminar repeticiones NAT que no agreguen cobertura.
