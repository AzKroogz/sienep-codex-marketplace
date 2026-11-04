# Guía de programación SIENEP (estado final, 3/11/2026)

Fuente verificada: GitLab `pft-main` (back `0a8dc68`, front `56de7be`). Antes de afirmar algo nuevo, mirar el código: esta guía es una foto del cierre.

## Índice

1. Entrega y repositorios
2. Arquitectura del backend
3. Arquitectura del frontend
4. Seguridad
5. Reglas transversales
6. Estado de los RF y limitaciones
7. UX y heurísticas
8. Pruebas, despliegue y base de datos
9. Entregables
10. Preguntas probables

## 1. Entrega y repositorios

- Equipo **SunSolutions**: Emanuel Turrión, Nicolás Ramírez y Facundo Abella. Entrega final: 6/11/2026.
- GitLab institucional (repositorio oficial): back `proyecto2dosem/sienep`, front `proyecto2dosem/sienep-frontend`.
- Ramas:
  - `develop`: integración.
  - `pft-main`: producción. Tiene todo `develop`.
  - `main`: histórica, del PDI.
  - Cada tarea va en `feat/…` o `fix/…` y entra por merge request.
- GitHub `develop` es un espejo para desplegar el back en Railway. Tiene el mismo contenido que GitLab, pero otra historia, por los cherry-picks.
- El front no se despliega: se muestra en local (`npm run build` + `npx next start`) contra el back de Railway.

## 2. Arquitectura del backend

Java 21, Spring Boot 4.0.6, Spring Web MVC, Data JPA (Hibernate), Validation, Security, JJWT 0.13, PostgreSQL, Springdoc (Swagger), OpenPDF, Lombok. Paquete `com.sienep.pdi_sienep3`.

```text
Cliente/Swagger -> SecurityFilterChain -> JwtAuthenticationFilter
-> Controller (@PreAuthorize) -> DTO + @Valid -> Service (@Transactional)
-> Repository (JPA, Specification) -> PostgreSQL (esquema proyectopdi)
-> Mapper -> DTO de respuesta -> JSON
```

| Paquete | Archivos | Para qué |
|---|---|---|
| controller | 20 | Contrato HTTP, códigos de estado y permisos con `@PreAuthorize` |
| service | 23 | Reglas de negocio y transacciones |
| repository | 24 | Acceso a datos (Spring Data JPA) |
| model | 27 | Entidades JPA |
| dto | 68 | Entrada y salida de la API; nunca se exponen las entidades |
| mapper | 10 | Entidad ↔ DTO, uno por entidad |
| specification | 1 | `EstudianteSpecification`, para búsquedas con filtros combinables |
| security | 4 | `JwtService`, `JwtAuthenticationFilter`, `GoogleLoginSuccessHandler`, `GoogleCalendarTokenCipher` |
| exception | 9 | `GlobalExceptionHandler` y excepciones de negocio |
| config | 7 | `SecurityConfig`, `CorsConfig`, `OpenApiConfig`, `PasswordConfig`, `S3Config`, `FechaHoraSienep` |

**Patrones:**
- DTO, que es obligatorio.
- Mapper.
- Specification.
- Repository.
- Service Layer.
- Inyección de dependencias.

Explicar cada uno con un ejemplo concreto: por ejemplo, `EstudianteSpecification` arma un `where` según los filtros que vienen vacíos o no.

**Dominio:**
- Usuario, con dos tipos: Funcionario y Estudiante. El estudiante no es un rol.
- Rol y Permiso, en relación muchos a muchos.
- Instancia, que es común o incidencia.
- Participante, con clave compuesta.
- Categoría de instancia y Categoría de recordatorio, las dos con baja lógica.
- Recordatorio, con recurrencia.
- Informe médico, guardado en un bucket S3 de Railway.
- Auditoría, con cambios en JSONB.
- Evento de Google Calendar.

## 3. Arquitectura del frontend

Next.js 16 (App Router, páginas `"use client"`), React 19, TypeScript estricto y Tailwind 4. Las pruebas son `node:test` sobre `lib/`.

```text
Página (app/**/page.tsx: estado, navegación, errores)
  -> servicio lib/<modulo>.ts (una función por endpoint)
    -> solicitarJson (lib/solicitud.ts) -> fetch con Bearer
       errores -> ErrorApi (status, message, errores)
```

