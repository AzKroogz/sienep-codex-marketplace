# Reestructura del frontend SIENEP — plan de implementación

> **Para quien lo ejecute:** se trabaja tarea por tarea. Antes de cada modificación de código se muestra el diff y se espera el OK del usuario. Al cerrar cada tarea se agrega una entrada en `registro-decisiones.md`. Los pasos usan casillas (`- [ ]`) para el seguimiento.

**Objetivo:** que todo el frontend siga los mismos tres patrones (capa de servicios por módulo, contenedor/presentación y mappers de payload), para que sea más fácil de mantener y de defender.

**Arquitectura:**
- **Páginas** (`app/**/page.tsx`): contenedores. Manejan el estado, la navegación y los errores (401 → `limpiarSesion()` + login; 403 → mensaje).
- **Servicios** (`lib/<modulo>.ts`): la "capa DAO" del front. Funciones con nombre, una por endpoint, que hacen el `fetch` mediante un único helper interno y devuelven datos o lanzan `ErrorApi`. No conocen `router` ni `useState`.
- **Componentes** (`components/<modulo>/`): presentacionales, reciben todo por props.
- **Tipos** (`types/`): una sola definición por entidad.

**Tecnologías:** Next.js 16.3.5, React 19.2.8, TypeScript 5.9 strict, tests con `node --test` (`lib/*.test.mjs`).

**Fuentes:** `auditoria-frontend.md` (hallazgos) y la conversación del 21/10 (decisión del patrón tipo DAO por módulo).

## Restricciones globales

- Código simple, nivel tecnicatura: sin dependencias nuevas, hooks propios, contextos, cliente genérico expuesto a las páginas ni librerías de componentes.
- Nombres en español, igual que el resto del repo.
- Firma de los servicios igual a la de `lib/recordatorios.ts`: `(apiUrl: string, token: string, ...args, fetchImpl: typeof fetch = fetch)`. La página pasa `API_URL`; el test pasa un `fetch` falso.
- Las páginas no llaman a `fetch` directamente. Excepción: la descarga desde `urlDescarga`, que es una URL firmada externa (`ListaInformesMedicos`).
- Toda respuesta 401 en una página: `limpiarSesion(); router.replace("/"); return;`.
- Una rama por tarea desde `origin/develop` (o apilada sobre la anterior si depende de ella), con merge request. Nunca push a `develop`, `main` ni `pft-main`; el push lo hace el usuario.
- Commits sin trailers ni archivos de IA.
- Al cerrar cada tarea deben pasar `npm test`, `npx tsc --noEmit`, `npx eslint .` y `npm run build`.
- Verificación en el navegador: build de producción + Playwright con `page.route('**/api/**')` y token falso. Las llamadas por pantalla no deben aumentar respecto de la tabla del §3 de la auditoría.
- Fuera de alcance: no se toca el backend ni la BD; no se agregan estilos (eso es otra etapa); `lib/calendario-google.ts` queda como está (ver Tarea 9).

## Puntos de revisión

1. **Sesión vencida (401) en cualquier pantalla migrada:** debe limpiar `localStorage` **y** `sessionStorage` y volver a `/`. Hoy no limpia `sessionStorage` (F2). Test: Tarea 1 (`ErrorApi.status === 401`); verificación Playwright en cada tarea.
2. **403 en `datos-sensibles`:** editar estudiante debe cargar igual, sin la sección de salud, aunque ahora la llamada vaya en paralelo. Test: Tarea 4.
3. **Respuesta vacía (204 o cuerpo vacío en DELETE/PATCH):** no debe romper con un error de JSON. Test: Tarea 1.
4. **Subida con `FormData` (foto, informe médico):** no debe enviarse `Content-Type`, para que el navegador ponga el boundary. Test: Tarea 1.
5. **Error 400 con lista `errores` (login, crear/editar funcionario):** se deben mostrar los mensajes de cada campo, no un genérico. Test: Tarea 1; uso en las Tareas 2 y 5.

---

### Tarea 1: helper único `lib/solicitud.ts` y error único `ErrorApi`

**Por qué:** hoy hay tres copias de `solicitarJson`/`obtenerMensajeError` y tres clases de error. Con un solo helper, los servicios se escriben todos igual.

