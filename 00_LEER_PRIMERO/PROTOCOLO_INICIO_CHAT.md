# PROTOCOLO DE INICIO DE CHAT

> **Este protocolo es OBLIGATORIO al inicio de cada nueva conversación.**
> No es opcional. No se puede saltar. Su ejecución tarda menos de 30 segundos y previene el 80% de los errores.

---

## ¿Por qué existe este protocolo?

Los agentes LLM no tienen estado entre sesiones. Cada nueva conversación empieza desde cero. Sin un ritual de arranque explícito, el agente puede:
- Operar con contexto incorrecto o desactualizado.
- Asumir cosas sobre el estado del sistema que ya no son ciertas.
- Responder con confianza sobre datos que no ha visto.

Este protocolo elimina esos riesgos.

---

## PASOS OBLIGATORIOS AL INICIAR UNA SESIÓN

### PASO 1 — LEER LA KNOWLEDGE BASE
```
[ACCIÓN INTERNA — no mostrar al usuario]
Leer y procesar los siguientes archivos en orden:
1. agente.md         → identidad, rol, límites operativos
2. bitacora.md       → contexto histórico, errores pasados, estado actual
3. iteracion.md      → traza de la última ejecución (si existe)
4. diccionario.md    → jerga del dominio (si existe)
```

### PASO 2 — DECLARAR EL ESTADO DE CONTEXTO
Mostrar al usuario un resumen compacto:

```
✅ Contexto cargado — [NOMBRE DEL AGENTE] v[VERSION]

Estado:
• Última ejecución: [fecha de la última entrada en iteracion.md, o 'Primera sesión']
• Errores conocidos: [listar brevemente, o 'Ninguno registrado']
• Datos disponibles: [listar archivos de datos en la knowledge base, o 'Ninguno cargado']
• Modo activo: [Analista / Orquestador / Mixto]

Listo. ¿Qué necesitás?
```

### PASO 3 — VERIFICAR INPUTS ANTES DE ACTUAR
Si la sesión involucra datos (CSVs, excels, logs):
- Confirmar qué archivos están disponibles en el contexto actual.
- NO asumir que los datos de una sesión anterior están presentes.
- Si faltan datos necesarios: pedirlos antes de proceder.

### PASO 4 — CONFIRMAR MODO DE TRABAJO
Si el usuario no lo especifica, preguntar:
```
¿En qué modo trabajamos hoy?
• PLAN — Diseño y análisis sin ejecutar código
• BUILD — Implementación directa del plan aprobado
• REVIEW — Revisión crítica de algo existente
• ANÁLISIS — Exploración de datos (necesito el archivo)
```

---

## SEÑALES DE ALERTA AL INICIO

Si alguna de estas condiciones se cumple, advertir al usuario **antes** de proceder:

| Condición | Advertencia a mostrar |
|-----------|----------------------|
| `iteracion.md` vacío o no existe | "No tengo registro de ejecuciones previas. Empezamos desde cero." |
| `bitacora.md` vacío | "No hay contexto histórico. Confirmar supuestos antes de actuar." |
| Archivo de datos no encontrado | "No veo [nombre_archivo] en el contexto. Por favor adjuntalo." |
| Solicitud sobre datos no vistos | "No procesé ese archivo en esta sesión. No puedo hacer cálculos sobre él sin verlo." |

---

## LO QUE EL AGENTE NO PUEDE HACER AL INICIO

- ❌ Asumir que recuerda algo de una sesión anterior sin leer la bitácora.
- ❌ Responder preguntas sobre datos sin haber visto esos datos.
- ❌ Saltar el paso 1 aunque el usuario pida empezar rápido.
- ❌ Inventar el estado actual del sistema si no está documentado.

---

## PLANTILLA DEL SALUDO CANÓNICO

```markdown
✅ Contexto cargado — [NOMBRE_AGENTE] v[X.X]
📅 Última entrada en bitácora: [FECHA o 'ninguna']
📂 Datos en contexto: [LISTA o 'ninguno']
⚠️  Errores conocidos: [LISTA o 'ninguno']

Modo por defecto: [ANALISTA / ORQUESTADOR]
Listo para trabajar. ¿Qué arrancamos?
```

---

## NOTA SOBRE SESIONES LARGAS

Si una conversación supera las 30-40 interacciones, el contexto del LLM puede saturarse. Cuando esto ocurra:
1. Avisar al usuario: *"El contexto de esta sesión está cerca del límite. Recomiendo documentar el estado actual en `iteracion.md` y abrir una sesión nueva."*
2. Generar un resumen del estado actual para volcar en `iteracion.md`.
3. No continuar ignorando el problema.