- 25 páginas:
  - login;
  - inicio;
  - estudiantes: lista, ficha, edición e instancias;
  - instancias: lista, nueva, detalle, edición y clonación;
  - recordatorios: lista, nuevo y detalle;
  - reportes;
  - configuración: usuarios, roles y las dos categorías;
  - cambiar contraseña;
  - retornos de OAuth.
- 21 módulos en `lib/` (`estudiantes.ts`, `instancias.ts`, `recordatorios.ts`, `reportes.ts`, `roles.ts`, `usuarios.ts`, `permisos.ts`, `solicitud.ts`, `api.ts`…), con sus tests. Los componentes de cada módulo están en `components/<modulo>/`.
- Sesión:
  - El token y los permisos se guardan en `sessionStorage`, a través de `lib/api.ts`.
  - `AuthGuard` protege las rutas de `(protected)`.
  - La sesión se cierra a los 15 minutos sin uso; el JWT en sí dura 24 h.
- Si la API responde 401, la página hace `limpiarSesion()` y redirige al login. Si responde 403, muestra "No tenés permisos para …".
- El front oculta botones según los permisos solo por comodidad: **la autorización real está en el back**.

## 4. Seguridad

**Login** (`AuthService`):
1. Busca el usuario por email.
2. Si tuvo demasiados intentos fallidos, lo bloquea un tiempo (`DemasiadosIntentosException`, auditado como `LOGIN_BLOQUEADO`).
3. Compara la contraseña con BCrypt.
4. Rechaza las cuentas inactivas.
5. Genera el JWT con el email, el `tokenVersion` y una expiración de 24 h.
6. Audita el login, exitoso o fallido.

**Pedido protegido:**
1. Llega `Authorization: Bearer …`.
2. Se validan la firma y la expiración.
3. El `tokenVersion` del token tiene que coincidir con el de la base.
4. El usuario tiene que estar activo.
5. Se cargan los permisos del rol al SecurityContext.
6. Se aplica `@PreAuthorize`.

**Puntos clave:**
- **Logout real (RF04):** al cerrar sesión se incrementa `usuarios.token_version` (migración `20261014_usuarios_token_version.sql`). Eso invalida en el servidor todos los tokens anteriores, aunque el JWT sea stateless.
- **Google (OAuth 2.0):**
  - `GoogleLoginSuccessHandler` emite el JWT propio de SIENEP.
  - Los permisos siguen siendo los del rol interno: OAuth autentica, pero no autoriza.
  - Una cuenta de Google que no esté registrada en SIENEP no entra.
- **Primer acceso:**
  - La cuenta nace pendiente y con `debe_cambiar_contrasena`.
  - Mientras eso esté activo, el back rechaza todo salvo cambiar la clave, ver los datos propios y cerrar sesión.
- **Calendar:** cada usuario da su consentimiento OAuth. Los tokens de Google se guardan cifrados con `GoogleCalendarTokenCipher`, y si vencen se pide reconectar.
- **Errores:** `GlobalExceptionHandler` devuelve mensajes genéricos. Los parámetros inválidos dan 400 (`PARAMETRO_INVALIDO` o `PARAMETRO_FALTANTE`), no 500. Ningún log imprime contraseñas ni tokens.

**Confusiones a corregir:**
- JWT está firmado, no cifrado: el contenido se puede leer.
- BCrypt es un hash, no cifrado.
- 401 es "no autenticado"; 403 es "autenticado pero sin permiso".

## 5. Reglas transversales

- **Cédula uruguaya:** se valida el dígito verificador. Ejemplo: `12345678` da "La cédula uruguaya no es válida".
- **Edad mínima de 18 años**, en años completos: "El usuario debe ser mayor de edad".
- **Baja lógica:** se cambia el estado y se conserva el historial, en estudiantes, instancias, informes, categorías y recordatorios.
- **Auditoría:** registra usuario, fecha y hora, acción, entidad y resultado, más el valor anterior y el nuevo en las modificaciones (JSONB). Cubre altas, bajas, modificaciones y login. No guarda contraseñas, datos médicos ni comentarios confidenciales.
- **Datos sensibles** (salud, motivo de derivación, comentario confidencial):
  - requieren un permiso específico y se exponen con DTO controlado;
  - nunca aparecen en los listados;
  - en la demostración se usa el rol Legales, que los ve pero no edita.
