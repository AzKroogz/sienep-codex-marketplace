# Banco 1: seguridad

Rutas del back relativas a `src/main/java/com/sienep/pdi_sienep3/`.

## S1. ¿Cómo funciona el login?

**Respuesta (30 s):** el usuario manda email y contraseña a `/api/auth/login`. El back:
1. busca la cuenta por email;
2. revisa si tuvo 3 intentos fallidos en los últimos 5 minutos y, si es así, la bloquea (429);
3. compara la contraseña con BCrypt;
4. rechaza las cuentas inactivas (403);
5. si todo está bien, genera un JWT con el email y el `tokenVersion`.

Cada intento, exitoso, fallido o bloqueado, queda en la auditoría.

**En el código:** `service/AuthService.java` → `login()`. El bloqueo usa `AuditoriaService.tieneDemasiadosIntentosFallidos(usuario, 3, 5)`, que cuenta los `LOGIN_FALLIDO` de la auditoría.

**Repreguntas:**
- ¿De dónde sale el contador de intentos? De la tabla de auditoría, no de una columna en usuarios.
- ¿Qué código HTTP da cada caso? Credenciales mal: 401. Inactivo: 403. Bloqueado: 429.

**Trampa:** decir que la contraseña se "desencripta" para compararla. BCrypt es un hash: `passwordEncoder.matches()` hashea lo que llega y compara.

## S2. ¿Qué recorrido hace un pedido protegido?

**Respuesta:**
1. `JwtAuthenticationFilter` toma el header `Authorization: Bearer`.
2. Valida la firma y la expiración del JWT.
3. Busca el usuario y comprueba que esté activo y que el `tokenVersion` del token sea igual al de la base.
4. Carga los permisos del rol como authorities en el `SecurityContext`.
5. Después, `@PreAuthorize` en el controller decide si tiene permiso.

**En el código:** `security/JwtAuthenticationFilter.java` → `doFilterInternal()`, y `config/SecurityConfig.java` → `securityFilterChain()`. Los permisos vienen de `funcionarioRepository.buscarConRolYPermisosPorUsuario()`.

**Repreguntas:**
- ¿Qué pasa si no manda token? El filtro deja pasar, pero `anyRequest().authenticated()` corta con 401.
- ¿Qué rutas son públicas? Login, Swagger, `/v3/api-docs` y las de OAuth.

**Trampa:** confundir autenticación con autorización. El filtro autentica (quién sos); `@PreAuthorize` autoriza (qué podés hacer).

## S3. El JWT es stateless. ¿Cómo hacen para que el logout lo invalide?

**Respuesta:**
- Cada usuario tiene una columna `token_version`, que va dentro del JWT.
- Al hacer logout, el back incrementa esa versión.
- Desde ese momento, todo token viejo tiene una versión distinta a la de la base, y el filtro lo rechaza.

Así se invalidan en el servidor todos los tokens de esa cuenta, sin guardar una lista negra.

**En el código:**
- `service/AuthService.java` → `logout()` → `usuarioRepository.incrementarTokenVersion()`.
- La comparación está en `JwtAuthenticationFilter`, con `extractTokenVersion(token) == usuario.getTokenVersion()`.
- La migración es `db/migrations/20261014_usuarios_token_version.sql`.
- La prueba es `LogoutInvalidacionTokenTest`.

**Repreguntas:**
- ¿Qué limitación tiene? Cierra todas las sesiones de esa cuenta, no solo la del dispositivo actual.
- ¿Por qué no una lista negra? Habría que guardar cada token hasta que venza; la versión es una sola columna.

**Trampa:** decir que "el logout borra el token del navegador y listo". Eso solo es local: sin `token_version`, el token seguiría sirviendo hasta que venza.

## S4. ¿El JWT está cifrado? ¿Qué garantiza?

**Respuesta:**
- **No está cifrado, está firmado** (HMAC, con la clave `JWT_SECRET`). Cualquiera puede leer el contenido, pero nadie puede modificarlo sin que la firma deje de coincidir.
- Por eso adentro solo van el email, el `tokenVersion` y la expiración (24 h); nada secreto.

**En el código:** `security/JwtService.java` → `generarToken()` y `tokenValido()`. La clave viene de la variable de entorno `JWT_SECRET`.

**Repregunta:** ¿por qué 24 h si la sesión se cierra a los 15 minutos? Los 15 minutos son por inactividad en el front (`AuthGuard`); el JWT tiene su propia expiración, y el logout lo invalida antes.

**Trampa:** "el JWT está encriptado". Está firmado.

## S5. ¿Cómo funciona el login con Google? ¿Qué pasa con una cuenta de Google que no existe en SIENEP?

**Respuesta:**
- Spring Security hace el flujo OAuth 2.0 con Google (`oauth2Login`).
- Cuando Google confirma la identidad, `GoogleLoginSuccessHandler` busca ese email en SIENEP y emite **nuestro propio JWT** con `AuthService.loginConGoogle()`.
- Si el email no existe o la cuenta está inactiva, redirige al login con `?error=google-no-autorizado`.
- Google solo autentica: los permisos siguen siendo los del rol interno.

**En el código:** `security/GoogleLoginSuccessHandler.java` → `onAuthenticationSuccess()`, `service/AuthService.java` → `loginConGoogle()` y `SecurityConfig` → `.oauth2Login(...successHandler...)`.

