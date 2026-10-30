# Estado del testing (checkpoint 28/10/2026)

Actualizar este archivo cuando cambie el estado.

## Hecho
- **Diseño con técnicas:** 7 planillas (ver [planillas-tecnicas.md](planillas-tecnicas.md)).
- **Casos en TestLink:**

  | Suite | Casos |
  |---|---|
  | Aplicación web | 312 (incluye 15 de usabilidad y 17 de accesibilidad) |
  | Servicios (API) | 13: TL-359 a 371, 39 assertions |
  | Base de datos | 29: 15 de la BD operativa y 14 del Data Warehouse |

- **Contraste contra el programa real:**
  - 61 requerimientos: ninguno sin casos; 2 no existen en el programa (foto en el alta, notificaciones).
  - 325 casos (web + servicios): 302 coinciden, 23 esperan otro resultado y van a fallar, ninguno con pasos a corregir y ninguno fuera del programa.
- **Ejecuciones de funcionalidades:** 2 de 3.
  - Plan "Entrega 2", Build 1.
  - Plan "Entrega 3", Build 1: 80 casos; 67 pasados, 6 fallados, 7 bloqueados.

## Decisiones tomadas (no reabrir)
- Se usan 3 técnicas: EP, VL y tablas de decisión. El resto de los casos son funcionales.
- Los casos que esperan algo distinto **se dejan fallar**: al ejecutarlos se decide si es un defecto (va a Mantis) o un error del caso (se corrige).
- Reescritos por decisiones de negocio:
  - 78: derivación → modificar el email.
  - 103: estudiante preasociado.
  - 108: consulta en el historial.
  - 32: fin del bloqueo temporal.
  - 65: alta sin teléfono.
- Corregidos los pasos:
  - Navegación del alta: 210–225 y 273–277.
  - Fechas: 174, 175 y 239.
  - BD operativa con SQL concreto: 87–99, 109 y 110.
- Todas las versiones anteriores quedaron en Obsoleto y las vigentes en Final.
- La suite de servicios se escribió sobre el código de `develop`. El backend desplegado no tiene un dominio público para leer su Swagger: hay que confirmarlo al ejecutar.

## Casos que van a fallar (23)
| Casos | Esperan | Hace el sistema |
|---|---|---|
| 20 | "Contraseña Incorrecta" | "Credenciales inválidas" |
| 21, 22, 23 | Mensajes rojos propios | `required` nativo |
| 24 | Login sin distinguir mayúsculas | El correo es exacto |
| 29, 30, 31 | "Cuenta bloqueada, contacte al administrador" | Bloqueo temporal de 5 minutos, "Demasiados intentos fallidos. Intente más tarde." |
| 69 | Alta con 6 obligatorios | Hay más obligatorios |
| 84 | La baja se bloquea si hay instancias futuras | Avisa y deja dar de baja |
| 100, 104, 105, 106 | Instancia sin canal ni categoría | Canal y categoría son obligatorios |
| 214 | Resultado vago | Solo se oculta "Observación confidencial" |
| 217, 219, 221, 223, 231, 233, 235 | Mensaje de "superó el máximo" | `maxLength`: no deja escribir de más |
| 282 | "Debe seleccionar una frecuencia válida." | Frecuencia es `required` |

Posible defecto real: `incidencias.lugar` (TL-346 y TL-347); ver [comportamiento-programa.md](comportamiento-programa.md).

## Falta (según la letra)
1. Una ejecución más de funcionalidades: plan o build con lo agregado el 28/10 (usuarios, informes médicos, incidencias, Inicio, servicios, BD).
2. Dos ejecuciones completas; la segunda, sobre la versión final.
3. Builds de Retest con Fix y de Regresión, con el tipo en el nombre.
4. Mantis: al menos 20 defectos. La cantidad actual no está verificada.
5. Plan de Pruebas en PDF. Lo hace el equipo; no generarlo sin que lo pidan.
6. Informe de Resultados en PDF.
7. Planilla de riesgos con el seguimiento de esta etapa.
8. Carpeta de entrega `Testing_<doc>_<entrega>_<equipo>` y exportaciones de TestLink y Mantis.
