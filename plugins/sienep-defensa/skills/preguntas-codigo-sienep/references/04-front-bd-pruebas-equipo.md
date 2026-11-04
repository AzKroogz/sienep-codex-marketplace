# Banco 4: frontend, base de datos, pruebas, despliegue y equipo

Rutas del front relativas a `~/IdeaProjects/pdi_sienep/frontend/sienep-frontend`.

## F1. ¿Cómo está organizado el frontend?

**Respuesta:**
- Next.js 16 con App Router, React 19, TypeScript estricto y Tailwind 4.
- Cada pantalla es una página en `app/` que maneja el estado, la navegación y los errores.
- Para hablar con la API llama a una función de `lib/<modulo>.ts`, una por endpoint.
- Esa función usa `solicitarJson()`, que agrega el token y convierte cualquier error en `ErrorApi`.
- La página nunca llama a `fetch` directamente.

**En el código:** `lib/solicitud.ts` (`solicitarJson`, `crearOpcionesAutenticadas`, `ErrorApi`). Por ejemplo, `lib/estudiantes.ts` y `app/(protected)/estudiantes/page.tsx`.

**Repregunta:** ¿por qué separar así? Hay un solo lugar que maneja el token y los errores, las páginas son más cortas y los servicios se prueban solos, con un `fetch` falso. Es el equivalente del controller → service del back.

## F2. ¿Qué hace el front ante un 401 y ante un 403?

**Respuesta:**
- **401** (sesión inválida o vencida): `limpiarSesion()`, que vacía el `sessionStorage`, y redirige al login.
- **403**: muestra "No tenés permisos para …" y la persona sigue en la pantalla.

**En el código:** se repite en las páginas, en los `.catch` con `error instanceof ErrorApi && error.status === 401`. `limpiarSesion` está en `lib/api.ts`.

## F3. ¿Cómo protege las rutas el front y cómo se cierra la sesión por inactividad?

**Respuesta:**
- `AuthGuard` envuelve las páginas de `(protected)`:
  - si no hay token, manda al login;
  - consulta `/api/auth/me` y, si la cuenta debe cambiar la contraseña, manda a `/cambiar-contrasena`;
  - guarda los permisos.
- Escucha la actividad del usuario y, a los 15 minutos sin uso, llama al logout del back y limpia la sesión.

**En el código:** `components/AuthGuard.tsx` (`TIEMPO_INACTIVIDAD = 15 * 60 * 1000` y `cerrarSesionPorInactividad`).

**Ojo, si lo leen:** la constante tiene el comentario `// temporal para pruebas`. Si preguntan, el valor de 15 minutos es el definido; el comentario quedó de una etapa anterior.

**Trampa:** "el front protege los datos". El front solo decide qué mostrar; la protección real son el JWT y `@PreAuthorize` del back.

## F4. ¿Dónde guardan el token y por qué?

**Respuesta:**
- En `sessionStorage`, a través de `lib/api.ts` (`guardarToken`, `obtenerToken` y `limpiarSesion`).
- Se borra al cerrar la pestaña.

**Límite:** al ser accesible desde JavaScript, un ataque XSS podría leerlo. La alternativa sería una cookie `HttpOnly`, que requiere cambiar el back y el CORS.

## F5. ¿Cómo se marca la opción activa del menú? (Hallazgo 1 de la prueba de usabilidad)

**Respuesta:**
- Antes se comparaba solo el comienzo de la ruta, así que `/configuracion/categorias` también marcaba en `/configuracion/categorias-recordatorio`.
- Ahora se compara la ruta exacta o la ruta seguida de `/`.
- Se usa `aria-current="page"` para los lectores de pantalla.

**En el código:** `components/Sidebar.tsx`, con `activo = rutaActual === href || rutaActual.startsWith(\`${href}/\`)`.

## F6. ¿Qué heurísticas de Nielsen aplicaron? Muéstrenlas.

**Respuesta:** cuatro.
1. **Consistencia y estándares:** todas las listas tienen el formato de Usuarios.
2. **Prevención y manejo de errores:** confirmación antes de crear y de dar de baja, y mensajes claros del back.
3. **Feedback inmediato:** "Guardando…", avisos verdes, contadores, pestañas con cantidades y una sola opción marcada en el menú.
4. **Reconocimiento antes que recuerdo:** el grupo depende de la carrera, hay listas para elegir y los filtros tienen ejemplos.

**Evidencia:** el guion `~/Escritorio/guion-demostracion-heuristicas-nielsen.md` y el documento UX.

## B1. ¿Qué hace `ddl-auto=validate` y cómo cambiaron la base entonces?

**Respuesta:**
- Al arrancar, Hibernate **compara** las entidades con las tablas. Si algo no coincide, la aplicación no levanta. Nunca crea ni modifica tablas.
- Cada cambio se hizo con un script SQL versionado en `db/migrations/AAAAMMDD_*.sql`, con su `_rollback.sql`, y se aplicó en Railway antes de desplegar.

