# Guía de infraestructura SIENEP

## Índice

1. Escenario
2. Núcleo obligatorio
3. Seguridad y servicios
4. Evidencias
5. Preguntas docentes
6. Riesgos históricos
7. Banco ampliado de preguntas

## Escenario

El campus SIENEP se representa con cinco sitios interconectados:

- A: administración, Data Center y POP;
- B: laboratorios de TI;
- C: aulas y biblioteca;
- D: cowork/BYOD;
- E: anfiteatro, eventos e IoT.

La defensa debe justificar disponibilidad, seguridad, segmentación y escalabilidad. El archivo portable de GNS3 y el video son excluyentes según la pauta resumida por el equipo.

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

Para cada demostración usar esta secuencia:

1. mostrar estado inicial;
2. formular resultado esperado;
3. ejecutar la prueba;
4. leer la salida relevante;
5. provocar la falla si corresponde;
6. comprobar convergencia;
7. restaurar y verificar.

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

Verificar antes de afirmar que siguen vigentes:

- una ACL Guest tuvo un `permit any` demasiado temprano;
- una ACL IoT permitió más destinos de los requeridos;
- QoS mostró marcado, pero faltó tráfico coincidente/prioridad efectiva;
- quedaron pendientes wireless, alta densidad, redundancia de servidor y algunos servicios.
