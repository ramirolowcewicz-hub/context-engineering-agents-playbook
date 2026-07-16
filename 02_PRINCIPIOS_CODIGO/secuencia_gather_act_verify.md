# La Secuencia Obligatoria: Gather → Act → Verify

> Esta secuencia no es opcional. Se aplica a toda tarea no trivial de programación o modificación de sistemas.

---

## Los 5 Pasos

### PASO 1: GATHER — Mapear antes de tocar

**Qué hacer:**
- Leer el sistema relevante en su totalidad.
- Comprender la base de datos o el script actual.
- Declarar qué depende de qué (*blast radius*: qué puede romperse).
- Identificar todos los archivos que serán afectados.

**Output de este paso (presentar al usuario):**
```
MAPEO DEL SISTEMA:
- Archivos relevantes: [lista]
- Dependencias identificadas: [lista]
- Blast radius potencial: [qué podría romperse]
- Supuestos que estoy haciendo: [lista]
```

**Regla dura:** Si no podemos mapear el blast radius, no procedemos hasta que el usuario lo aclare.

---

### PASO 2: PLAN — Presentar el enfoque antes de ejecutar

**Qué hacer:**
- Presentar el enfoque propuesto.
- Listar los archivos que se van a tocar.
- Declarar el criterio de éxito medible.
- Listar los supuestos sobre los que se basa el plan.
- Describir el plan de pruebas.
- **Esperar aprobación explícita antes de proceder.**

**Template de plan:**
```
PLAN PROPUESTO:
• Enfoque: [descripción del cómo]
• Archivos que se modifican: [lista]
• Archivos que NO se tocan: [lista — para dejar claro el alcance]
• Supuestos: [lista numérica]
• Criterio de éxito: [descripción medible]
• Cómo lo probamos: [método de verificación]

¿Aprobamos este plan?
```

---

### PASO 3: ACT — Cambio mínimo

**Qué hacer:**
- Implementar únicamente el código estrictamente necesario para cumplir el plan.
- No agregar "mejoras" no planificadas.
- Si se detecta algo que mejoraría el sistema pero está fuera del scope: documentarlo para después, no tocarlo ahora.

**Control de scope:**
```
Durante la ejecución, si aparece una tentación de:
• Refactorizar algo que no pide la tarea → PARAR, documentar, continuar con el scope
• Agregar un feature útil pero no pedido → PARAR, proponer, esperar confirmación
• Mejorar el estilo de código existente → PARAR, es drive-by refactoring
```

---

### PASO 4: VERIFY — Verificar con evidencia

**Qué hacer:**
- Ejecutar los scripts de prueba, linters o queries.
- Mostrar el output real en consola (tanto el comando como el resultado).
- Confirmar que nada fuera del alcance se vio alterado.
- Comparar el resultado contra el criterio de éxito declarado en el PLAN.

**Formato de verificación:**
```
VERIFICATION REPORT:
• Comando: [exactamente lo que se ejecutó]
• Output: [copia exacta del output de consola]
• Criterio de éxito: [PASADO / FALLADO]
• Archivos fuera del scope modificados: [NINGUNO / lista si hubo]
• Efectos secundarios detectados: [ninguno / descripción]
```

**Regla dura:** Si el criterio de éxito falló, ir al PASO 5 (Fix), no ajustar el criterio para que "pase".

---

### PASO 5: FIX (si es necesario) — Arreglar el sistema, no el síntoma

**Qué hacer:**
- Identificar la causa raíz del error en la lógica.
- No colocar parches superficiales que mitiguen el síntoma.
- Proponer la corrección como un nuevo PLAN (volver al PASO 2).
- Documentar el error y su causa raíz en `iteracion.md`.

---

## Cuándo saltear pasos (excepciones válidas)

| Tarea | Pasos requeridos |
|-------|------------------|
| Script de un solo uso, desechable | Puede ir directo a ACT con criterio de éxito informal |
| Corrección de typo en comentario | Solo ACT + VERIFY rápido |
| Refactoring de producción | Todos los pasos obligatorios |
| Nuevo feature en sistema existente | Todos los pasos obligatorios |
| Consulta o análisis sin modificar archivos | Solo GATHER |

**Ante la duda: usar todos los pasos.**
