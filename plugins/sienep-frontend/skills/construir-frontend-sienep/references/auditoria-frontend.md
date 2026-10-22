# Auditoría del frontend SIENEP — 21/10/2026

**Alcance:** `~/IdeaProjects/pdi_sienep/frontend/sienep-frontend`, rama `style/estudiantes-editar` (último commit `daa2618`). Auditoría en solo lectura: no se modificó código.

**Método:**
- Lectura completa de los 61 archivos fuente versionados (unas 8.100 líneas).
- `eslint`, `tsc --noEmit`, `npm test` y `npm run build`.
- Medición de llamadas por pantalla con Playwright en build de producción (`next start`) y en `next dev`, con la API **simulada** (`page.route('**/api/**')`, token falso). No se tocó Railway ni se usaron credenciales.

**Convención:** *observado* = visto en el código o medido; *inferido* = deducido leyendo el código, pendiente de probar contra la API real.

---

## 1. Tecnologías

| Capa | Tecnología | Uso |
|---|---|---|
| Framework | Next.js 16.3.5, App Router | Rutas en `app/`; grupo `(protected)` con `AuthGuard` |
| UI | React 19.2.8 | Todas las páginas son `"use client"`: SPA en navegador, sin Server Components ni Server Actions |
| Lenguaje | TypeScript 5.9, `strict` | Alias `@/*` |
| Estilos | Tailwind CSS 4.3 (PostCSS) + clases propias en `app/globals.css` | |
| Calidad | ESLint 9 + `eslint-config-next` (core-web-vitals, typescript) | |
| Tests | `node --test` (Node 24) | Solo funciones de `lib/` |
| Datos | `fetch` nativo | Sin axios/SWR/React Query; sin caché |
| Sesión | JWT en `localStorage` | Login propio + Google OAuth del backend |

No hay estado global, librería de formularios, de componentes ni de validación.

## 2. Estado de las herramientas (observado)

| Verificación | Resultado |
|---|---|
| `eslint .` | 0 errores, 0 advertencias |
| `tsc --noEmit` | 0 errores |
| `npm test` | 61/61 OK |
| `npm run build` | OK. 16 rutas. Advierte un `package-lock.json` suelto en `frontend/` (fuera del repo) |

Límite: los tests cubren solo `lib/`. No hay pruebas de componentes ni de flujo completo.

## 3. Llamadas a la API por pantalla (medido)

| Pantalla | Producción | Dev | Llamadas en producción |
|---|---:|---:|---|
| `/dashboard` | 2 | 4 | instancias/mias/proximas, recordatorios/mios/proximos |
| `/estudiantes` | 1 | 2 | estudiantes/buscar |
| `/estudiantes/1` (ficha) | 2 | 4 | estudiantes/1, informes-medicos-adjuntos |
| `/estudiantes/1/editar` | **6** | **12** | estudiantes/1, direccion, carreras, telefonos, grupos, datos-sensibles |
| `/estudiantes/1/instancias` | 2 | 4 | estudiantes/1, instancias?idEstudiante |
| `/estudiantes/1/instancias/nueva` | 2 | 4 | estudiantes/1, categorias |
| `/recordatorios` | **4** | 7 | vencidos, hoy, proximos, calendario/pendientes |
| `/recordatorios/1` | 3 | 6 | recordatorios/1, evento, estado (en serie) |
| `/recordatorios/nuevo` | 1 | 2 | **GET /api/estudiantes (lista completa)** |
| `/configuracion/usuarios` | 1 | 2 | funcionarios |
| `/configuracion/usuarios/nuevo` | 2 | 4 | sedes, roles |
| `/configuracion/usuarios/1/editar` | 3 | 6 | funcionarios/1, sedes, roles |

Navegación interna ficha → editar → cancelar: 2 + 6 + 2 = **10 llamadas**. `GET /api/estudiantes/1` se pide 3 veces.

