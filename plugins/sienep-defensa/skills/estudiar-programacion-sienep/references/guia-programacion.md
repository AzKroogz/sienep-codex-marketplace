# Guía de programación SIENEP

## Índice

1. Arquitectura
2. Seguridad
3. Reglas transversales
4. Mapa RF
5. Pruebas y Swagger
6. Preguntas docentes

## Arquitectura

```text
Swagger/cliente -> SecurityFilterChain -> JwtAuthenticationFilter
-> Controller -> DTO + @Valid -> Service + @Transactional
-> Repository -> JPA/Hibernate -> PostgreSQL
-> Mapper -> DTO de respuesta -> JSON
```

- Controller: contrato HTTP y status.
- DTO: entrada/salida sin exponer el modelo interno.
- Service: reglas de negocio y coordinación.
- Repository: acceso a datos.
- Entity: persistencia.
- Mapper: conversión.
- Exception handler: errores uniformes.

Patrones defendibles además de DTO: Repository, Service Layer, Mapper, Specification e inyección de dependencias.

## Seguridad

Flujo de login:

1. buscar usuario por email;
2. controlar intentos fallidos;
3. comparar contraseña con BCrypt;
4. rechazar usuario inactivo;
5. generar JWT con expiración;
6. auditar el resultado.

Flujo protegido:

1. recibir `Authorization: Bearer`;
2. validar firma y expiración;
3. extraer email;
4. verificar usuario activo;
5. cargar permisos del rol;
6. poblar SecurityContext;
7. aplicar `@PreAuthorize`.

JWT autentica la identidad; authorities y `@PreAuthorize` autorizan acciones. El payload JWT puede leerse: no guardar secretos en él.

## Reglas transversales

- Cédula uruguaya: normalizar y validar dígito verificador.
- Edad: calcular años completos con `Period`.
- Contraseña: almacenar hash y excluirla de respuestas/logs.
- Baja lógica: cambiar estado y preservar historial.
- Auditoría: usuario, fecha/hora, acción, resultado y entidad.
- Datos sensibles: permiso específico y DTO controlado.
- PostgreSQL/JPA: `spring.jpa.hibernate.ddl-auto=validate`.
- DTO obligatorio y al menos otro patrón justificable.

`validate` compara mappings con el esquema y falla ante incompatibilidades; no crea ni modifica tablas.

## Mapa RF

Estado orientativo de una auditoría histórica de `main`: 28 claros, 9 parciales/básicos/condicionados y 3 no localizados. Verificar después de cada integración.

| Grupo | Cobertura observada | Riesgo principal |
|---|---|---|
| RF01-RF04 autenticación | login/JWT implementado | pantalla frontend, gestión de credenciales y revocación/logout parciales |
| RF05-RF09 estudiantes | CRUD, búsqueda y baja lógica | adjuntos guardan metadatos/URL, no necesariamente archivo binario |
| RF10-RF18 instancias | alta, tipos, vistas, código, gestión, clonación y ficha | Calendar/notificación de ID parciales |
| RF19-RF27 recordatorios | CRUD, recurrencia, consultas, ID e instancia desde recordatorio | notificación depende de Google |
| RF28-RF29 incidencias | registro e historial | verificar datos y permisos de demostración |
| RF30-RF31 reportes | seguimiento y PDF | probar descarga real |
| RF32-RF37 administración | roles, permisos y categorías de instancia | verificar auditoría completa |
| RF38-RF40 categorías de recordatorio | no localizadas históricamente | un campo `tipo` no equivale a un ABM de categorías |

### Dominio principal

- Usuario, Estudiante y Funcionario.
- Rol-Permiso many-to-many.
- Instancia con detalles Comun/Incidencia.
- Participante con clave compuesta.
- Recordatorio con recurrencia.
- Informe de salud y adjunto médico.
- Auditoría y reportes.

### Transacciones

Usar transacción cuando un caso realiza varias escrituras que deben confirmarse o revertirse juntas. Diferenciar validación de DTO, regla de negocio y restricción de base.

### Calendar

La integración histórica generaba OAuth, intercambiaba el código, creaba eventos desde recordatorios, convertía recurrencia a RRULE e invitaba participantes. Riesgos: tokens en memoria, ausencia de renovación/persistencia segura y dependencia externa.

## Pruebas y Swagger

Estado histórico: 25 pruebas, 18 correctas y 7 errores. Causas observadas:

- mocks faltantes de `UsuarioAutenticadoService`;
- mock faltante de un servicio requerido por controller tests;
- contexto completo sin URL JDBC de test válida.

No afirmar que la suite está verde sin volver a ejecutarla. Preferir perfil de test aislado o Testcontainers.

Secuencia Swagger recomendada:

1. login inválido;
2. login válido;
3. Authorize con bearer token;
4. búsqueda de estudiante;
5. crear/consultar instancia;
6. crear/consultar recordatorio;
7. clonar o crear instancia desde recordatorio;
8. descargar reporte PDF;
9. demostrar 403 con un perfil sin permiso.

No mostrar secretos, contraseñas, tokens completos ni credenciales OAuth.

## Preguntas docentes

1. ¿Qué diferencia hay entre autenticación y autorización?
2. ¿Qué recorrido hace una petición con JWT?
3. ¿Por qué BCrypt no se desencripta?
4. ¿Qué garantiza la firma JWT?
5. ¿Por qué `ddl-auto=validate` es obligatorio?
6. ¿Por qué usar DTO y mapper?
7. ¿Qué revierte una transacción?
8. ¿Cómo funciona una baja lógica?
9. ¿Cómo se aplican roles y permisos?
10. ¿Cuál es la diferencia entre 401 y 403?
11. ¿Cómo se genera y clona una instancia?
12. ¿Cómo funciona la recurrencia?
13. ¿Qué limitaciones tiene Calendar?
14. ¿Cómo se protegen datos médicos?
15. ¿Qué pruebas fallan y cómo se arreglan?

Mejoras defendibles: Java 21 consistente, suite verde, revocación/refresh tokens, almacenamiento seguro de adjuntos/OAuth, categorías de recordatorio, migraciones Flyway/Liquibase y observabilidad.
