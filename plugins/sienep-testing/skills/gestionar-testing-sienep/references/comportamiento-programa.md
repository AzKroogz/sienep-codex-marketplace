# Comportamiento real del programa (para escribir y auditar casos)

Verificado en el código el 28/10/2026: frontend `develop` 144d3a5 y backend `develop` ce1d080. Si el código cambió, volver a verificar antes de usarlo.

## Login (Módulo 1)
- Correo con `required` y `type=email`; contraseña con `required`. Si falta un dato o el formato es inválido, **el navegador frena el envío** con su aviso. No hay mensajes rojos propios.
- Un correo no registrado, un correo con otra capitalización (la búsqueda es exacta) o una contraseña incorrecta dan el mismo mensaje: **"Credenciales inválidas"** (401).
- Usuario dado de baja con la contraseña correcta: **"Usuario inactivo"** (403). Se evalúa después de la contraseña.
- Bloqueo **temporal**: con 3 o más fallos en los últimos 5 minutos, el intento siguiente da **"Demasiados intentos fallidos. Intente más tarde."** (429). Se levanta solo: no existe el desbloqueo por un administrador.
- Inactividad: la sesión se cierra a los **15 minutos**. Cerrar sesión invalida el token (`token_version`).
- Inicio con Google: botón "Continuar con Google".

## Usuarios (Configuración → Usuarios)
- Listado con búsqueda por nombre o email y filtro Todos / Funcionarios / Estudiantes / Sin perfil. Acciones Editar y Desactivar/Activar, con confirmación.
- "Nueva cuenta" → Tipo de cuenta Funcionario o Estudiante. Botones "Crear cuenta" y "Crear estudiante".
- Obligatorios: usuario (máx. 100), email (100), nombre y apellido (50), cédula, fecha de nacimiento, contraseña, sede y rol. Para estudiante, además: matrícula (200), carrera, grupo (depende de la carrera), sistema de salud (50), calle, número de puerta, ciudad, departamento y país.
- Cédula: **exactamente 8 dígitos, sin puntos ni guion** (`\d{8}`), con dígito verificador. Válida: 41234563; inválida: 41234567.
- Contraseña: **mínimo 8 caracteres** en el formulario; máximo 200 en el backend, sin `maxLength`.
- "Observación confidencial" **solo aparece** con el permiso `MODIFICAR_DATOS_SENSIBLES_ESTUDIANTE`.
- El alta **no tiene campo de foto**: la foto se sube al editar.

## Estudiantes
- Listado: columnas Nombre, Carrera y Email; paginación "Página X de Y"; total de estudiantes.
- Búsqueda por nombre, cédula, carrera y grupo: texto parcial, sin distinguir mayúsculas, combinable. Filtro Estado (Activos / Inactivos) y orden por campo, ascendente o descendente.
- Ficha:
  - "Modificar estudiante", "Dar de baja" y "Dar de alta", con confirmación.
  - "Crear instancia" y "Consultar instancias".
  - La baja con instancias futuras **avisa y deja confirmar**: no se bloquea.
- Edición:
  - La cédula no aparece.
  - Teléfonos (máx. 20): "Agregar teléfono", "Guardar teléfono" y "Quitar".
  - Foto solo JPG o PNG de hasta 5 MB. Mensajes: "La foto debe ser JPG o PNG." y "La foto no puede superar los 5 MB.".
- Informes médicos:
  - Formatos PDF, JPG y PNG, hasta 10 MB.
  - Mensajes: "Solo se permiten archivos PDF, JPG y PNG." y "El archivo no puede superar los 10 MB.".
  - Acciones Ver, Descargar y Eliminar (con confirmación).
- Los campos con `maxLength` **no dejan escribir de más**: el límite + 1 no muestra mensaje. Excepción: la contraseña.

## Instancias
- Se crean desde la ficha y el estudiante **viene fijo**: no hay selector.
- Primero se elige el Tipo de instancia: Registro común o Incidencia.
- Registro común:
  - Obligatorios: título (50), fecha y hora, canal (32) y categoría.
  - Opcionales: comentario (500), comentario confidencial (500) y participantes. El estudiante y quien registra se agregan solos.
  - Botón "Guardar registro común".
