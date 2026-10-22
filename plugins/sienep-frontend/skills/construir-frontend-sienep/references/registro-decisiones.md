# Reestructura del frontend SIENEP — registro de decisiones

Para qué sirve: dejar escrito **qué** cambiamos, **por qué** y **cómo defenderlo**, sin depender de la IA. Cada entrada corresponde a un commit. El plan está en `plan-reestructura.md`.

## Mapa de patrones (la idea general)

| Capa en el front | Qué hace | Equivalente en el back |
|---|---|---|
| Página (`app/**/page.tsx`) | Contenedor: estado, navegación, qué hacer ante 401/403 | Controller |
| Servicio (`lib/<modulo>.ts`) | Acceso a la API: una función por endpoint, sin saber de la pantalla | Repository / DAO |
| Mapper (`crearPayload…`) | Transforma los datos del formulario en lo que espera la API | Mapper + DTO |
| Componente (`components/`) | Presentación: recibe datos y callbacks por props | Vista |
| Tipos (`types/`) | Una sola definición por entidad | Entidad / DTO |

**Frase de defensa:** "Separamos presentación de acceso a datos: las páginas no saben cómo se llama a la API, solo usan funciones como `obtenerEstudiante`. Es la misma idea que controller → service → repository en el backend."

---

## Entrada 0 — Quitar el ID de funcionario del registro común

- **Commit:** `4a29823` (rama `fix/instancia-sin-id-funcionario`), 21/10/2026.
- **Qué cambió:** `FormularioRegistroComun` ya no pide "ID del funcionario"; `crearPayloadRegistroComun` y `crearPayloadInstanciaDesdeRecordatorio` ya no lo envían. Se borró un tipo duplicado de `lib/instancias.ts` que no se usaba.
- **Antes / después:** antes el usuario escribía un número obligatorio; ahora el campo no existe.
- **Patrón:** responsabilidad en el servidor. El dato que identifica a quien hace la acción sale de la sesión (JWT), no del formulario.
- **Por qué es mejor:** el backend (`InstanciaService`, commit `ea1344c`) ya ignoraba ese valor y usaba el funcionario autenticado. El campo era obligatorio, confundía y se descartaba igual.
- **Evidencia:** 61/61 tests; Playwright con la API simulada: los dos POST (`/api/instancias/comunes` y `/api/recordatorios/{id}/instancias`) salen sin `idFuncionario`.
- **Defensa en 30 segundos:** "¿Quién registró la instancia? El backend lo saca del token. El front no puede elegirlo, así nadie puede atribuirle un registro a otro funcionario. Por eso quitamos el campo. Límite: la edición (PUT) en el backend todavía acepta `idFuncionario`; hoy no hay pantalla que la use."
- **Preguntas probables:**
  - *¿Y si alguien manda el campo con Postman?* Al crear, el backend lo pisa con el funcionario autenticado.
  - *¿Por qué no validarlo en el front?* Porque el front se puede saltear; la regla tiene que estar en el servidor.

---

## Entrada 1 — Un solo helper (`lib/solicitud.ts`) y un solo error (`ErrorApi`)

- **Rama:** `refactor/solicitud-unica` (apilada sobre `fix/instancia-sin-id-funcionario`), 21/10/2026. Commit: `831ea5d`.
- **Qué cambió:**
  - Nuevo `lib/solicitud.ts` con `ErrorApi`, `crearOpcionesAutenticadas` y `solicitarJson`.
  - `lib/recordatorios.ts` y `lib/instancias.ts` borraron sus copias y usan el helper único.
  - `lib/instancias.ts` pasó a la firma estándar `(apiUrl, token, …, fetchImpl)`.
  - 7 pantallas importan `ErrorApi` de `@/lib/solicitud` y, ante un 401, llaman a `limpiarSesion()`.
  - `tsconfig.json`: `allowImportingTsExtensions`.
- **Antes / después:**
  - Antes había 3 copias de `solicitarJson` y 3 clases de error (`ErrorApiRecordatorio`, `ErrorApi` de instancias y `ErrorApiGoogleCalendar`).
  - Ahora hay 1 helper y 1 error para recordatorios e instancias (Calendar se decide en la Tarea 9).
  - Antes el 401 hacía `localStorage.removeItem("token")`; ahora hace `limpiarSesion()`.
