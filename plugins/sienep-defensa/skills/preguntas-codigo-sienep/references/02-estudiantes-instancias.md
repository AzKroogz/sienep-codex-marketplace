# Banco 2: estudiantes e instancias

Rutas del back relativas a `src/main/java/com/sienep/pdi_sienep3/`.

## E1. ¿Cómo validan la cédula uruguaya? ¿En qué capa?

**Respuesta:**
- En la capa de servicio, al crear la cuenta.
- Primero se normaliza la cédula, sacando puntos y guiones (`replaceAll("\\D", "")`).
- Después se valida el dígito verificador con la librería `ciuy` (`Validator.validateCi`).
- Si no es válida, se lanza `ValidacionNegocioException`, que da 400 con "La cédula uruguaya no es válida".
- Después se controla que no esté repetida (409).

**En el código:** `service/UsuarioService.java` → `crearUsuarioDesdeRegistro()` y `normalizarCedula()`. La dependencia `uy:ciuy` está en el `pom.xml`.

**Repreguntas:**
- ¿Por qué en el servicio y no en el DTO? Es una regla de negocio que se combina con otras: unicidad y edad.
- ¿Qué valida el DTO con `@Valid`? Formato y campos obligatorios.

**Prueba negativa:** la cédula `12345678` da 400. La `12345672` es válida.

**Trampa:** decir "lo valida el front". El front puede ayudar, pero la regla está en el back.

## E2. ¿Cómo controlan la edad mínima?

**Respuesta:**
- Con `Period.between(fechaNacimiento, LocalDate.now()).getYears() >= 18`, que cuenta años completos, no días divididos por 365.
- Si no llega a 18, devuelve 400 con "El usuario debe ser mayor de edad".

**En el código:** `service/UsuarioService.java` → `esMayorDeEdad()`.

**Prueba negativa:** con la fecha de nacimiento `2015-05-05`, da 400.

## E3. El alta de un estudiante guarda varias cosas. ¿Qué pasa si una falla?

**Respuesta:**
- `crearEstudiante()` es `@Transactional`. Dentro crea el usuario, la dirección, el estudiante y los teléfonos, y registra la auditoría.
- Si cualquier paso lanza una excepción (por ejemplo, una matrícula repetida o un grupo inexistente), se revierte todo: no queda un usuario sin estudiante.

**En el código:** `service/EstudianteService.java` → `crearEstudiante()`, que llama a `usuarioService.crearUsuarioDesdeRegistro()` dentro de la misma transacción.

**Repreguntas:**
- ¿Qué revierte exactamente? Las escrituras en la base hechas dentro de la transacción.
- ¿Y un archivo subido al bucket? Eso no lo revierte la transacción, porque es un sistema externo. Por eso la foto se sube aparte, con su propio endpoint.

**Trampa:** creer que `@Transactional` revierte llamadas externas, como S3 o Google.

## E4. ¿Cómo funciona la búsqueda de estudiantes con filtros?

**Respuesta:**
- Con el patrón **Specification** de Spring Data JPA.
- `EstudianteSpecification.conFiltros()` arma el `where` solo con los filtros que vienen cargados: nombre, cédula, carrera, grupo y estado. Si no viene el estado, toma "activos".
- El repositorio ejecuta `findAll(spec, pageable)`, que devuelve una página ordenada.

**En el código:** `specification/EstudianteSpecification.java` y `service/EstudianteService.java` → `buscarEstudiantes()`. La prueba es `repository/EstudianteSpecificationTest`.

**Repregunta:** ¿por qué no un método del repositorio por cada combinación de filtros? Con 5 filtros opcionales serían decenas de métodos; la Specification los combina.

**Límite:** la búsqueda no ignora tildes.

## E5. ¿Cómo hacen la baja lógica de un estudiante?

**Respuesta:**
- No se borra nada: se pone `estadoUsuario = false` en su usuario y se audita `BAJA_LOGICA_ESTUDIANTE`.
- El historial (instancias, informes y auditoría) queda intacto.
- La cuenta ya no puede entrar, porque el login y el filtro rechazan las cuentas inactivas.
- En la búsqueda se lo ve filtrando por estado "Inactivos".

**En el código:** `service/EstudianteService.java` → `bajaLogicaEstudiante()`.

**Repregunta:** ¿qué pasa si tiene instancias futuras? El front avisa antes de confirmar; el back no lo bloquea (es una limitación de RF06).

**Trampa:** decir "hacemos `delete` pero con cuidado". Es un `update` de estado.

## E6. ¿Cómo protegen los datos sensibles del estudiante?

**Respuesta:** en tres niveles:
1. **Endpoint:** los datos sensibles tienen endpoints propios, con permisos específicos (`VER_DATOS_SENSIBLES_ESTUDIANTE` y `MODIFICAR_DATOS_SENSIBLES_ESTUDIANTE`).
2. **Servicio:** al crear, `descartarDatosSensiblesSinPermiso()` anula la salud, el motivo de derivación, las observaciones confidenciales y la foto si quien crea no tiene permiso. Así no se cuelan por el alta.
3. **DTO:** el listado usa un DTO sin esos campos.

**En el código:** `controller/EstudianteController.java` (los `@PreAuthorize` de `obtenerDatosSensibles` y `modificarDatosSensibles`) y `service/EstudianteService.java` → `descartarDatosSensiblesSinPermiso()`. La prueba es `EstudianteDatosSensiblesControllerTest`.

**Límite (RNF01):** en la base no están cifrados. Se protegen con permisos, HTTPS y el acceso a la base.

## E7. ¿Cómo guardan los informes médicos y la foto?