**Archivos:**
- Crear: `lib/solicitud.ts`, `lib/solicitud.test.mjs`
- Modificar: `tsconfig.json` (agregar `"allowImportingTsExtensions": true`)
- Modificar: `lib/recordatorios.ts` (borrar su `ErrorApiRecordatorio`, `obtenerMensajeError`, `solicitarJson` y `crearOpcionesAutenticadas`; importarlos de `./solicitud.ts` y reexportarlos con `export { … } from "./solicitud.ts"`, y `ErrorApi as ErrorApiRecordatorio` mientras haya páginas que lo usen)
- Modificar: `lib/instancias.ts` (quitar `import { API_URL }`, su `ErrorApi` y su `solicitarJson`; pasar a la firma estándar `obtenerCategorias(apiUrl, token, fetchImpl)`, `obtenerInstanciasEstudiante(apiUrl, token, idEstudiante, fetchImpl)`, `crearIncidencia(apiUrl, token, idEstudiante, datos, fetchImpl)`, `crearRegistroComun(apiUrl, token, idEstudiante, datos, fetchImpl)`; sus imports internos pasan a relativos con `.ts`)
- Modificar los consumidores para que importen `ErrorApi` de `@/lib/solicitud` y llamen con `API_URL`: `recordatorios/page.tsx`, `recordatorios/[id]/page.tsx`, `recordatorios/nuevo/page.tsx`, `SelectorInstanciaRecordatorio.tsx`, `CrearInstanciaDesdeRecordatorio.tsx`, `estudiantes/[id]/instancias/page.tsx`, `estudiantes/[id]/instancias/nueva/page.tsx`. En esos mismos archivos, cada 401 pasa a `limpiarSesion()`.
- Crear: `lib/instancias.test.mjs` (casos nuevos)

**Interfaces que produce:**
```ts
export class ErrorApi extends Error {
  status: number;
  errores: string[];          // mensajes de cada campo, si la API los manda
  constructor(status: number, message: string, errores?: string[]);
}
export function crearOpcionesAutenticadas(token: string, opciones?: RequestInit): RequestInit;
export async function solicitarJson<T>(
  url: string, token: string, mensajeError: string,
  opciones?: RequestInit, fetchImpl?: typeof fetch
): Promise<T>;
```
Reglas de `solicitarJson`:
- Error: mensaje = `mensaje` → `message` → `mensajeError`. Si llega `errores: [{campo, mensaje}]`, se guardan sus `mensaje` en `errores` y el `message` es `errores.join(" | ")`.
- Éxito: si el cuerpo viene vacío devuelve `undefined`; si no, el JSON.
- Si `opciones.body` es un `FormData`, no agrega `Content-Type`.

- [ ] **Paso 1: tests que fallan** en `lib/solicitud.test.mjs`:
  - `"lanza ErrorApi con el status y el mensaje de la API"`: respuesta `{status: 403, body: {mensaje: "Sin permiso"}}` → `error.status === 403`, `error.message === "Sin permiso"`.
  - `"usa el mensaje por defecto si el error no trae JSON"`: 500 con texto plano → `message === mensajeError`.
  - `"junta los errores de validación"`: 400 `{errores: [{campo: "email", mensaje: "Email inválido"}, {campo: "cedula", mensaje: "Cédula inválida"}]}` → `error.errores` deep-equal `["Email inválido", "Cédula inválida"]` y `message === "Email inválido | Cédula inválida"`.
  - `"devuelve undefined si la respuesta está vacía"`: `new Response(null, {status: 204})` → `undefined`.
  - `"no pone Content-Type cuando el cuerpo es FormData"`: el `fetch` falso comprueba `"Content-Type" in headers === false` y que `Authorization === "Bearer jwt"`.
  - `"conserva el 401 para que la página cierre la sesión"`: 401 → `error instanceof ErrorApi && error.status === 401`.
- [ ] **Paso 2:** `npm test` → fallan los 6 tests nuevos (no existe el módulo).
- [ ] **Paso 3:** agregar `allowImportingTsExtensions` y crear `lib/solicitud.ts` (mostrar el diff primero).
- [ ] **Paso 4:** `npm test` → pasan los 6 nuevos y los 61 anteriores (`lib/recordatorios.test.mjs` sigue usando los reexports).
- [ ] **Paso 5:** `npx tsc --noEmit && npm run build` → sin errores. **Si el build rechaza el import con `.ts`**, detenerse y consultar al usuario antes de buscar alternativas.
- [ ] **Paso 6:** migrar `lib/recordatorios.ts` y `lib/instancias.ts` y agregar en `lib/instancias.test.mjs` `"crea un registro común con POST autenticado"` (verifica la URL `${apiUrl}/api/instancias/comunes`, el método `POST` y que el body no tenga `idFuncionario`). Correr `npm test`.
- [ ] **Paso 7:** migrar las 7 páginas y componentes consumidores (diff por archivo). Correr lint, tsc, test y build.
- [ ] **Paso 8:** Playwright: `/recordatorios`, `/recordatorios/1`, `/recordatorios/nuevo`, `/estudiantes/1/instancias` y `/nueva` con las mismas llamadas que en la auditoría; con 401 forzado en `/recordatorios`, comprobar que `sessionStorage` queda vacío y la URL es `/`.
- [ ] **Paso 9:** commit `refactor(api): unificar solicitarJson y ErrorApi en lib/solicitud` + entrada en el registro de decisiones.

