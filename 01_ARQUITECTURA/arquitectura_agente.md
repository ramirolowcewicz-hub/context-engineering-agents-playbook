# Arquitectura Canónica de un Agente

> Todo agente construido bajo este playbook sigue esta estructura. No es sugerida: es obligatoria.

---

## Ecosistema de Archivos

Un agente robusto se compone de un ecosistema ordenado de archivos. Cada archivo tiene una responsabilidad única e irremplazable.

```
agente/
├── agente.md          [OBLIGATORIO]   El cerebro. Identity + reglas + protocolo.
├── bitacora.md        [RECOMENDADO]   Memoria a largo plazo.
├── iteracion.md       [RECOMENDADO]   Log de la última ejecución.
├── diccionario.md     [SI EXISTE]     Jerga del dominio.
├── arquitectura.md    [OPCIONAL]      Mapa de dependencias.
├── plantilla.md       [SI APLICA]     Formato del output.
└── scripts/
    ├── main.py          [SI APLICA]     Lógica determinista principal.
    └── utils.py         [SI APLICA]     Funciones auxiliares.
```

---

## Descripción de Cada Archivo

### `agente.md` — El Cerebro (OBLIGATORIO)

Es el System Prompt. Define quién es el agente y qué puede hacer.

**Secciones mínimas obligatorias:**

```markdown
## IDENTIDAD
- Nombre: [nombre del agente]
- Versión: [X.X]
- Rol: [descripción en una línea]
- Repositorio de referencia: context-engineering-agents-playbook

## MODO OPERATIVO
- Modo primario: [ANALISTA / ORQUESTADOR / MIXTO]
- Capacidades: [lista de lo que SÍ puede hacer]

## KILL-SWITCHES (LO QUE NO PUEDE HACER)
- [Listado explícito de prohibiciones]

## PROTOCOLO DE EJECUCIÓN
- [Paso a paso de cómo opera el agente en cada sesión]

## CRITERIO DE ÉXITO
- [Cómo medir si una respuesta fue buena]
```

---

### `bitacora.md` — La Memoria a Largo Plazo (RECOMENDADO)

Es el diario de vida del agente. Se escribe una sola vez y se actualiza con cada aprendizaje significativo.

**Secciones mínimas:**

```markdown
## CONTEXTO INICIAL (First Principles)
Verdades inmutables del dominio. Nunca cambian sin revisión humana explícita.

## REGISTRO DE ERRORES PASADOS
[FECHA] — [Descripción del error] — [Causa raíz] — [Solución aplicada]

## ESTADO ACTUAL
Ultima actualización: [FECHA]
Arquitectura vigente: [descripción]
Bugs conocidos: [lista o 'ninguno']

## DECISIONES DE DISEÑO
[Por qué se eligió tal enfoque sobre otras alternativas]
```

**Regla de escritura:** Solo agregar entradas. Nunca borrar historial. El pasado del agente es su capital de aprendizaje.

---

### `iteracion.md` — El Log de Ejecución (RECOMENDADO)

Se sobreescribe en cada ejecución. Es el contexto de corto plazo.

**Uso principal:** Cuando algo falla, se pega la traza del error en este archivo y se le pide al agente que entre en "Modo Auditor" para diagnosticar.

```markdown
## ITERACIÓN [FECHA YYYY-MM-DD HH:MM]

### Input recibido
[Qué se le pidió al agente]

### Acciones tomadas
[Resumen de lo que hizo]

### Output generado
[Qué produjo]

### Errores / Comportamiento inesperado
[Traza del error o 'Ninguno']

### Pendientes
[Qué quedó sin resolver]
```

---

### `diccionario.md` — El Contexto Semántico (SI EXISTE)

El agente no puede saber la jerga del negocio por osmosis. Este archivo es el contrato entre el lenguaje del dominio y el lenguaje del modelo.

**Ejemplo de entrada:**
```markdown
### Net Revenue
Fee + Upfronts. NO incluye reembolsos. Se calcula sobre ventanas cerradas de 4 semanas.
Ref: definición aprobada por Finance en Q2-2025.
```

**Regla de mantenimiento:** Toda nueva terminología que aparezca en los datos y no esté en el diccionario debe ser consultada antes de usarla, nunca inferida.

---

### `arquitectura.md` — El Mapa de Dependencias (OPCIONAL)

Documenta cómo fluyen los datos entre los archivos del agente. Útil cuando el ecosistema crece en complejidad.

Formato mínimo:
```
[INPUT] datos.csv
    ↓
[SCRIPT] main.py  ←  diccionario.md (contexto semántico)
    ↓
[OUTPUT] reporte_YYYYMMDD_HHMMSS.html
    ↓
[LOG] iteracion.md (actualizado automáticamente)
```

---

## Jerarquía de Autoridad

Cuando hay conflicto entre fuentes de información, esta jerarquía define cuál gana:

```
1. Instrucciones del humano en la sesión actual  (mayor autoridad)
2. agente.md                                      (identidad y límites)
3. bitacora.md                                    (contexto histórico)
4. diccionario.md                                 (definiciones del dominio)
5. iteracion.md                                   (estado de la última ejecución)
6. Conocimiento propio del LLM                    (menor autoridad; solo si nada anterior cubre el tema)
```

**Implicación crítica:** Si el LLM "cree" algo que contradice la knowledge base, la knowledge base gana. Siempre.

---

## Principio de Mínima Superficie de Conocimiento

Un agente solo debe saber lo que necesita para su tarea. No cargar contexto irrelevante:
- Mejora la calidad de respuestas (menos ruido en el contexto).
- Reduce el riesgo de que el agente "mezcle" dominios.
- Facilita el debugging cuando algo sale mal.
