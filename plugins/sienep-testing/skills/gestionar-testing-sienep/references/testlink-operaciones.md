# Operar TestLink (UTEC)

Base: `https://testlink.utec.edu.uy/testlink`. Proyecto `2026-PFT-DZ-GRUPO04` (id 1513018), prefijo de los casos `2026PFTDZG04-`.

La sesión la abre el usuario: no se escriben sus credenciales. Desde un navegador automatizado se usa `fetch` dentro de la página para aprovechar su sesión.

## Suites (id del contenedor)

| Suite | id |
|---|---|
| Aplicación Web SIENEP | 1543494 |
| ├ Módulo 1 – Autenticación y Acceso | 1551722 |
| ├ Módulo 2 – Gestión de Estudiantes | 1552101 |
| ├ Módulo 3 – Gestión de Instancias | 1552980 |
| └ Módulo 4 – Gestión de Recordatorios | 1639893 |
| Base de Datos Operativa – Módulo 2 (DB) | 1552979 |
| Base de Datos Operativa – Módulo 3 (DB) | 1552981 |
| Servicios del Sistema SIENEP | 1543496 |

Planes existentes: "Entrega 2" (1557276), "Entrega 3" (1649885) y "test" (1513051, vacío).

## Exportar una suite completa (para auditar)

`/lib/results/printDocument.php?level=testsuite&id=<suite>&type=testspec&summary=y&body=y&header=y&toc=n&author=n&keyword=n&requirement=n&cfields=n`

Cada caso es una `table.tc`:
- El `th` tiene "Caso de Prueba 2026PFTDZG04-N: título".
- Las filas con `span.label` traen Resumen, Precondiciones, Importancia y Duración.
- Las filas de 3 `td` con un número en la primera son los pasos: número, acción y resultado.

Los encabezados `h1`/`h2`/`h3` indican la suite. Con `level=testproject&id=1513018` se exporta todo el proyecto.

## Importar casos (XML)

Pantalla: `/lib/testcases/tcImport.php?containerID=<suite>`. Tiene tres selectores: tipo (XML), "Considerar duplicado si" y "Acción para duplicados".

| Objetivo | "Duplicado si" | "Acción" |
|---|---|---|
| Casos nuevos | tiene el mismo nombre | Do not import the test case |
| Corregir casos existentes | tiene el mismo ID Externo | Crear una nueva versión |

Formato (los textos van en `<p>` dentro de CDATA; con un resultado vacío el paso queda sin resultado):

```xml
<testcases>
<testcase name="Validar alta de estudiante sin teléfono">
<externalid>65</externalid>  <!-- solo para corregir un caso existente -->
<summary><![CDATA[<p>Verificar que el teléfono sea opcional.</p>]]></summary>
<preconditions><![CDATA[<p>Usuario con permiso de gestión de estudiantes.</p>]]></preconditions>
<execution_type>1</execution_type><importance>2</importance><status>7</status><estimated_exec_duration>3</estimated_exec_duration>
<steps>
<step><step_number>1</step_number><actions><![CDATA[<p>Ingresar a Configuración → Usuarios…</p>]]></actions><expectedresults><![CDATA[<p>Se muestra el formulario…</p>]]></expectedresults><execution_type>1</execution_type></step>
</steps></testcase>
</testcases>
```

Códigos: `importance` 3 = Alta, 2 = Media, 1 = Baja. `status`: 1 = Borrador, 2 = Listo para revisión, 3 = Revisión en curso, 4 = Modificado, **5 = Obsoleto**, 6 = Futuro, **7 = Final**.

Después de importar: la página lista cada caso con "ok". Volver a exportar la suite y verificar la cantidad de casos, los pasos y que no haya duplicados.

## Cambiar el estado de una versión

1. ID interno del caso: `POST /lib/testcases/tcSearch.php` con el formulario de búsqueda y `targetTestCase=2026PFTDZG04-N`. El resultado contiene `openTCEditWindow(<id>)`.
2. Abrir `/lib/testcases/archiveData.php?edit=testcase&id=<id>&show_mode=show`.
   - La versión vigente es `#topControls input[name=tcversion_id]`.
   - Cada versión tiene un `form#statusForm_<tcversion_id>` (`doAction=setStatus`).
3. Enviar ese formulario con `status=7` para la vigente y `status=5` para las anteriores. Volver a abrir el caso y confirmar.

## Planes y métricas
- Builds de un plan: `/lib/plan/buildView.php?tplan_id=<id>`.
- Métricas: `/lib/results/resultsGeneral.php?tplan_id=<id>&format=0` (falla si el plan no tiene builds).
