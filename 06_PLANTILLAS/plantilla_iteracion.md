# Plantilla: iteracion.md

> Este archivo se sobreescribe después de cada ejecución.
> Funciona como el log de corto plazo del agente.

---

```markdown
# Iteración — [NOMBRE DEL AGENTE]

> Log de la última ejecución. Se sobreescribe en cada ciclo.
> Para debugging: pegar aquí la traza del error y pedir al agente que entre en Modo Auditor.

---

## ITERACIÓN [YYYY-MM-DD HH:MM:SS]

### Input Recibido
[Descripción de la solicitud o tarea recibida]

### Modo Activo
[ANALISTA / ORQUESTADOR / MIXTO]

### Datos Procesados
- Archivo: [nombre del archivo, o 'No aplica']
- Tamaño: [filas x columnas, o 'No aplica']
- Período cubierto: [desde – hasta, o 'No aplica']

### Acciones Tomadas
1. [Paso 1]
2. [Paso 2]
3. [Paso N]

### Output Generado
- Archivo: [nombre con timestamp, o 'Respuesta en chat']
- Contenido: [descripción del output]

### Criterio de Éxito
[ ] PASADO
[ ] FALLADO → ver sección Errores abajo

### Errores / Comportamiento Inesperado
[NINGUNO]

```
[Si hay error: pegar el stack trace o el output incorrecto exacto aquí]
```

### Hipótesis de Causa Raíz (si hay error)
[Dejar vacío si no hay error]

### Fix Aplicado (si hay error)
[Dejar vacío si no hay error]

### Pendientes para Próxima Sesión
- [ ] [Pendiente 1, si existe]

### Kill-Switches Activados
[NINGUNO / listar si alguno se activó]

---

## HISTORIAL DE ESTA SESIÓN (solo las últimas N interacciones)

### [HH:MM] Interacción 1
[Breve descripción]

### [HH:MM] Interacción 2
[Breve descripción]
```

---

## Cómo Usar Este Archivo para Debugging

Cuando algo falla:

1. Pegar el error exacto en la sección `Errores / Comportamiento Inesperado`.
2. Decirle al agente: **"Entrá en Modo Auditor: leé iteracion.md y diagnosticá la causa raíz"**.
3. El agente leerá su propia traza y propondrá un fix quirúrgico.
4. Aprobar el fix y ejecutar.
5. Documentar el aprendizaje en `bitacora.md`.

**Este flujo es la diferencia entre un agente que mejora y uno que repite los mismos errores.**
