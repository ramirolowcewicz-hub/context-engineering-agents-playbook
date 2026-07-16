# Anti-Alucinación Numérica

> Los LLMs pueden alucinar números con total confianza. Este archivo define cómo eliminar ese riesgo.

---

## El Problema

Cuando un LLM lee una tabla con cientos de filas e intenta sumar, promediar o agrupar, puede:
- Omitir filas silenciosamente.
- Calcular promedios incorrectos.
- Inventar totales "plausibles" que no coinciden con los datos reales.
- Reportar el resultado con total confianza, sin advertencia de error.

**Este riesgo es mayor cuando:**
- El CSV es grande (el LLM no puede "ver" todas las filas en su contexto).
- Los números tienen muchos decimales.
- Hay valores nulos que el LLM ignora silenciosamente.
- Hay distintas unidades mezcladas (USD vs. ARS, por ejemplo).

---

## La Regla de Oro

> **Todo número que va a un reporte, una decisión de negocio o una presentación debe venir de un script, nunca del razonamiento nativo del LLM.**

---

## Cómo Marcar la Procedencia de un Número

En cada output que contenga números, el agente debe indicar de dónde viene cada dato:

```
✅ Revenue total: $1,234,567.89  [calculado por script — confiable]
⚠️  Tendencia: parece estar subiendo en el último mes  [estimación LLM — validar]
❌ Nunca: "El revenue total fue aproximadamente $1.2M" sin indicar cómo se obtuvo
```

---

## Checklist Anti-Alucinación para Outputs Numéricos

```
☐ ¿El número viene de un script Python/SQL que procesó los datos reales?
☐ ¿Se mostró cuántas filas se procesaron?
☐ ¿Se validó que no había nulos ni duplicados que distorsionen el resultado?
☐ ¿Se verificó el rango de fechas del dataset procesado?
☐ ¿El resultado tiene sentido de orden de magnitud? (Sanity check)
☐ ¿Se marcó explícitamente si algún número es una estimación, no un cálculo?
```

---

## Sanity Checks Obligatorios

Antes de reportar cualquier KPI:

```python
# Sanity check 1: El total no puede ser 0 si el dataset tiene datos
assert revenue_total > 0, "ALERTA: Revenue total es 0 o negativo. Verificar filtros."

# Sanity check 2: Los promedios deben estar dentro de rangos lógicos
assert 0 < revenue_promedio < revenue_total, "El promedio no puede ser mayor que el total"

# Sanity check 3: La suma de partes debe igualar el total
total_por_canal = df.groupby('canal')['revenue'].sum().sum()
diff = abs(total_por_canal - revenue_total)
assert diff < 0.01, f"Discrepancia entre total y suma por canal: {diff}"

# Sanity check 4: Las fechas están en el rango esperado
if fecha_inicio_esperada and fecha_fin_esperada:
    assert df['fecha'].min() >= fecha_inicio_esperada, "Datos fuera del rango esperado"
```

---

## Qué Hacer Cuando el Agente No Puede Calcular

Si el agente no tiene acceso a ejecutar código y el usuario pide un cálculo sobre datos grandes:

```
Respuesta correcta:
"Para calcular este número correctamente necesito ejecutar un script sobre el CSV.
 No puedo darte este número con precisión desde el contexto de la conversación.
 ¿Podés darme acceso a ejecutar código o ejecutar este script de tu lado?

 [INCLUIR EL SCRIPT LISTO PARA EJECUTAR]"

Respuesta incorrecta:
"El revenue total aproximado es $1.2M" (sin script, sin evidencia)
```

---

## Unidades y Monedas

- Siempre declarar la unidad de cada métrica.
- Si el CSV mezcla monedas (ARS, USD, BRL), documentarlo antes de sumar.
- Nunca sumar valores en distintas monedas sin conversión explícita y documentada.
- Si la columna de moneda no existe en el CSV: preguntar antes de calcular totales.