**Conclusión 1 (observada):** gran parte de las "demasiadas llamadas" que se ven en DevTools durante el desarrollo es **React Strict Mode**, que en `next dev` monta cada efecto dos veces. En producción no hay duplicados. La única pantalla con protección es `GoogleCalendarPendientes`: por eso `/recordatorios` da 7 y no 8.

**Conclusión 2 (observada):** aun en producción hay llamadas que se pueden reducir:

1. **Editar estudiante: 6 llamadas en 3 tandas** (`editar/page.tsx:122-215`). Primero 4 en paralelo, después `grupos`, después `datos-sensibles`. Esta última no depende de nada y podría ir en el primer `Promise.all`; `grupos` sí depende de `idCarrera`.
2. **`GET /api/estudiantes/{id}` en 4 pantallas** (ficha, editar, instancias, nueva) sin ningún caché: cada navegación vuelve a pedirlo.
3. **Selector de recordatorio con lista completa sin paginar** (`lib/recordatorios.ts:29`). Es la llamada que más crece con los datos y ya existe `/api/estudiantes/buscar` paginado.
4. **Recordatorios: 3 llamadas por estado** + deduplicación en el front (`lib/recordatorios.ts:395`). El backend devuelve los mismos recordatorios en dos listas; un solo endpoint agrupado lo resolvería.
5. **Calendar en el detalle: 2 llamadas en serie** (evento → estado), repetidas en cada guardado porque el componente se remonta con `key={...revisionCalendar}` (`recordatorios/[id]/page.tsx:79`).
6. **Datos que casi no cambian se piden de nuevo**: categorías (cada vez que se abre el formulario en `CrearInstanciaDesdeRecordatorio.tsx:52`), sedes y roles (nuevo y editar usuario).

**Sobre "API expuesta en el código":** `NEXT_PUBLIC_API_URL` queda dentro del JavaScript del navegador. Es inevitable en una SPA que llama directo a la API y **no es una vulnerabilidad**: la protección es JWT + `@PreAuthorize` en el backend. El problema real es de mantenimiento: las rutas `/api/...` están escritas a mano en unos 20 archivos.

## 4. Reutilización y arquitectura (observado)

**Bien reutilizado:**
- `lib/recordatorios.ts`, `lib/calendario-google.ts`, `lib/instancias.ts`, `lib/informes-medicos.ts`, `lib/estudiante-form.ts`, `lib/instancia-payload.ts`, `lib/telefonos.ts`: lógica pura separada de la UI, con tests.
- `FormularioRegistroComun` se usa desde la ficha y desde un recordatorio.
- `Sidebar` (`EnlaceMenu`, `OpcionPronto`, el mismo `Menu` para celular y escritorio).
- `FiltrosEstudiantes` y `ListaEstudiantes` reciben todo por props; la página solo orquesta.

**Duplicado o inconsistente:**

| Hallazgo | Evidencia |
|---|---|
| 3 clientes HTTP con la misma función | `solicitarJson` (`lib/recordatorios.ts:91`), otro `solicitarJson` (`lib/instancias.ts:45`), `solicitarCalendar` (`lib/calendario-google.ts:24`) y el `consultar` del dashboard (`dashboard/page.tsx:16`) |
| 3 clases de error equivalentes | `ErrorApiRecordatorio`, `ErrorApi`, `ErrorApiGoogleCalendar`; `obtenerMensajeError` copiado 2 veces y una tercera variante dentro de `AdjuntarInformeMedico` |
| 37 `fetch` crudos en páginas y componentes | 10 en `estudiantes/[id]/editar/page.tsx` |
| 43 copias del manejo de 401 | `localStorage.removeItem("token"); router.replace("/")` en todo `app/` y `components/` |
| Logout duplicado | `AppHeader.tsx:17` y `AuthGuard.tsx:36` |
| Chequeo de sesión repetido | `AuthGuard` ya protege el layout, pero casi todas las páginas repiten `if (!token) router.replace("/")`; `recordatorios/nuevo` tiene su propio "Verificando sesión..." |
| Tipo `Estudiante` redefinido 4 veces | Ficha, editar, instancias y nueva; existe `types/estudiante.ts` incompleto |
| Tipo duplicado y divergente | `InstanciaDesdeRecordatorioRequest` en `lib/instancias.ts:156` (`comentariaConfidencial`, `idUsuariosParticipante`) contra `types/instancia.ts:43` (`comentarioConfidencial`, `idsUsuariosParticipantes`). Se usa el de `types/`; el de `lib/` es código muerto con errores de tipeo |
| `API_URL` llega de dos formas | Parámetro en recordatorios y calendar; import en instancias |
| Estilos repetidos | Constantes de clases solo en editar estudiante; el resto repite cadenas Tailwind |