**Respuesta:**
- No van en la base: van a un bucket S3 de Railway (`AlmacenamientoArchivoService`). La base guarda solo la clave del archivo.
- Validaciones:
  - informes: PDF, JPG o PNG de hasta 10 MB (`multipart.max-file-size`); si se pasa, responde 413;
  - foto: JPG o PNG de hasta 5 MB.
- Para descargar, el back genera una **URL prefirmada** que vence a los 60 segundos.

**En el código:** `service/AlmacenamientoArchivoService.java` (`subirFotoEstudiante`, `S3Presigner` con `signatureDuration(Duration.ofSeconds(60))`) y `service/InformeMedicoAdjuntoService.java`.

**Repregunta:** ¿por qué una URL que vence? Si alguien copia el enlace, al rato no sirve; el permiso se controla cada vez que se pide uno nuevo.

**Límite:** 5 informes viejos se dieron de baja porque apuntaban a un bucket anterior.

## E8. ¿Qué es una instancia y cómo se modela común contra incidencia?

**Respuesta:**
- Una instancia es un registro de seguimiento del estudiante: una reunión, una llamada o un informe.
- La tabla `instancia` tiene los datos comunes: título, fecha, estudiante, funcionario, comentario, comentario confidencial, código y estado.
- Cada instancia tiene un detalle en otra tabla:
  - `Comun`: canal, categoría y participantes;
  - `Incidencia`: lugar e involucrados, que pueden no ser usuarios del sistema.

**En el código:** `model/Instancia`, `model/Comun` y `model/Incidencia`. En `service/InstanciaService.java`, `crearInstanciaComun()` y `crearInstanciaIncidencia()`.

**Repregunta:** ¿cómo saben de qué tipo es? Se busca si existe un `Comun` o una `Incidencia` para ese id, como hace `clonarInstancia`.

## E9. ¿Cómo se genera el código único de una instancia? ¿Por qué no es correlativo?

**Respuesta:**
- `generarCodigoInstancia()` arma `INST-` más la fecha y hora en milisegundos, en la zona de Montevideo.
- Para que dos instancias creadas en el mismo milisegundo no repitan, usa un `AtomicLong` que siempre avanza al menos 1.
- Además, la columna tiene una restricción UNIQUE.

**En el código:** `service/InstanciaService.java` → `generarCodigoInstancia()` (`ultimaMarcaCodigo.updateAndGet(...)`).

**Límite (RF14):** la ficha pide `INST-AAAA-NNNNNN`, correlativo por año, y el nuestro no lo es. Propuesta: una tabla `secuencias_instancia(anio, ultimo)`, actualizada con un bloqueo de fila.

**Repregunta:** ¿y si hubiera dos servidores? El `AtomicLong` es por proceso; en ese caso la restricción UNIQUE frena el duplicado (409). Con la tabla de secuencias se resolvería del todo.

## E10. ¿Cómo funciona la clonación?

**Respuesta:**
- Crea una instancia nueva con los datos de la original, una fecha nueva elegida por el usuario y un código nuevo.
- Copia el detalle (común con sus participantes, o incidencia).
- Le pone el título "… (clonado N)", numerado para ese estudiante y sin pasar los 50 caracteres.
- Todo en una transacción, y se audita `CLONACION_INSTANCIA`.

**En el código:** `service/InstanciaService.java` → `clonarInstancia()`, `generarTituloClonado()` y `clonarParticipantes()`.

**Límite (RF11):** la clonación copia la categoría aunque esté inactiva. El alta y la edición, en cambio, la rechazan.

## E11. ¿Cómo evitan que se use una categoría dada de baja?

**Respuesta:**
- Al crear o editar, `obtenerCategoriaActiva()` lanza 400 con "La categoria seleccionada no esta activa".
- El front solo ofrece categorías activas y obliga a cambiarla si la instancia tenía una inactiva.

**En el código:** `service/InstanciaService.java` → `obtenerCategoriaActiva()`.

## E12. ¿Cómo respeta la visualización el rol (RF12)? Por ejemplo, con Legales.

**Respuesta:**
- El comentario confidencial solo lo ve y lo escribe quien tiene `VER_INSTANCIA_CONFIDENCIAL`. Si no lo tiene, el servicio lo anula antes de responder o de guardar.
- Legales tiene permiso para ver lo confidencial, pero no para editar ni dar de baja: el front no muestra esos botones y, por API, responde 403.

**En el código:** `service/InstanciaService.java` → `puedeVerConfidencial()`, `descartarConfidencialSinPermiso()` y `visualizarInstanciaPorRol()`.

**Límite:** no hay control de pertenencia: quien tiene `VER_INSTANCIAS` ve las instancias de todos los estudiantes.

## E13. ¿Qué pasa al dar de baja una instancia?

**Respuesta:**
- Baja lógica (`estado = false`), en una transacción.
- Se guardan los valores anteriores en la auditoría (`valoresAuditables`).
- Si el usuario gestiona el calendario, se elimina el evento de Google.

**En el código:** `service/InstanciaService.java` → `darDeBajaInstancia()`.

**Trampa:** la transacción no puede "deshacer" el borrado del evento en Google si después algo falla.

## E14. ¿Qué es el historial de incidencias (RF29)?

**Respuesta:**
- En la ficha del estudiante se listan sus incidencias, con lugar, involucrados y fecha (`obtenerHistorialIncidenciasPorEstudiante`).
- El filtro por período se aplica en pantalla.

**En el código:** `service/InstanciaService.java` → `obtenerHistorialIncidenciasPorEstudiante()`.

**Límite:** el filtro por período es del front, no del back.