- **`ddl-auto=validate`:** Hibernate solo compara el mapeo con el esquema. Cada cambio de la base es un script en `db/migrations/` con su script de reversión, y lo aplica una persona.
- **Zona horaria:** `America/Montevideo` en Hibernate y Jackson (`FechaHoraSienep`). El front manda la hora local, no UTC.

## 6. Estado de los RF y limitaciones

Son 38 obligatorios, todos implementados (36 cumplen la ficha y 2 tienen un límite declarado), más los 2 opcionales (RF30 y RF31).

| Módulo | RF | Notas para defender |
|---|---|---|
| 1. Acceso | 01–04 | Login con contraseña y con Google, bloqueo por intentos, cuentas pendientes y cambio de clave obligatorio, logout con `token_version` |
| 2. Estudiantes | 05–09 | Alta con cédula, edad, motivo, foto y dirección; baja lógica con aviso de instancias futuras; búsqueda con Specification, orden y paginación; informes médicos (PDF o imagen de hasta 10 MB) en el bucket, descargados con enlace temporal |
| 3. Instancias | 10–18 | Común o incidencia; categoría editable, sin permitir categorías inactivas; vista según permisos; Calendar; código único; edición, baja y clonación numerada; alta desde la ficha |
| 4. Recordatorios | 19–27 | Recurrencia diaria, semanal o mensual, que termina por cantidad o por fecha; tipo de un catálogo administrable; evento en Calendar con invitación por correo (RF23) auditado; pestañas vencidos, hoy y próximos; crear instancia desde el recordatorio, que queda "Cumplido" |
| 5. Incidencias | 28–29 | Lugar e involucrados externos; historial en la ficha con filtro por período |
| 6. Reportes (opcional) | 30–31 | Filtros por carrera, grupo y período; totales; CSV; acceso a Looker para el análisis histórico |
| 7. Administración | 32–40 | Roles predefinidos y personalizados, con permisos agrupados; no se puede quitar el propio acceso a roles; ABM de categorías de instancia y de recordatorio; no se puede dar de baja una categoría con instancias futuras activas |

**Limitaciones declaradas.** Decirlas antes de que pregunten: suma credibilidad.

| RF | Límite | Qué hay en su lugar o qué se propone |
|---|---|---|
| 05 | Sin importación desde la preinscripción | No hay un formato definido. Se propone un CSV con un informe de filas aceptadas y rechazadas |
| 14 | El ID es `INST-` + fecha-hora, único pero no correlativo por año | Hay constraint UNIQUE. Se propone una tabla `secuencias_instancia(anio, ultimo)` |
| 15 | El ID se muestra en pantalla, no se manda por correo | — |
| 22 | El evento de Calendar se crea con un botón, no automáticamente | Es por consentimiento y control del usuario |
| 23 | Sin WhatsApp; el correo lo envía Google | La letra condiciona WhatsApp a que esté habilitado. Solo se audita el alta del evento |
| 12 | Sin control de pertenencia: quien tiene `VER_INSTANCIAS` ve todas | — |
| 31 | CSV y pantalla; sin Excel ni PDF agregado | El CSV abre en Excel. El PDF por estudiante existe solo en la API |
| 33 | La carga de los roles base no registra auditoría | — |
| RNF01 | Los datos de salud no se cifran en la base | HTTPS en tránsito, hash de contraseñas y tokens de Calendar cifrados |
| RNF07 | El filtro de instancias pide el ID del estudiante | Está propuesto buscar por nombre o cédula |

## 7. UX y heurísticas

