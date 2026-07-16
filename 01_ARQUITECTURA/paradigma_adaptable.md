# El Paradigma Adaptable: Analista vs. Orquestador

> La elección correcta entre estos dos modos es la decisión de diseño más importante de cualquier agente.

---

## Los Dos Modos

### MODO ANALISTA — El Agente Razona

El agente usa su capacidad nativa de razonamiento del LLM.

**Usar cuando:**
- El problema requiere comprensión semántica (textos, estrategia, inferencia de contexto).
- El resultado correcto depende de juicio, no de cálculo.
- Los datos son pequeños y verificables visualmente.
- La precisión numérica no es crítica (estimaciones, rangos, tendencias cualitativas).

**Ejemplos válidos:**
- "Resumir este reporte de 3 páginas"
- "Analizar las tendencias de este párrafo"
- "Evaluar si esta propuesta tiene sentido estratégico"
- "Explicar por qué un KPI podría estar bajo"

**Límite crítico:** El agente NO puede sumar columnas de un CSV grande en modo Analista. El LLM puede equivocarse en aritmética con series largas de números.

---

### MODO ORQUESTADOR — El Agente Ejecuta Código

El agente delega la computación a código determinista (Python/SQL) y solo interpreta los resultados.

**Usar cuando:**
- El archivo de datos tiene más de ~1,000 filas o ~1MB.
- El cálculo debe ser exacto y reproducible.
- Hay riesgo de Out-Of-Memory (OOM) si el LLM procesa todo el contexto.
- El resultado será usado para tomar decisiones de negocio.

**Ejemplos válidos:**
- "Calcular el revenue total por canal del CSV de ventas"
- "Agrupar por semana y encontrar el pico máximo"
- "Cruzar dos tablas y detectar discrepancias"
- "Generar una tabla pivote del archivo de 200k filas"

**Ventajas del Orquestador:**
- Los números son correctos (el código no alucina).
- El proceso es auditable (el script queda registrado).
- No colapsa con datos grandes.
- El resultado es reproducible en cualquier momento.

---

## Árbol de Decisión

```
¿El problema involucra datos numéricos?
├── NO  → Modo Analista (razonamiento del LLM)
└── SÍ  → ¿Los datos están completamente en el contexto visible?
            ├── SÍ, son pocos (≤50 filas) → Analista puede funcionar
            └── NO, están en un archivo → Modo Orquestador OBLIGATORIO
                                              (escribir y ejecutar script)
```

---

## Anti-Patrones a Evitar

### Anti-patrón 1: El Agente Calculador
El agente intenta sumar/agrupar/calcular datos de un CSV largo leyéndolos en el contexto.

**Consecuencias:** Alucinaciones numéricas, resultados incorrectos sin advertencia, errores difíciles de detectar.

**Solución:** Siempre Modo Orquestador para datos tabulares grandes.

### Anti-patrón 2: El Agente Sobre-Automatizado
Se crea un script para cada pequeña consulta, incluso cuando el razonamiento nativo bastaría.

**Consecuencias:** Overhead innecesario, dificultad de mantenimiento, lentitud operativa.

**Solución:** Usar Analista para preguntas que el LLM puede responder con certeza desde la knowledge base.

### Anti-patrón 3: El Modo Híbrido sin Freno
El agente mezcla cálculos del LLM con cálculos del script sin documentar cuál hizo qué.

**Consecuencias:** Imposible auditar. Errores indetectables.

**Solución:** En el output, siempre indicar qué cálculos vinieron del script (confiables) y cuáles del razonamiento (estimaciones).

---

## Conveyor Belt: Cómo pasar de uno a otro en una sesión

```
Usuario pregunta algo
    ↓
Agente determina el modo correcto
    ↓
[Analista]                              [Orquestador]
Responde desde la KB                    Escribe el script
o desde el razonamiento                 Muestra el plan
    ↓                                   Espera aprobación
Marca certeza                           Ejecuta
    ↓                                   Muestra resultado real
Usuario evalua                              ↓
                                        Agente interpreta el output
                                        Marca qué es resultado de código
```

---

## Nota sobre Modelos que Ejecutan Código

Cuando el agente tiene capacidad de ejecutar Python (como en Claude Code, Gemini Code, o similares):
- El script debe ser **completamente autocontenido**: import + load data + process + output en un solo bloque.
- Nunca asumir que variables de bloques anteriores persisten.
- Mostrar siempre el output real de la consola, no una descripción de lo que "debería" decir el output.