- **Patrón:** capa de acceso a datos con un helper interno compartido, como `JdbcTemplate` para los repositorios. Las páginas nunca lo usan directamente: llaman a funciones con nombre, como `obtenerCategorias`.
- **Por qué es mejor:**
  - Una sola regla para leer errores (`mensaje`, `message` o lista `errores`).
  - Funciona con `FormData` (archivos) y con respuestas vacías (204).
  - `instancias.ts` ahora se puede testear.
  - Al vencer la sesión se limpia también `sessionStorage`, que es lo que pide RF04.
- **Evidencia:**
  - 68/68 tests (6 nuevos de `solicitud`, 1 nuevo de `instancias`); tsc, lint y build OK.
  - Playwright: las llamadas por pantalla no cambiaron (recordatorios 4, detalle 3, nuevo 1, instancias 2, nueva 2).
  - Con un 401 forzado, la página vuelve a `/` con `localStorage` y `sessionStorage` vacíos.
- **Defensa en 30 segundos:** "Todas las llamadas pasan por `solicitarJson`, que agrega el token, interpreta el error del backend y lanza `ErrorApi` con el código HTTP. La página solo decide: con 401 cierra la sesión con `limpiarSesion()`, que borra token y datos temporales (RF04); con 403 muestra que no tiene permisos. Límite: Google Calendar todavía usa su propio helper, y el resto de las pantallas se migra en las tareas siguientes."
- **Preguntas probables:**
  - *¿Por qué no axios?* No hace falta: `fetch` es nativo y el helper tiene 80 líneas que se pueden explicar línea por línea.
  - *¿Por qué el 401 se maneja en la página y no en el helper?* Porque redirigir es responsabilidad de la pantalla (necesita el `router`). El servicio no sabe de navegación, igual que un repository no sabe de HTTP.
  - *¿Para qué `fetchImpl`?* Para inyectar un `fetch` falso en los tests y probar sin backend.
  - *¿Por qué no se manda `Content-Type` con archivos?* Con `FormData` el navegador arma el `multipart/form-data` con su *boundary*; si lo forzamos a JSON, el backend no puede leer el archivo.

---

## Entrada 2 — Servicio de autenticación (`lib/auth.ts`)

- **Rama:** `refactor/servicio-auth` (apilada sobre `refactor/solicitud-unica`), 21/10/2026. Commit: `7ae282c`.
- **Qué cambió:**
  - Nuevo `lib/auth.ts` con `iniciarSesion(apiUrl, email, password)` y `cerrarSesion(apiUrl, token)`.
  - El login (`app/page.tsx`), el botón "Cerrar sesión" (`AppHeader`) y el cierre por inactividad (`AuthGuard`) los usan.
  - `solicitud.ts` ya no manda `Authorization` cuando no hay token (caso del login).
- **Antes / después:**
  - El login tenía 30 líneas de `fetch` y lectura de errores; ahora es una llamada y un `catch`.
  - El logout estaba copiado en dos componentes; ahora está en una función.
- **Patrón:** capa de servicios (DAO) + un único punto de manejo de errores (`ErrorApi`).
- **Por qué es mejor:**
  - **F9 corregido:** antes el login leía el JSON antes de mirar el status; si Railway devolvía un 502 en HTML, decía "No se pudo conectar al servidor", que era falso. Ahora distingue tres casos: error del servidor ("No se pudo iniciar sesión."), validación (mensajes de cada campo) y sin red ("No se pudo conectar al servidor").
  - El logout ahora tiene `catch`: si el backend falla, la sesión local se cierra igual y no queda un error sin manejar.
- **Evidencia:**
  - 72/72 tests (3 de `auth`, 1 de token vacío); tsc, lint y build OK.
  - Playwright: login correcto → `/dashboard` con token y sin `Authorization` en el pedido; 400 → "El email no es válido | La contraseña es obligatoria"; 502 HTML → "No se pudo iniciar sesión."; sin red → "No se pudo conectar al servidor".
  - Logout con el botón, con backend 200 y con 500 → vuelve a `/` con `localStorage` y `sessionStorage` vacíos y `Authorization: Bearer …` en el pedido.
  - Inactividad (reloj del navegador adelantado): a los 14 min sigue en el dashboard; a los 15 llama al logout y vuelve a `/` limpio. 0 errores de JavaScript.
