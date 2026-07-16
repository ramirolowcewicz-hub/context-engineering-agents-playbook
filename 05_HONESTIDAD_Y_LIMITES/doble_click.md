# Capacidad de Doble Click — Profundización Conversacional

> Un agente conversacional de calidad no solo responde preguntas: sabe cuándo una respuesta merece más profundidad y cómo ofrecer ese nivel sin abrumar.

---

## ¿Qué es el "Doble Click"?

En el contexto de agentes conversacionales, el "doble click" es la capacidad de:

1. **Detectar** cuándo una respuesta superficial no es suficiente.
2. **Ofrecer activamente** ir más profundo sin que el usuario tenga que pedirlo explícitamente.
3. **Desglosar** un concepto complejo en sus capas cuando el usuario quiere entender mejor.
4. **Conectar** la respuesta puntual con el sistema más amplio.

---

## Cuándo Activar el Doble Click

### Señales de que el usuario quiere más profundidad:
- Pregunta "por qué" después de una respuesta.
- Repite una pregunta ligeramente distinta (indicó que la respuesta anterior no fue suficiente).
- Responde con "entiendo" seguido de una pregunta relacionada.
- Hace una pregunta sobre un término que apareció en la respuesta anterior.
- La pregunta contiene "pero, ¿como...?", "¿y si...?", "¿qué pasa cuando...?"

### Señales de que el usuario quiere brevedad:
- Preguntas de sí/no.
- "Dame solo el número".
- "Resumido".
- El tono de la conversación es rápido y transaccional.

---

## Cómo Implementar el Doble Click

### Patrón 1: Respuesta Modular con Opción de Profundizar

```
[Respuesta directa a la pregunta]

→ Si querés profundizar en alguno de estos puntos, deciéndome cuál:
  A. [Aspecto 1 que se pudo desarrollar más]
  B. [Aspecto 2]
  C. [Aspecto 3]
```

### Patrón 2: Respuesta en Capas

```
Capa 1 (resumen): [Respuesta en 1-2 oraciones]
Capa 2 (detalle): [Expansión con contexto]
Capa 3 (implicancias): [Qué significa esto para el sistema más amplio]

Decime en qué capa necesitás estar.
```

### Patrón 3: Conectar con el Sistema

Despues de responder algo puntual, si tiene relevancia sistémica:
```
[Respuesta puntual]

Nota: Esto conecta con [concepto más amplio]. ¿Es relevante explorarlo?
```

---

## Lo que el Doble Click NO es

- **No es abrumar con información no pedida.** Ofrecer la profundidad, no imponerla.
- **No es saltar sin confirmación.** Si el usuario no pidió profundidad, preguntar antes.
- **No es cambiar de tema.** El doble click es sobre el mismo tema, más profundo.
- **No es compensar incertidumbre con volumen.** Más palabras no reemplazan más certeza.

---

## El Doble Click en Modo Analítico (CSV)

Cuando el agente analiza datos, el doble click toma esta forma:

```
Resultado de primer nivel:
• Revenue total julio: $1,234,567 [script]

¿Querés hacer doble click en alguno de estos?
→ A. Desglosar por canal
→ B. Comparar con junio
→ C. Ver los 10 productos con mayor contribución
→ D. Analizar la variación día a día
```

Esto convierte un resultado plano en una conversación explorativa que multiplica el valor del análisis.

---

## El Doble Click en Modo Código

Cuando el agente entrega código, el doble click puede ser:

```
[Código entregado]

Si querés, puedo desarrollar:
→ A. Tests unitarios para este script
→ B. Manejo de errores más robusto para edge cases
→ C. Versión optimizada para mayor volumen de datos
→ D. Documentación y comentarios del script
```

---

## Principio de Economia del Doble Click

No ofrecer doble click en:
- Respuestas a preguntas factuales simples con una sola respuesta correcta.
- Tareas que el usuario claramente ya entiende.
- Conversaciones donde el usuario explicitamente pide brevedad.

Ofrecer doble click en:
- Resultados de análisis que pueden tener múltiples ángulos.
- Conceptos que tienen implicancias prácticas más allá de la pregunta puntual.
- Cuando el resultado en el primer nivel sugiere anomalías que merecen investigación.
