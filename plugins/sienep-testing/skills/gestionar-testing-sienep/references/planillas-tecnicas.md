# Planillas de técnicas de prueba

Se usan tres técnicas de caja negra: **clases de equivalencia (EP)**, **valores límite (VL)** y **tablas de decisión**. Los casos que no salen de ninguna técnica son **funcionales**.

## Archivos (uno por módulo)

1. Acceso y usuarios.
2. Estudiantes.
3. Instancias.
4. Recordatorios.
5. Usabilidad.
6. Accesibilidad.
7. Servicios (API).

Las versiones finales están en la carpeta Testing del Drive del equipo, en *Proyecto Tecnicatura S4*. Se suben como .xlsx y se convierten con "Guardar como Hojas de cálculo de Google".

## Pestañas

**Casos.** Todos los casos del módulo en TestLink: ID `TL-N`, título, resumen, precondiciones, pasos y resultados, importancia y duración. La técnica se calcula con fórmulas: aparece EP, VL o Decisión según en qué pestaña figura el ID; si no figura en ninguna, es Funcional. Al pie hay un resumen por técnica y por importancia.

**Clases de equivalencia.** Columnas Variable | ID (EP-NN) | Clase | Tipo (Válida/No válida) | Representante | Resultado esperado | Caso 1..3 | Casos (`COUNTA`; en rojo si es 0).

**Valores límite.** Columnas Variable | Límite | Valor probado | Posición (Límite − 1 / Límite / Límite + 1) | Tipo | Resultado esperado | Caso 1..3 | Casos. Se prueba el borde y un valor a cada lado.

**Tabla de decisión.**
- Condiciones con Sí / No / "—" (no importa).
- Una fila de resultado esperado por regla y los casos de TestLink.
- Control:
  - Combinaciones por regla = 2^(cantidad de "—").
  - La suma se compara con 2^(cantidad de condiciones) para indicar si la "Tabla completa" está.

Tablas actuales:
- Inicio de sesión: 5 reglas.
- Activar/desactivar cuentas: 3.
- Cambio de estado del estudiante (baja y reactivación): 5.
- Eliminar informe médico: 2.
- Recurrencia: 10. Las reglas 4 y 5 solo se pueden probar por API.
- Acceso a recordatorios: 3.

**Assertions** (solo en Servicios). Por caso: endpoints, las "Assertion N" y si cumple el mínimo de 2.

## Reglas
- El **resultado esperado** de cada fila es el del **programa real**, aunque el caso de TestLink espere otra cosa. Esa diferencia se registra aparte, en el contraste.
- Cada clase o valor necesita al menos un caso. Si queda una en 0, falta un caso o la clase sobra.
- Los representantes tienen que poder ingresarse en la pantalla. Por ejemplo: cédula de 8 dígitos sin puntos; horas sin segundos.
- Después de generar o cambiar una planilla, recalcularla (LibreOffice headless) y comprobar que ninguna celda tenga errores (`#…`).

## Contraste (documento de apoyo)
"Requerimientos reales y contraste" tiene una pestaña de requerimientos del programa (61, con su RF), el contraste requerimiento ↔ planillas ↔ casos, cada caso frente al programa y cada fila de las planillas frente al programa.

Estados de un caso:
- coincide con el programa;
- espera algo distinto al sistema;
- pasos a corregir;
- fuera del programa.