**Repregunta:** ¿por qué la sesión no es `STATELESS` en `SecurityConfig`? La sesión HTTP se usa solo para el ida y vuelta con Google (el `state` de OAuth). La autenticación no se guarda en la sesión: se usa `RequestAttributeSecurityContextRepository`, y cada pedido se valida con el JWT.

**Trampa:** decir que "Google da los permisos". OAuth no reemplaza la autorización.

## S6. ¿Qué pasa en el primer ingreso de una cuenta nueva?

**Respuesta:**
- La cuenta se crea con `debe_cambiar_contrasena = true`.
- Mientras eso esté activo, el filtro de JWT rechaza con 403 (`CAMBIO_CONTRASENA_OBLIGATORIO`) cualquier pedido, salvo cambiar la contraseña, `/api/auth/me` y el logout.
- En el front, `AuthGuard` lo detecta y manda a `/cambiar-contrasena`.

**En el código:**
- `JwtAuthenticationFilter` → `esRutaDelCambioDeContrasena()` y `rechazarPorCambioObligatorio()`.
- La migración es `20261101_usuarios_debe_cambiar_contrasena.sql`.
- La prueba es `CambioContrasenaObligatorioTest`.

**Repregunta:** ¿por qué controlarlo en el back y no solo redirigir en el front? Porque con el token se podría llamar a la API directamente, por ejemplo desde Swagger.

**Límite:** el correo con la clave inicial no se envía (RF03); la comunica el administrador.

## S7. ¿Qué reglas tiene la contraseña y cómo se guarda?

**Respuesta:**
- Mínimo 8 caracteres, al menos una letra y un número.
- Se guarda con un hash BCrypt (`passwordEncoder.encode`) y nunca vuelve en ninguna respuesta, porque los DTO no la incluyen.

**En el código:** `service/UsuarioService.java` → `validarContrasena()` y `crearUsuarioDesdeRegistro()`. El bean de BCrypt está en `config/PasswordConfig.java`.

**Trampa:** "la ciframos con BCrypt". Es un hash de un solo sentido, con salt.

## S8. ¿Cuándo devuelven 400, 401, 403, 404, 409 o 500?

**Respuesta:** lo centraliza `GlobalExceptionHandler`:

| Código | Cuándo |
|---|---|
| 400 | Validación del DTO (`@Valid`), regla de negocio (`ValidacionNegocioException`, por ejemplo la cédula), JSON mal formado o parámetro inválido o faltante (`PARAMETRO_INVALIDO` o `PARAMETRO_FALTANTE`) |
| 401 | Sin autenticar o credenciales incorrectas |
| 403 | Autenticado pero sin permiso (`AccessDeniedException`), o cuenta inactiva |
| 404 | `RecursoNoEncontradoException` |
| 409 | Duplicado (`NombreDuplicadoException`, `DataIntegrityViolationException`), o Calendar pide reconectar |
| 413 | Archivo de más de 10 MB |
| 429 | Demasiados intentos de login |
| 500 | Solo lo inesperado, con un mensaje genérico |

**En el código:** `exception/GlobalExceptionHandler.java`, un método `@ExceptionHandler` por excepción.

**Repreguntas:**
- Den un ejemplo de 409. Cédula o email ya registrados.
- ¿Por qué el 500 tiene un mensaje genérico? Para no exponer detalles internos ni la pila.

**Trampa:** confundir 401 con 403.

## S9. ¿Cómo se aplican los permisos? ¿Qué es `@PreAuthorize`?

**Respuesta:**
- Cada rol tiene permisos (muchos a muchos). El filtro los carga como authorities.
- En cada endpoint, `@PreAuthorize("hasAuthority('GESTIONAR_ESTUDIANTES')")` deja pasar solo a quien tiene ese permiso. Si no lo tiene, responde 403.
- El front oculta botones según los permisos, pero eso es solo comodidad: la regla está en el back.

**En el código:** por ejemplo `controller/EstudianteController.java` (`VER_ESTUDIANTES`, `GESTIONAR_ESTUDIANTES`, `VER_DATOS_SENSIBLES_ESTUDIANTE`, `MODIFICAR_DATOS_SENSIBLES_ESTUDIANTE`). En el front, `lib/permisos.ts`.

**Repregunta:** ¿qué authorities tiene un estudiante? Ninguna de funcionario: los permisos se cargan desde el funcionario asociado. El estudiante no es un rol, es un tipo de cuenta.

**Prueba negativa:** con el rol Legales, intentar editar una instancia por Swagger da 403.

## S10. ¿Qué se audita en el login y qué no se guarda nunca?

**Respuesta:**
- Se auditan `LOGIN_EXITOSO`, `LOGIN_GOOGLE_EXITOSO`, `LOGIN_FALLIDO`, `LOGIN_BLOQUEADO` y `LOGOUT`, con el usuario, la fecha y hora y el resultado.
- Nunca se guarda la contraseña ni el token, ni en la auditoría ni en los logs.

**En el código:** las llamadas a `auditoriaService.registrar(...)` en `AuthService`.

**Repregunta:** si el email no existe, ¿se audita? No: no hay usuario al que asociarlo, y se responde 401 igual que con una contraseña incorrecta, para no revelar qué emails existen.