**En el código:** `src/main/resources/application.properties` y `db/migrations/` en el repo del back.

**Repregunta:** ¿por qué no `update`? `update` cambia el esquema sin control ni reversión, y la letra lo considera un incumplimiento grave.

**Trampa:** "validate crea las tablas que faltan".

## B2. ¿Cómo manejan la zona horaria? (La dificultad principal)

**Respuesta:**
- El servidor y Google interpretaban la hora distinto, y un recordatorio quedaba corrido 3 horas.
- Se unificó todo en `America/Montevideo`:
  - en Hibernate (`jdbc.time_zone`) y Jackson;
  - con una clase `FechaHoraSienep`;
  - el front manda la hora local, sin convertirla a UTC.
- Google recibe la fecha con `timeZone` explícito.

**En el código:** `config/FechaHoraSienep.java`, `application.properties` y `lib/recordatorios.ts` en el front (`formatearHoraLocal`).

**Límite:** los recordatorios creados antes del 2/11 y la auditoría vieja quedaron con 3 horas de diferencia.

## B3. ¿Qué tests tienen y de qué tipo?

**Respuesta:**
- **Back: 279 pruebas, 0 fallos.**
  - Tests de servicio con Mockito (`@Mock`, `@InjectMocks`), por ejemplo `AuthServiceTest` y `EstudianteServiceTest`.
  - Tests de controller y seguridad con `@WebMvcTest` y `@MockitoBean`, por ejemplo `LogoutInvalidacionTokenTest`, `CambioContrasenaObligatorioTest` y `*ControllerSecurityTest`.
  - Tests de repositorio con `@DataJpaTest`, por ejemplo `EstudianteSpecificationTest`.
- **Front: 148 pruebas** con `node --test`, sobre `lib/`, con un `fetch` falso.

**En el código:** `src/test/java/...` en el back y `lib/*.test.mjs` en el front.

**Repreguntas:**
- ¿Qué diferencia hay entre un mock y la base real? El mock simula al colaborador para probar solo la lógica del servicio.
- Den un test negativo: `logoutSinToken_deberiaRetornar401_yNoInvalidarNada`.

## B4. ¿Cómo se despliega y cómo se levanta en local?

**Respuesta:**
- El back está en Railway, que despliega desde GitHub `develop`, con PostgreSQL y el bucket S3 de Railway.
- El front se muestra en local con `npm run build` y `npx next start`, contra el back de Railway.
- Las variables (`JWT_SECRET`, base de datos, Google, bucket) son de entorno y nunca están en el repo.
- Los README explican cómo levantar cada parte.

**Repregunta:** ¿por qué GitHub si el oficial es GitLab? Railway se conecta a GitHub. GitHub es un espejo con el mismo contenido.

## B5. ¿Cómo trabajaron con Git?

**Respuesta:**
- GitLab institucional, con dos repos.
- Ramas:
  - `develop` para integración;
  - `pft-main` como producción, que tiene todo `develop`;
  - `main`, que queda del PDI;
  - una rama `feat/…` o `fix/…` por tarea, que entra por merge request.

**Límites:**
- Hubo un `push --force` puntual en una rama de MR (!45), para quitar archivos no deseados; no tocó `develop`.
- La historia de GitHub es distinta por los cherry-picks.

## Q1. ¿Qué hizo cada uno? *(No aceptar "todos hicimos de todo")*

**Guía para practicar:** cada integrante tiene que poder nombrar 2 o 3 cosas concretas que hizo, abrir el archivo y explicarlo. Usar `git log --author` para recordarlo. Como guía, Nicolás Ramírez hizo la prueba de usabilidad. El reparto exacto lo tiene que decir el equipo; no inventarlo.

## Q2. ¿Cuál fue la dificultad principal y cómo la resolvieron?

**Respuesta modelo:** la zona horaria (ver B2). Otras posibles:
- reconectar el bucket de los informes médicos cuando cambió;
- con `validate`, hacer cada cambio de la base a mano, con su script de reversión;
- mantener GitLab y GitHub con el mismo contenido.

## Q3. ¿Qué mejorarían si tuvieran más tiempo?

**Respuesta:**
- Un ID correlativo por año (RF14).
- Importación de estudiantes por CSV (RF05).
- Cifrar los datos de salud en la base (RNF01).
- Buscar instancias por nombre o cédula (RNF07).
- Exportar a Excel (RF31).
- Crear el evento de Calendar automáticamente (RF22).
- Un cuadro de confirmación propio.
- El token en una cookie `HttpOnly`.
- Repetir la prueba de usabilidad con usuarios reales.

## Q4. ¿Qué es lo que más les costó entender del código del otro, o del PDI heredado?

**Guía:** respuesta personal y honesta. Un ejemplo válido es entender el flujo del filtro JWT, o la relación Instancia–Común–Incidencia. Practicarla en voz alta.