## 5. Problemas funcionales (prioridad 1)

| # | Hallazgo | Tipo | Dónde |
|---|---|---|---|
| F1 | **El registro común pedía "ID del funcionario" a mano.** *Corregido el 21/10:* el backend (`InstanciaService`, commit `ea1344c` en develop) ya ignora ese valor al crear y asigna el funcionario autenticado, así que no era un agujero de seguridad sino un campo obligatorio inútil. Se quitó del front en la rama `fix/instancia-sin-id-funcionario`. Queda en el backend: `actualizarInstancia` (PUT) todavía toma `idFuncionario` del request (`InstanciaService.java:352-359`); hoy no hay pantalla que lo use | Observado | `FormularioRegistroComun.tsx` |
| F2 | **Expirar la sesión no limpia `sessionStorage`**: las 43 copias del 401 no usan `limpiarSesion()`. Quedan los filtros de búsqueda y los avisos del usuario anterior. Contradice RF04 ("limpiar temporales") | Observado | ver §4 |
| F3 | **Editar recordatorio no permite cambiar recurrencia ni instancia**, aunque el payload las reenvía. Si un recordatorio tiene frecuencia pero ni cantidad ni fecha fin, `crearPayloadRecordatorio` lanza "Debe seleccionar cómo finaliza la recurrencia" y no hay campo para corregirlo | Inferido | `recordatorios/[id]/page.tsx:127-148`, `lib/recordatorios.ts:165` |
| F4 | Frecuencias `1/2/3` escritas a mano en el front: dependen de los IDs de la BD | Observado | `lib/recordatorios.ts:156`, `recordatorios/nuevo/page.tsx` |
| F5 | El tipo de recordatorio es texto libre (RF21 y RF38-40 piden catálogo) | Observado | `recordatorios/nuevo/page.tsx` |
| F6 | El detalle de recordatorio muestra "Instancia relacionada: 1" (el ID, no el título ni el código) | Observado | `recordatorios/[id]/page.tsx` |
| F7 | La ficha muestra el bloque de informes médicos a todos; sin permiso aparece un error rojo y el botón "Adjuntar" igual | Observado | `ListaInformesMedicos.tsx`, ficha |
| F8 | La ficha no distingue 403 al cargar el estudiante (mensaje genérico); el resto de las pantallas sí | Observado | `estudiantes/[id]/page.tsx:50` |
| F9 | El login lee `respuesta.json()` antes de mirar `ok`: si Railway responde con HTML (502), se muestra "No se pudo conectar al servidor" | Observado | `app/page.tsx:31` |
| F10 | `AuthGuard` solo comprueba que haya un token, no si venció; el comentario de 15 min dice "temporal para pruebas", pero RF04 exige justamente 15 min | Observado | `AuthGuard.tsx:10` |

## 6. Responsive y presentación (prioridades 2 y 3)