- **Defensa en 30 segundos:** "El login y el logout pasan por `lib/auth.ts`. Si el backend devuelve errores de validación los mostramos campo por campo; si devuelve un error del servidor no lo confundimos con falta de conexión. Al cerrar sesión, manual o por 15 minutos de inactividad (RF04), avisamos al backend y siempre limpiamos el token y los datos temporales, aunque el backend falle. Límite: la invalidación real del JWT la hace el backend."
- **Preguntas probables:**
  - *¿Por qué el login no manda token?* Porque todavía no lo tiene; el backend lo devuelve en la respuesta y lo guardamos en `localStorage`.
  - *Si el backend falla al cerrar sesión, ¿el usuario queda logueado?* No: el `finally` siempre limpia la sesión local y vuelve al login.
  - *¿Cómo probaron los 15 minutos sin esperar?* Con el reloj falso de Playwright (`page.clock`), que adelanta el tiempo del navegador.

---

## Entrada 3 — Servicio de estudiantes (`lib/estudiantes.ts`) y tipo único de ficha

- **Rama:** `refactor/servicio-estudiantes` (apilada sobre `refactor/servicio-auth`), 21/10/2026. Commit: `7404dcb`.
- **Qué cambió:**
  - Nuevo `lib/estudiantes.ts`: `armarParametrosBusqueda`, `buscarEstudiantes`, `obtenerEstudiante`, `darDeBajaEstudiante`.
  - Nuevo `lib/usuarios.ts`: `reactivarUsuario`.
  - Nuevos tipos `EstudianteDetalle` (en `types/estudiante.ts`) y `Pagina<T>` (en `types/pagina.ts`).
  - Migradas 4 pantallas: listado, ficha, instancias del estudiante y nueva instancia (68 líneas agregadas y 217 borradas).
- **Antes / después:**
  - `GET /api/estudiantes/{id}` estaba escrito en 4 pantallas y el tipo `Estudiante` redefinido en 4 lugares. Ahora hay una función y un tipo.
  - Cada `fetch` tenía su `if (data === null) return;` porque el `.then` del 401 devolvía `null`. Ahora el 401 llega al `.catch` como `ErrorApi`: el `.then` queda con el caso feliz y el `.catch` con los errores.
- **Patrón:** capa de servicios (DAO) + tipos compartidos como "DTO del front". `Pagina<T>` es el espejo de `Page<T>` de Spring.
- **Por qué es mejor:**
  - Si cambia el endpoint del estudiante, se cambia en un lugar.
  - La armado de la búsqueda (RF08) ahora tiene test.
  - La ficha muestra "No tenés permisos para ver este estudiante." con 403 (F8).
  - El listado y la ficha limpian `sessionStorage` con 401 (F2).
- **Un detalle que salió en la verificación:** la página del listado ya tenía una función `buscarEstudiantes()` (el botón Buscar) que tapaba al servicio con el mismo nombre. TypeScript lo detectó y se resolvió importando el servicio como `buscarEstudiantesApi`, la misma convención que `cerrarSesionApi` en `AppHeader`.
- **Evidencia:**
  - 77/77 tests (4 de estudiantes, 1 de usuarios); tsc, lint y build OK.
  - Playwright: listado 1 llamada; ficha 2; instancias 2; nueva 2 (igual que en la auditoría).
  - Buscar con cédula " 123 " → `&cedula=123` (recortada).
  - Dar de baja → `DELETE /api/estudiantes/1` y vuelve a `/estudiantes`.
  - Ficha con 403 → "No tenés permisos para ver este estudiante."
  - 401 en listado y ficha → `/` con token y `sessionStorage` vacíos.
- **Defensa en 30 segundos:** "Las pantallas de estudiantes no hacen `fetch`: llaman a `obtenerEstudiante` o a `buscarEstudiantes` de `lib/estudiantes.ts`, igual que un controller llama al repository. El tipo de la ficha está una sola vez en `types/`. Así, si el backend cambia la ruta o un campo, se corrige en un lugar y los tests lo detectan. Límite: la pantalla de edición todavía tiene sus propios `fetch`; se migra en la tarea siguiente."
- **Preguntas probables:**
  - *¿Qué es `Pagina<T>`?* Un tipo genérico para la respuesta paginada de Spring: `content`, `number`, `totalPages` y `totalElements`. Sirve para estudiantes y para cualquier otro listado paginado.
  - *¿Por qué `reactivarUsuario` está en `usuarios.ts` y no en `estudiantes.ts`?* Porque el endpoint es `/api/usuarios/{id}/reactivar`: reactiva al usuario, que puede ser estudiante o funcionario.
  - *¿Por qué `buscarEstudiantesApi`?* Para no chocar con el handler del botón, que ya se llamaba `buscarEstudiantes`. El sufijo `Api` indica que viene del servicio.
