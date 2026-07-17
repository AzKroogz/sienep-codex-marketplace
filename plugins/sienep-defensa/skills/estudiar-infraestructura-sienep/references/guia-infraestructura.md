# Guía de infraestructura SIENEP

## Índice

1. Escenario
2. Núcleo obligatorio
3. Seguridad y servicios
4. Evidencias
5. Preguntas docentes
6. Riesgos históricos

## Escenario

El campus SIENEP se representa con cinco sitios interconectados:

- A: administración, Data Center y POP;
- B: laboratorios de TI;
- C: aulas y biblioteca;
- D: cowork/BYOD;
- E: anfiteatro, eventos e IoT.

La defensa debe justificar disponibilidad, seguridad, segmentación y escalabilidad. El archivo portable de GNS3 y el video son excluyentes según la pauta resumida por el equipo.

## Núcleo obligatorio

### Recorrido de un paquete

```text
Host -> puerto access -> VLAN -> trunk -> SVI/gateway
-> ACL -> routing OSPF -> backbone -> red destino
```

Hacia Internet:

```text
Host -> gateway -> ruta por defecto -> borde -> NAT/PAT -> ISP
```

### VLAN y routing inter-VLAN

- Una VLAN separa dominios de broadcast.
- Un access transporta una VLAN; un trunk transporta varias con 802.1Q.
- Una VLAN nativa segura y no utilizada reduce riesgos de tráfico sin etiqueta.
- El routing inter-VLAN requiere capa 3 mediante SVI, subinterfaces o router-on-a-stick.

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

## Riesgos históricos

Verificar antes de afirmar que siguen vigentes:

- una ACL Guest tuvo un `permit any` demasiado temprano;
- una ACL IoT permitió más destinos de los requeridos;
- QoS mostró marcado, pero faltó tráfico coincidente/prioridad efectiva;
- quedaron pendientes wireless, alta densidad, redundancia de servidor y algunos servicios.