### Tarea 2: servicio de autenticación `lib/auth.ts`

**Por qué:** el login y el logout tienen `fetch` sueltos, y el logout está duplicado en `AppHeader` y `AuthGuard` (F9: el login lee el JSON antes de mirar `ok`).

**Archivos:** crear `lib/auth.ts` y `lib/auth.test.mjs`; modificar `app/page.tsx`, `components/AppHeader.tsx` y `components/AuthGuard.tsx`.

**Interfaces:**
- Consume: `solicitarJson`, `ErrorApi` (Tarea 1).
- Produce: `iniciarSesion(apiUrl, email, password, fetchImpl?): Promise<{ token: string }>` (POST `/api/auth/login`, sin token: se pasa `""` y no se manda `Authorization` si el token está vacío; agregar esa regla y su test en `solicitud.ts`) y `cerrarSesion(apiUrl, token, fetchImpl?): Promise<void>` (POST `/api/auth/logout`).

- [ ] Tests: `"inicia sesión y devuelve el token"`, `"un 400 con errores llega como ErrorApi con la lista"`, `"cierra sesión con POST autenticado"`, y en `solicitud.test.mjs` `"sin token no envía Authorization"`.
- [ ] Implementar, migrar las 3 pantallas (el login muestra `error.errores.join(" | ")` o `error.message`; si el `fetch` falla, "No se pudo conectar al servidor").
- [ ] Verificación completa + Playwright del login con 401 y con 400 de validación.
- [ ] Commit `refactor(auth): mover login y logout a lib/auth` + registro.

### Tarea 3: tipos de estudiante y lectura (`lib/estudiantes.ts`)

**Por qué:** `GET /api/estudiantes/{id}` está escrito en 4 pantallas y el tipo `Estudiante` está redefinido 4 veces.

**Archivos:**
- Modificar: `types/estudiante.ts`. Agregar `EstudianteDetalle` (= `Estudiante` + `matricula`, `grupo`, `fechaNacimiento`, `idGrupo`, `idCarrera`, `estadoUsuario?`).
- Crear: `types/pagina.ts` con `Pagina<T> = { content: T[]; number: number; totalPages: number; totalElements: number }`.
- Crear: `lib/estudiantes.ts` y `lib/estudiantes.test.mjs`. Mover ahí `armarParametros` desde `estudiantes/page.tsx` como `armarParametrosBusqueda(filtros, pagina): URLSearchParams`.
- Crear: `lib/usuarios.ts` con `reactivarUsuario` (también lo usa la Tarea 5).
- Modificar: `estudiantes/page.tsx`, `estudiantes/[id]/page.tsx`, `estudiantes/[id]/instancias/page.tsx`, `estudiantes/[id]/instancias/nueva/page.tsx` (borrar sus tipos locales).

**Interfaces:**
- `buscarEstudiantes(apiUrl, token, filtros: FiltrosEstudiantes, pagina: number, fetchImpl?): Promise<Pagina<Estudiante>>`
- `obtenerEstudiante(apiUrl, token, idEstudiante: number, fetchImpl?): Promise<EstudianteDetalle>`
- `darDeBajaEstudiante(apiUrl, token, idEstudiante: number, fetchImpl?): Promise<void>` (DELETE)
- `reactivarUsuario(apiUrl, token, idUsuario: number, fetchImpl?): Promise<void>` (PATCH `/api/usuarios/{id}/reactivar`)

- [ ] Tests: `"arma los parámetros de búsqueda sin filtros vacíos"` (con `nombre: "  "` no aparece `nombre`; con `cedula: "123"` → `cedula=123`, `size=10`), `"busca estudiantes por GET autenticado"`, `"obtiene un estudiante por id"`, `"da de baja con DELETE y acepta respuesta vacía"`, `"reactiva un usuario con PATCH"`.
- [ ] Implementar y migrar las 4 pantallas: mismo comportamiento, 401 con `limpiarSesion()`, 403 en la ficha con "No tenés permisos para ver este estudiante." (F8).
- [ ] Verificación completa + Playwright: las 4 pantallas mantienen 1-2 llamadas.
- [ ] Commit `refactor(estudiantes): capa de servicios para búsqueda y ficha` + registro.