- Incidencia:
  - Obligatorios: título, fecha y hora, e involucrado.
  - Opcionales: lugar (500) y comentarios.
  - Botón "Guardar incidencia".
- Título repetido, sin distinguir mayúsculas: "Ya existe una instancia con ese titulo". Para un estudiante dado de baja: "No se puede crear una instancia para un estudiante dado de baja".
- Historial ("Consultar instancias"): muestra título, fecha, "Código: INST-…", comentario y participantes. **No muestra el comentario confidencial.** No hay pantalla de detalle de una instancia.
- Editar, dar de baja y clonar instancias **solo se puede por API**.

## Recordatorios
- Alta: título (50), tipo (100) y descripción (200) son obligatorios y no admiten solo espacios. El formulario no tiene `maxLength`: el backend responde, por ejemplo, "El título no puede superar los 50 caracteres".
- Fecha y hora **futura**, en `datetime-local` (**sin segundos**). Si la fecha es pasada: "La fecha y hora debe ser futura". Los recordatorios con fecha de hoy temprano o de ayer se crean el día anterior.
- Recurrencia: Frecuencia (Diaria/Semanal/Mensual) es `required`. Finalización por cantidad (mínimo 1; más de 365 da "La recurrencia debe estar entre 1 y 365") o por fecha final (no anterior al inicio). Al elegir el tipo de finalización se borra el otro campo.
- Listado en Vencidos / Hoy / Próximos, con búsqueda por título, código o descripción. Panel de sincronizaciones pendientes de Google.
- Detalle: "Editar recordatorio", "Dar de baja", Google Calendar y "Crear instancia desde recordatorio".

## Inicio y menú
- Inicio: "Próximas instancias" y "Tus recordatorios" (hoy, vencidos y próximos), con mensajes "No tenés …" cuando no hay datos.
- El menú depende de los permisos:
  - Estudiantes = `VER_ESTUDIANTES`.
  - Recordatorios = `GESTIONAR_RECORDATORIOS`.
  - Usuarios = `GESTIONAR_FUNCIONARIOS`.
  - "Instancias" y "Reportes" aparecen como **Pronto**.

## API (Swagger)
- Público: `/api/auth/login`, Swagger y el callback de Google. Todo lo demás exige JWT.
- Sin token → 401. Sin permiso → 403 `ACCESO_DENEGADO`. Recurso inexistente → 404 `RECURSO_NO_ENCONTRADO`. Body inválido → 400 `VALIDACION_ERROR`, con `errores` por campo. Duplicado → 409 `REGISTRO_DUPLICADO`.
- Login → `{token, tipo: "Bearer"}`. Logout → "Sesion cerrada correctamente." y el mismo token pasa a dar 401.
- Funciones sin pantalla:
  - `PUT` / `DELETE /api/instancias/{id}` y `POST /api/instancias/{id}/clones`.
  - `/api/categorias` y `/api/roles` (+ `/permisos`).
  - `/api/reportes/seguimiento/estudiante/{id}` (+ `/pdf`).
  - `/api/auditorias`, ordenado de lo más reciente a lo más viejo, con acciones `LOGIN_EXITOSO`, `LOGIN_FALLIDO`, `LOGIN_BLOQUEADO`, `LOGOUT`, `ALTA_ESTUDIANTE`, etc.

## Base de datos operativa (esquema `proyectopdi`)
- Un estudiante ocupa varias tablas: `usuarios` (cédula, nombre, email, contraseña cifrada, `estado_usuario`, `token_version`), `estudiantes` (`f_nacimiento`, matrícula, `sis_salud`, `id_grupo`, `id_carrera`, `id_direccion`), `direcciones` y `telefonos`.
- La baja lógica cambia **`usuarios.estado_usuario`**: la tabla `estudiantes` no tiene estado.
- Instancias: la tabla `instancias` más `comunes` (canal, `id_categoria`) o `incidencias` (involucrado, lugar), y `participantes`.
- Posible inconsistencia, a confirmar en la base desplegada: el script tiene `incidencias.lugar varchar(32) NOT NULL`, pero la aplicación permite dejarlo vacío y escribir hasta 500 caracteres.