- **Documento UX:** `ux/documento-ux.pdf` en el front, de 4 páginas. Tiene comparaciones prototipo/final, justificación, prueba de usabilidad y mejoras. En el repo está la versión del 2/11; la versión reescrita, con 3 comparaciones, está en Drive (Sprint 4/Programacion) y en `~/Escritorio/documento-ux-sienep.pdf`.
- **Prototipo:** de baja fidelidad, en Figma Make, con 15 pantallas. Las capturas están en `Arquetipo.pdf`, de la Entrega 2.
- **Cuatro heurísticas de Nielsen:**
  1. Consistencia y estándares: todas las listas tienen el formato de Usuarios.
  2. Prevención y manejo de errores: confirmación antes de crear y de dar de baja, y reglas con mensajes claros.
  3. Feedback inmediato: "Guardando…", avisos de resultado, contadores, pestañas con cantidades y una sola opción marcada en el menú.
  4. Reconocimiento antes que recuerdo: el grupo depende de la carrera, hay listas para elegir y los filtros tienen ejemplos.
- **Prueba de usabilidad:** la hizo Nicolás Ramírez como usuario simulado, el 2/11. Encontró 4 problemas y los 4 se corrigieron:
  1. el menú marcaba dos opciones;
  2. los botones de archivo no tenían marco;
  3. las listas tenían formatos distintos;
  4. las altas no pedían confirmación.
- **Guion de la demostración en vivo:** `~/Escritorio/guion-demostracion-heuristicas-nielsen.md`.

## 8. Pruebas, despliegue y base de datos

- **Back:** 279 pruebas con JUnit 5 y Mockito, 0 fallos (3/11).
- **Front:** 148 pruebas con `node --test`, 0 fallos. ESLint, `tsc` y el build sin errores.
- **Back y front se levantan desde cero siguiendo los README.** Se verificó el 3/11:
  - el back arranca en unos 10 s;
  - `/v3/api-docs` responde 200;
  - un endpoint sin token responde 401.
- **Railway:**
  - back: se despliega desde GitHub `develop`;
  - PostgreSQL;
  - bucket `sienep-informes-medicos2`.
- **Migraciones:** van en `db/migrations/AAAAMMDD_*.sql`, con su `_rollback.sql`. Las últimas son las categorías de recordatorio, el motivo de derivación, `debe_cambiar_contrasena` y los cambios de la auditoría en JSONB.

## 9. Entregables

- **Checklist oficial marcado:** 147 de 162 Cumple y 15 parciales con el motivo escrito. El apartado 16 está completo (SunSolutions, 3/11/2026, responsable Nicolás Ramírez). Archivo: `~/Escritorio/Checklist Programación_PFT_SIENEP_2026 - marcado.pdf`.
- **Video final:** grabado, de 3 integrantes, siguiendo `~/Escritorio/guion-video-final-programacion.md`.
- **Drive** (Pre-entrega/Sprint 4/Programacion): los repositorios, los guiones, el documento UX y el checklist.

## 10. Preguntas probables

1. ¿Qué diferencia hay entre autenticación y autorización? ¿Dónde está cada una en SIENEP?
2. ¿Cómo invalida el logout un JWT si el token es stateless? (`token_version`)
3. ¿Qué pasa si alguien entra con una cuenta de Google que no existe en SIENEP?
4. ¿Por qué BCrypt no se puede "desencriptar"? ¿Qué garantiza la firma del JWT?
5. ¿Qué hace `ddl-auto=validate`? ¿Cómo cambiaron la base entonces?
6. ¿Para qué el DTO y el Mapper? ¿Qué es una Specification y dónde la usan?
7. ¿Qué revierte un `@Transactional`? Den un caso con varias escrituras.
8. ¿Por qué 400, 401, 403, 404 o 409 en tal caso?
9. ¿Cómo validan la cédula y la edad? ¿En qué capa?
10. ¿Cómo protegen los datos médicos? ¿Qué ve el rol Legales?
11. ¿Cómo se genera el ID de una instancia? ¿Por qué no es correlativo?
12. ¿Cómo funciona la recurrencia de un recordatorio y la notificación?
13. ¿Por qué no se puede dar de baja una categoría en uso?
14. ¿Cómo se organiza el front? ¿Por qué la página nunca llama a `fetch` directamente?
15. ¿Qué pasa en el front ante un 401 y ante un 403?
16. ¿Qué heurísticas aplicaron? Muéstrenlas en el sistema.
17. ¿Qué hizo cada integrante? ¿Cuál fue la dificultad principal? (La zona horaria)
18. ¿Qué mejorarían? (Correlativo por año, importación CSV, cifrado de salud, búsqueda de instancias por nombre, Excel)
