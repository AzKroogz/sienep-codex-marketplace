# Banco 3: recordatorios, Calendar, auditoría, administración y reportes

Rutas del back relativas a `src/main/java/com/sienep/pdi_sienep3/`.

## R1. ¿Cómo funciona la recurrencia de un recordatorio?

**Respuesta:**
- Un recordatorio puede tener una frecuencia: diaria, semanal o mensual (`idFrecuencia` 1 a 3).
- Si la tiene, hay que elegir **una** forma de terminar:
  - por cantidad de repeticiones (`recurrencia`, entre 1 y 365);
  - o por fecha de fin.
- El servicio valida que no vengan las dos ni ninguna, y que la fecha de fin no sea anterior al inicio. Cualquier error da 400.

**En el código:** `service/RecordatorioService.java` → `validarYCalcularRecurrencia()`.

**Repreguntas:**
- ¿Qué pasa si manda la recurrencia y la fecha de fin a la vez? 400, con "No se puede usar recurrencia y fecha fin al mismo tiempo".
- ¿Se crean N filas, una por repetición? No: es un solo recordatorio con su regla, y en Google se traduce a RRULE.

## R2. ¿Cómo se traduce la recurrencia a Google Calendar?

**Respuesta:**
- Se arma una regla RFC 5545: `RRULE:FREQ=DAILY|WEEKLY|MONTHLY`.
- Se le agrega `;COUNT=n` si termina por cantidad, o `;UNTIL=…Z` si termina por fecha (fin del día de Montevideo, pasado a UTC).

**En el código:** `service/CalendarioGoogleService.java` → `construirReglasRecurrencia()` y `obtenerFrecuenciaGoogle()`.

## R3. ¿Cómo llega la notificación del recordatorio (RF23)?

**Respuesta:**
- Al apretar "Agregar a Calendar", el back crea el evento en el calendario del usuario conectado, con `sendUpdates=all`.
- Google manda la invitación por correo a los participantes de la instancia, con el asunto "Recordatorio de seguimiento – <estudiante>".
- El evento tiene avisos propios: correo 60 minutos antes y en pantalla 10 minutos antes.
- El resultado queda en la auditoría como `NOTIFICACION_RECORDATORIO`, con `OK` o `ERROR`.

**En el código:** `service/CalendarioGoogleService.java` → `crearEventoDesdeRecordatorio()` (los `reminders` con `overrides` y `construirInvitados()`).

**Límites (RF22 y RF23):**
- Es manual, con un botón, no automático al crear el recordatorio.
- No hay WhatsApp; la letra lo condiciona a que esté habilitado.
- "Éxito" quiere decir que Google aceptó el evento, no que el correo llegó a la bandeja.
- Si el único invitado es el propio organizador, Google no manda invitación.

## R4. Si el envío a Google falla, ¿por qué la auditoría no se pierde con el rollback?

**Respuesta:**
- El error se registra con `registrarEnTransaccionPropia()`, que tiene `@Transactional(propagation = REQUIRES_NEW)`: abre una transacción nueva e independiente.
- Si la operación principal se revierte, el registro del fallo queda guardado igual.

**En el código:** `service/AuditoriaService.java` → `registrarEnTransaccionPropia()`, llamado desde `CalendarioGoogleService.crearEventoDesdeRecordatorio()`.

**Repregunta:** ¿qué es la propagación? Cómo se comporta un método transaccional cuando ya hay una transacción abierta. `REQUIRED`, el valor por defecto, se une a la existente; `REQUIRES_NEW` suspende la actual y abre otra.

**Trampa:** decir que "todo lo que está en un `@Transactional` se guarda aunque falle".

## R5. ¿Cómo se conecta un usuario a Google Calendar y dónde quedan sus tokens?

**Respuesta:**
- Cada usuario da su consentimiento OAuth, separado del login.
- El back intercambia el código por los tokens y los guarda **cifrados** con `GoogleCalendarTokenCipher`, usando una clave de entorno.
- Si el token vence o lo revocan, responde 409 (`GOOGLE_CALENDAR_RECONECTAR`) y el front pide reconectar.

**En el código:** `service/GoogleCalendarOAuthService.java`, `security/GoogleCalendarTokenCipher.java` (`cifrar` y `descifrar`) y `exception/GoogleCalendarReconexionException`. La migración es `20261008_google_calendar_oauth.sql`.

**Repregunta:** ¿por qué cifrar el token y hashear la contraseña? Porque el token se tiene que poder leer para usarlo contra Google (cifrado reversible), y la contraseña solo se compara (hash).