### Tarea 4: edición de estudiante

**Por qué:** es la pantalla más grande (942 líneas), con 10 `fetch` y 3 tandas de llamadas.

> El 19/10 el usuario dijo que quería escribir él esta pantalla. **Preguntarle antes de empezar** si la escribe él con este plan y revisión, o si la hago yo mostrando el diff.

**Archivos:**
- Crear: `lib/catalogos.ts` y `lib/catalogos.test.mjs`
- Modificar: `lib/estudiantes.ts` y su test
- Crear: `components/estudiantes/SeccionTelefonos.tsx` y `components/estudiantes/FormularioDatosSensibles.tsx` (presentacionales: reciben datos, estados de guardado y callbacks por props)
- Modificar: `estudiantes/[id]/editar/page.tsx` (los tipos locales pasan a `types/estudiante.ts`: `Direccion`, `Carrera`, `Grupo`, `Telefono`)

**Interfaces:**
- `listarCarreras(apiUrl, token, fetchImpl?): Promise<Carrera[]>`; `listarGrupos(apiUrl, token, idCarrera: number, fetchImpl?): Promise<Grupo[]>`
- `obtenerDireccion(apiUrl, token, idEstudiante, fetchImpl?): Promise<Direccion>`
- `actualizarEstudiante(apiUrl, token, idEstudiante, datos: DatosFormularioEstudiante, fetchImpl?): Promise<void>` (usa `crearPayloadEdicion`)
- `obtenerDatosSensibles(apiUrl, token, idEstudiante, fetchImpl?): Promise<DatosSensiblesFormulario | null>`: **devuelve `null` con 403**; los demás errores se lanzan.
- `actualizarDatosSensibles(...)`, `subirFotoEstudiante(apiUrl, token, idEstudiante, archivo: File, fetchImpl?): Promise<{ foto: string }>` (FormData con el campo `archivo`)
- `listarTelefonos(apiUrl, token, idEstudiante, fetchImpl?): Promise<Telefono[]>`; `actualizarTelefono(apiUrl, token, idEstudiante, numeroActual, numeroNuevo, fetchImpl?): Promise<Telefono>` (usa `crearSolicitudActualizacionTelefono`)

- [ ] Tests: `"datos sensibles devuelve null con 403"`, `"datos sensibles lanza ErrorApi con 500"`, `"sube la foto como FormData con el campo archivo"`, `"actualiza un teléfono con la ruta codificada"`, `"lista grupos de una carrera"`.
- [ ] Implementar. La carga inicial hace **un** `Promise.all` con estudiante, dirección, carreras, teléfonos y datos sensibles, y después `grupos`, que depende de `idCarrera`: pasa de 3 tandas a 2, con 6 llamadas.
- [ ] Extraer los dos componentes, sin cambiar el marcado ni las clases.
- [ ] Verificación completa + Playwright: 6 llamadas en 2 tandas; con 403 en `datos-sensibles` la página carga sin esa sección.
- [ ] Commit `refactor(estudiantes): servicios y componentes de la edición` + registro.

### Tarea 5: usuarios (`lib/usuarios.ts`)

**Archivos:** modificar `lib/usuarios.ts` y `lib/catalogos.ts`, crear `lib/usuarios.test.mjs`, crear `types/usuario.ts` (`Funcionario`, `FuncionarioDetalle`, `FuncionarioRequest`, `Opcion`), modificar las 3 páginas de `configuracion/usuarios`.

**Interfaces:** `listarFuncionarios`, `obtenerFuncionario(…, idFuncionario)`, `crearFuncionario(…, datos: FuncionarioRequest)`, `actualizarFuncionario(…, idFuncionario, datos)`, `desactivarFuncionario(…, idFuncionario)` (DELETE), y en catálogos `listarSedes` y `listarRoles`, que ya devuelven `Opcion[]` (`{ id, nombre }`; el mapeo desde `idSede`/`idRol` pasa al servicio).

- [ ] Tests: `"lista sedes como opciones id/nombre"`, `"crear funcionario con 400 devuelve la lista de errores"`, `"desactiva con DELETE"`.
- [ ] Implementar y migrar: los formularios muestran `error.errores` si vienen, si no `error.message`.
- [ ] Verificación completa + Playwright: 1/2/3 llamadas.
- [ ] Commit `refactor(usuarios): capa de servicios de cuentas` + registro.

