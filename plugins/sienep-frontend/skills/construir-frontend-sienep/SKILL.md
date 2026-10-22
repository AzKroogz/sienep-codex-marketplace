---
name: construir-frontend-sienep
description: Usar para cualquier cambio de código en el frontend SIENEP (Next.js, repositorio sienep-frontend): pantallas nuevas, migraciones de la reestructura, servicios en lib/, tipos, componentes o arreglos. Impone la estructura página → lib/<modulo>.ts → solicitarJson/ErrorApi, el flujo diff-antes-de-aplicar y el registro de decisiones para la defensa.
---

# Construir el frontend SIENEP

## GUARDRAIL (obligatorio, sin excepciones)

**Todo código sigue exactamente la estructura diseñada el 21/10/2026. No se forman otras cosas ni se escribe de más.**

| Pieza | Dónde | Regla |
|---|---|---|
| Página | `app/**/page.tsx` | Contenedor: estado, navegación y errores. Nunca llama a `fetch`. |
| Servicio | `lib/<modulo>.ts` | Una función por endpoint. Firma `(apiUrl, token, …args, fetchImpl = fetch)`. Implementada con `solicitarJson` de `./solicitud.ts`. Sin `router`, `useState` ni mensajes de pantalla. |
| Error | `lib/solicitud.ts` | Solo `ErrorApi` (`status`, `message`, `errores`). No crear otras clases de error. |
| Tipos | `types/<entidad>.ts` | Una definición por entidad. No redefinir tipos en páginas. |
| Componente | `components/<modulo>/` | Presentacional: todo por props. |
| Mapper | `lib/<modulo>-form.ts` / `crearPayload…` | Transformar formulario → payload, con test. |
| Test | `lib/<modulo>.test.mjs` | `node --test` con `fetchImpl` falso. |

### Herramientas permitidas para codear (únicas)

| Para | Solo esto |
|---|---|
| Framework | Next.js 16.3.5 (App Router), páginas `"use client"` |
| UI | React 19.2.8: `useState`, `useEffect`, `useRef`, props |
| Lenguaje | TypeScript 5.9 (`strict`) |
| Estilos | Tailwind CSS 4 (clases en `className`); `globals.css` solo si ya existe la clase |
| Llamadas a la API | `fetch` nativo, siempre a través de `solicitarJson` |
| Navegación | `next/navigation` (`useRouter`, `useParams`, `usePathname`) y `next/link` |
| Sesión | `localStorage`/`sessionStorage` solo mediante `lib/api.ts` (`obtenerToken`, `limpiarSesion`) |
| Tests | `node:test` + `node:assert/strict` (`npm test`) |
| Calidad | ESLint (`npx eslint .`), `tsc --noEmit`, `npm run build` |

Para **verificar**, no para codear, también: Playwright MCP contra el build local con la API simulada.

Cualquier otra librería o herramienta (axios, SWR/React Query, Redux/Zustand, librerías de componentes o formularios, Jest/Vitest, etc.) está **prohibida** salvo autorización explícita del usuario.

Prohibido:
- helpers, hooks, contextos o capas nuevas; clientes genéricos usados desde páginas;
- dependencias nuevas o herramientas fuera de la tabla anterior;
- funcionalidades, validaciones o "mejoras" que la tarea no pide; código "por las dudas";
- comentarios que repiten el código;
- tocar backend o BD (solo documentar como límite).

Antes de cada diff, comprobar: ¿usa solo las piezas de la tabla? ¿es lo mínimo para la tarea? Si algo no encaja, **preguntar al usuario antes de inventar**.

Convenciones fijas:
- 401 en página: `limpiarSesion(); router.replace("/"); return;`
- 403 en página: mensaje "No tenés permisos para …".
- Imports entre archivos de `lib/` con ruta relativa y `.ts` (`./solicitud.ts`); desde páginas, `@/lib/...`.
- Si un nombre del servicio choca con uno de la página, alias con sufijo `Api` (`buscarEstudiantesApi`).
- Nombres en español; mismo estilo que el código vecino.

## Plantillas mínimas

Servicio:
```ts
export function obtenerX(apiUrl: string, token: string, id: number, fetchImpl: typeof fetch = fetch) {
  return solicitarJson<X>(`${apiUrl}/api/x/${id}`, token, "No se pudo cargar X.", {}, fetchImpl);
}
```

Página:
```ts
obtenerX(API_URL, token, Number(id))
  .then((data) => { setX(data); setCargando(false); })
  .catch((error) => {
    if (error instanceof ErrorApi && error.status === 401) { limpiarSesion(); router.replace("/"); return; }
    setError(error instanceof ErrorApi && error.status === 403 ? "No tenés permisos para ver X." : "No se pudo cargar X.");
    setCargando(false);
  });
```

## Flujo por tarea

1. Leer el estado real: `git status`, la rama y los archivos a tocar. El plan es contexto, no verificación.
2. Rama nueva desde `origin/develop`, o apilada sobre la anterior si depende de ella. **Nunca** push ni commits en `develop`, `main` o `pft-main`; el push lo hace el usuario.
3. **Mostrar el diff y esperar el OK** antes de cada modificación, un paso lógico por vez:
   a. tests que fallan → aplicar → `npm test` (deben fallar);
   b. `lib/` y `types/` → aplicar → `npm test` + `npx tsc --noEmit`;
   c. pantallas: armar el diff en una copia en el scratchpad (`git diff`) → mostrar → `git apply`.
4. Verificar: `npm test`, `npx tsc --noEmit`, `npx eslint .`, `npm run build`. Si algo falla, mostrar el diff del arreglo antes de aplicarlo.
5. Navegador: `npx next start -p 3100` en segundo plano + Playwright MCP con `page.route('**/api/**')` y `localStorage.token` falso (sin Railway). Comprobar:
   - que las llamadas por pantalla no aumentan (tabla del §3 de [la auditoría](references/auditoria-frontend.md));
   - 401 → `/` con `localStorage` y `sessionStorage` vacíos;
   - 403 → mensaje de permisos.
   Para `window.confirm`, reemplazarlo con `page.evaluate(() => { window.confirm = () => true; })`. Para tiempos, usar `page.clock`. Al terminar, cerrar el navegador y matar el servidor con `pgrep -x next-server` (no `pkill -f`, que mata la propia shell).
6. Agregar la entrada en [references/registro-decisiones.md](references/registro-decisiones.md) y publicarla en el marketplace con una PR que suba la versión del plugin.
7. Proponer el commit (mensaje en español, sin trailers ni menciones de IA) y hacerlo solo con el OK. No incluir `AGENTS.md`, `CLAUDE.md` ni `next-env.d.ts`.

## Entrada del registro de decisiones

Cada entrada (una por commit), corta:
- **Rama y commit.**
- **Qué cambió** (archivos).
- **Antes / después.**
- **Patrón** y su equivalente en el backend.
- **Por qué es mejor**, con evidencia (tests, llamadas medidas).
- **Defensa en 30 segundos:** respuesta directa → concepto → decisión SIENEP → evidencia → límite.
- **Preguntas probables** con su respuesta corta.

## Referencias

- Plan de tareas: [references/plan-reestructura.md](references/plan-reestructura.md)
- Registro para la defensa: [references/registro-decisiones.md](references/registro-decisiones.md)
- Auditoría (hallazgos F1-F10 y llamadas medidas): [references/auditoria-frontend.md](references/auditoria-frontend.md)
- Prioridades del front (AGENTS.md): funcionalidad → responsive → presentación → accesibilidad.
- Este repo usa Next.js 16: ante dudas de API, leer `node_modules/next/dist/docs/` antes de escribir.