## R6. ¿Cómo se crea una instancia desde un recordatorio (RF27) y cómo se sabe que está cumplido?

**Respuesta:**
- Se toma el estudiante de la instancia original del recordatorio y se crea una instancia común nueva, guardando de qué recordatorio vino.
- Un recordatorio figura como "Cumplido" si existe una instancia con ese origen.

**En el código:** `service/RecordatorioService.java` → `crearInstanciaDesdeRecordatorio()` (llama a `instanciaService.crearInstanciaComun(dto, idRecordatorio)`) e `idsCumplidos()`. La migración es `20261009_instancia_recordatorio_origen.sql`.

**Repregunta:** ¿qué pasa si el recordatorio o la instancia original están dados de baja? 404, con "No existe un recordatorio activo…".

## R7. ¿Qué guarda la auditoría y cómo se ven los cambios?

**Respuesta:**
- Cada registro tiene la acción, el tipo de evento, la entidad, la descripción, el resultado, el usuario y la fecha y hora.
- En las modificaciones guarda además `cambios`, en una columna **JSONB**, con el valor anterior y el nuevo de cada campo. Así se puede reconstruir qué pasó.
- No guarda contraseñas, datos médicos ni comentarios confidenciales.

**En el código:** `model/Auditoria.java` (`@JdbcTypeCode(SqlTypes.JSON)` en `cambios`) y `service/AuditoriaService.java` (`registrar()` y `registrarCambio()`). La migración es `20261102_auditorias_cambios_jsonb.sql`.

**Repregunta:** ¿por qué JSONB y no una columna por campo? Cada entidad cambia campos distintos; JSONB guarda un mapa flexible.

## R8. ¿Cómo funcionan los roles y los permisos? ¿Qué impide que un admin se bloquee?

**Respuesta:**
- Rol y Permiso están en una relación muchos a muchos.
- Hay roles base (Administrador, Psicopedagogo, Tutor, Docente, Legales…) y se pueden crear roles personalizados eligiendo permisos.
- Al modificar un rol, si es **el propio rol** de quien edita y le quita los permisos de gestión de roles, se rechaza con "No podés quitarle a tu propio rol los permisos para gestionar roles".

**En el código:** `service/RolService.java` → `validarNoPierdeGestionDeRoles()` y `crearOActualizarRolBase()` (los roles base).

**Límites (RF33, RF32 y RF34):**
- La carga de los roles base se hace por un endpoint y no registra auditoría.
- No hay restricción de roles por carrera.

## R9. ¿Por qué no se puede dar de baja una categoría de instancia en uso?

**Respuesta:**
- Si hay instancias **activas y futuras** con esa categoría, la baja se rechaza con 400: "No se puede dar de baja la categoria porque tiene instancias futuras activas".
- Las instancias pasadas no bloquean, porque el historial conserva la categoría aunque esté dada de baja.

**En el código:** `service/CategoriaService.java`, en la baja: `comunRepository.existsByCategoriaIdCategoriaAndInstanciaEstadoTrueAndInstanciaFechaHoraAfter(...)`.

**Repregunta:** ¿cómo hace la consulta sin escribir SQL? Es un *derived query* de Spring Data: el nombre del método define el `where`.

## R10. ¿En qué se diferencian las categorías de recordatorio de las de instancia?

**Respuesta:**
- Son catálogos separados, cada uno con su ABM y su baja lógica (RF35-37 y RF38-40).
- El tipo del recordatorio sale del catálogo de categorías de recordatorio.

**En el código:** `service/CategoriaRecordatorioService.java` y `controller/CategoriaRecordatorioController.java`. La migración es `20261101_categorias_recordatorio.sql`, con su rollback.

## R11. ¿Cómo se genera el reporte de seguimiento y la exportación?

**Respuesta:**
- `generarSeguimientoGrupal()` toma la carrera, el grupo y el período, y cuenta por estudiante sus instancias, incidencias y recordatorios activos, con una fila de totales.
- `generarCsvSeguimientoGrupal()` arma el CSV que descarga el front.
- Por estudiante también hay un PDF con OpenPDF (`ReportePdfService`), pero solo desde la API.

**En el código:** `service/ReporteService.java`, `service/ReportePdfService.java` y `controller/ReporteController.java`.

**Límites (RF31):**
- No hay Excel `.xlsx` ni un PDF grupal; el CSV abre en Excel.
- Un período sin datos devuelve los estudiantes con ceros.
- Looker es para el análisis histórico, sobre el data warehouse.

**Repregunta:** ¿el reporte respeta permisos? Sí: el endpoint tiene su `@PreAuthorize` y no devuelve datos sensibles.