- **Pantallas sin estilos** (0-3 `className`): recordatorios (listado, detalle, nuevo), instancias (listado y nueva), `FormularioIncidencia`, `FormularioRegistroComun`, `ListaRecordatorios`, `CrearInstanciaDesdeRecordatorio`. Contrastan con estudiantes, que ya tiene tarjetas y grilla responsive.
- Usuarios (`p-4`, `text-xl`) sigue otro patrón visual que estudiantes (`max-w-6xl`, `text-2xl`).
- Se mezclan Tailwind y clases propias en `globals.css` (`.adjuntar-informe-medico`, `.selector-archivo-oculto`).
- **Modo oscuro (inferido):** `globals.css` pone el `body` oscuro con `prefers-color-scheme: dark`, pero los componentes usan `bg-white` y `text-slate-*` fijos. En las pantallas sin fondo propio quedaría texto oscuro sobre fondo negro. Falta verificarlo en el navegador.
- `app/layout.tsx` sigue con la plantilla: `lang="en"` y título "Create Next App" (se ve en la pestaña: confirmado con Playwright).

## 7. Seguridad (observado)

- **Bien:** validación de la URL de autorización de Google (`https`, host `accounts.google.com`, sin usuario ni contraseña) y del `htmlLink` del evento; no hay `dangerouslySetInnerHTML`, `innerHTML` ni `eval`; el token de Google llega en el hash (no viaja al servidor) y se reemplaza el historial.
- **Límites para la defensa:** el JWT en `localStorage` es accesible por XSS; `AuthGuard` no valida la vigencia del token; los permisos en el front son cosméticos y la protección real está en el backend.
- 27 `console.error` dejan detalles de errores en la consola del navegador; no se vio que impriman datos sensibles.

## 8. Cobertura de RF desde el frontend

Base: recuento del 19/10 (11 listos de 40) y el plan de trazabilidad del 12/10, contrastada con el código actual.

- **Con pantalla:** RF01, RF04 (login, logout, inactividad); RF06-RF09 (ficha, baja/alta, editar, búsqueda, informes); RF10/RF18/RF28 (alta común e incidencia desde la ficha); RF19, RF20, RF22, RF25-RF27 (recordatorios y Calendar); RF03 parcial (usuarios).
- **Sin pantalla:** RF05 (alta de estudiante), RF11 (reclasificación), RF16-RF17 (gestión global y clonar instancias; el menú dice "pronto"), RF29 (historial combinado), RF30-RF31 (reportes), RF32-RF34 (roles), RF35-RF40 (categorías).

## 9. Recomendación (ordenada según las prioridades del proyecto)

Sin agregar librerías y manteniendo el estilo simple:

1. **F1 y F2 primero** (funcionales y de auditoría): sacar el ID de funcionario del formulario (coordinar con el backend) y usar `limpiarSesion()` en todos los 401.
2. **Un único `pedirApi(ruta, opciones)` en `lib/api.ts`**: pone el token, ante un 401 hace `limpiarSesion()` y redirige, y lanza un solo `ErrorApi`. Reemplaza los 3 clientes, las 43 copias y el `consultar` del dashboard. Migrar de a una pantalla por rama, con tests.
3. Reducir llamadas reales: `datos-sensibles` en el `Promise.all` inicial; selector de recordatorio con `/buscar`; evaluar un endpoint agrupado de recordatorios en el backend.
4. Borrar el tipo duplicado de `lib/instancias.ts` y completar `types/estudiante.ts`.
5. Después, estilos de recordatorios e instancias, `lang="es"`, título y modo oscuro.
6. No vale la pena "arreglar" el doble montaje de Strict Mode: solo pasa en desarrollo. Basta con documentarlo.

## 10. Límites de esta auditoría

- La medición usó una API simulada: no mide latencia ni tamaño de respuestas de Railway, ni el comportamiento con permisos reales (403).
- F3 y el modo oscuro son inferencias pendientes de probar.
- No se auditó el backend ni la correspondencia exacta de DTOs con el OpenAPI desplegado.