### Tarea 6: informes médicos

**Archivos:** modificar `lib/informes-medicos.ts` y su test; modificar `components/estudiantes/ListaInformesMedicos.tsx` y `AdjuntarInformeMedico.tsx` (crear `types/informe-medico.ts` con `InformeMedico` y `DescargaInforme`).

**Interfaces:** `listarInformesMedicos(apiUrl, token, idEstudiante, fetchImpl?)`, `adjuntarInformeMedico(…, idEstudiante, archivo: File)`, `obtenerDescargaInforme(…, idEstudiante, idAdjunto): Promise<DescargaInforme>`, `eliminarInformeMedico(…, idEstudiante, idAdjunto)`. Todos usan `obtenerEndpointAdjuntosMedicos`.

- [ ] Tests: `"adjunta el informe como FormData"`, `"pide la URL de descarga del adjunto"`, `"elimina con DELETE"`.
- [ ] Implementar y migrar (el `fetch(descarga.urlDescarga)` queda como excepción documentada). Arreglar el filtro con closure vieja: `setInformes((actuales) => actuales.filter(...))`.
- [ ] Verificación completa + Playwright: la ficha sigue con 2 llamadas.
- [ ] Commit `refactor(informes): servicios de adjuntos médicos` + registro.

### Tarea 7: dashboard

**Archivos:** `lib/instancias.ts` y `lib/recordatorios.ts` (más sus tests), `dashboard/page.tsx` (borrar `consultar`).

**Interfaces:** `listarMisProximasInstancias(apiUrl, token, fetchImpl?): Promise<Instancia[]>` (`/api/instancias/mias/proximas`) y `listarMisProximosRecordatorios(apiUrl, token, fetchImpl?): Promise<Recordatorio[]>` (`/api/recordatorios/mios/proximos`).

- [ ] Tests de las dos rutas; implementar y migrar; verificación + Playwright (2 llamadas).
- [ ] Commit `refactor(dashboard): usar servicios de instancias y recordatorios` + registro.

### Tarea 8: formulario de recordatorio compartido

**Por qué:** `recordatorios/nuevo` y la edición en `recordatorios/[id]` repiten el formulario, y la edición no permite cambiar la recurrencia (F3).

**Archivos:** crear `components/recordatorios/FormularioRecordatorio.tsx`; modificar `recordatorios/nuevo/page.tsx` y `recordatorios/[id]/page.tsx`.

**Interfaz:** `FormularioRecordatorio({ datos, onChange, onSubmit, guardando, textoBoton, children? })`, donde `datos: DatosFormularioRecordatorio`, `onChange: (datos: DatosFormularioRecordatorio) => void` y `children` es el lugar donde `nuevo` pone el `SelectorInstanciaRecordatorio` (la edición no lo muestra: la instancia no cambia).

- [ ] Test en `lib/recordatorios.test.mjs`: `"editar un recordatorio recurrente sin límite exige elegir finalización"` (documenta el caso F3 con `crearPayloadRecordatorio`).
- [ ] Extraer el formulario de `nuevo` sin cambios visuales y usarlo en la edición, que ahora muestra frecuencia y finalización.
- [ ] Verificación + Playwright: crear y editar mandan el mismo payload que antes, y la edición de uno recurrente permite cambiar el límite.
- [ ] Commit `refactor(recordatorios): formulario compartido entre alta y edición` + registro.

### Tarea 9 (opcional, decidir al final): Google Calendar

`lib/calendario-google.ts` tiene su propio `solicitarCalendar` (204 → `null` y `codigo` de error). Pasarlo a `solicitarJson` exigiría agregar `codigo` a `ErrorApi`. Se decide después de la Tarea 8 según el tiempo disponible; si no se hace, se documenta como excepción.

---

## Registro de decisiones (para la defensa)

Al cerrar cada tarea se agrega una entrada en `registro-decisiones.md` con:

1. **Qué cambió** (archivos y commit).
2. **Antes / después** (fragmento corto).
3. **Patrón que aplica** y su equivalente en el backend.
4. **Por qué es mejor** (mantenimiento, tests, seguridad o rendimiento, con evidencia: llamadas medidas, tests).
5. **Cómo defenderlo en 30 segundos** (respuesta directa → concepto → decisión SIENEP → evidencia → límite).
6. **Preguntas probables del docente** y su respuesta corta.

Al terminar, ese registro es la base para crear la skill de estudio de la reestructura.
