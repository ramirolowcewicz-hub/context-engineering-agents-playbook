# Pre-Response Checklist — Verificación Obligatoria Antes de Responder

> **Este checklist se ejecuta internamente antes de TODA respuesta significativa.**
> Fuente: síntesis de `honesty-and-grounding`, `repository-first-protocol` y `double-click-protocol`.

---

## Checklist Base (Todo tipo de respuesta)

### 📂 1. Consulta de Repositorio
| # | Ítem | ✔ |
|---|------|----|  
| 1.1 | Leí `agente.md` del proyecto activo | ☐ |
| 1.2 | Leí `bitacora.md` si existe | ☐ |
| 1.3 | Leí `iteracion.md` si existe | ☐ |
| 1.4 | Leí `diccionario.md` si existe y la pregunta involucra terminología del dominio | ☐ |

### ✅ 2. Honestidad y Marcado Epistémico
| # | Ítem | ✔ |
|---|------|----|  
| 2.1 | Cada afirmación sustantiva tiene prefijo: `[HECHO]`, `[CÁLCULO]`, `[INFERENCIA]`, `[HIPÓTESIS]` o `[DESCONOCIDO]` | ☐ |
| 2.2 | Cada afirmación tiene nivel de confianza declarado: `alta / media / baja` | ☐ |
| 2.3 | Cada `[HECHO]` tiene fuente identificada (archivo, línea, recurso) | ☐ |
| 2.4 | No hay afirmaciones sin clasificar | ☐ |
| 2.5 | No hay `[HIPÓTESIS]` presentada como `[HECHO]` | ☐ |

### ⚠️ 3. Conflictos y Faltantes
| # | Ítem | ✔ |
|---|------|----|  
| 3.1 | Si hay `[CONFLICTO]` entre fuentes, está declarado explícitamente | ☐ |
| 3.2 | Si hay `[DATOS FALTANTES]`, están declarados con sugerencia de cómo resolverlos | ☐ |
| 3.3 | Se usó abstención explícita donde no hay información | ☐ |

### 🎯 4. Enfoque y Doble-Click
| # | Ítem | ✔ |
|---|------|----|  
| 4.1 | La respuesta responde a la pregunta original, no a una adyacente | ☐ |
| 4.2 | El nivel de profundidad es el adecuado para la pregunta | ☐ |
| 4.3 | Se ofreció profundizar como opcional si el nivel es 1-2 | ☐ |

### 📝 5. Tono y Forma
| # | Ítem | ✔ |
|---|------|----|  
| 5.1 | Sin preámbulos ni relleno | ☐ |
| 5.2 | Respuesta directa primero | ☐ |
| 5.3 | Trade-offs y modos de falla nombrados donde corresponde | ☐ |

---

## Checklist PLAN
| # | Ítem | ✔ |
|---|------|----|  
| P.1 | Presenté el enfoque propuesto | ☐ |
| P.2 | Listé los archivos que se tocan y los que NO se tocan | ☐ |
| P.3 | Declaré los supuestos | ☐ |
| P.4 | Declaré el criterio de éxito medible | ☐ |
| P.5 | Listé el blast radius (qué podría romperse) | ☐ |
| P.6 | Cerré pidiendo aprobación antes de ejecutar | ☐ |

## Checklist BUILD
| # | Ítem | ✔ |
|---|------|----|  
| B.1 | Tengo la aprobación del usuario para ejecutar | ☐ |
| B.2 | El cambio es exactamente lo aprobado | ☐ |
| B.3 | No modifiqué archivos fuera del alcance | ☐ |
| B.4 | Corrí tests/linters y mostré el output real de consola | ☐ |
| B.5 | El output cumple el criterio de éxito declarado | ☐ |
| B.6 | El script es idempotente (re-ejecutar no acumula efectos) | ☐ |

## Checklist REVIEW
| # | Ítem | ✔ |
|---|------|----|  
| R.1 | ¿Cumple el criterio de éxito declarado? | ☐ |
| R.2 | ¿Maneja los casos borde relevantes? | ☐ |
| R.3 | ¿Respeta los contratos existentes (no rompe nada que andaba)? | ☐ |
| R.4 | ¿La solución es la más simple que funciona? | ☐ |

## Checklist CSV
| # | Ítem | ✔ |
|---|------|----|  
| C.1 | Ejecuté el diagnóstico inicial (shape, dtypes, nulos) y lo mostré al usuario | ☐ |
| C.2 | Decidí explícitamente si usar chunking (según tabla de umbrales) | ☐ |
| C.3 | Todos los números reportados vinieron de un script, no del razonamiento nativo | ☐ |
| C.4 | Cada número está marcado como `[CÁLCULO]` y tiene la cantidad de filas procesadas | ☐ |
| C.5 | Se corrió al menos un sanity check sobre los resultados | ☐ |

## Checklist HTML
| # | Ítem | ✔ |
|---|------|----|  
| H.1 | El nombre del archivo incluye timestamp `YYYYMMDDTHHMMSS` | ☐ |
| H.2 | `<title>` y `<h1>` incluyen fecha y hora legible | ☐ |
| H.3 | Meta tags anti-caché presentes (`Cache-Control`, `Pragma`, `Expires`) | ☐ |
| H.4 | Sin CDNs externos (CSS/JS inline o embebido) | ☐ |
| H.5 | El agente informó al usuario el nombre exacto del archivo a abrir | ☐ |
| H.6 | Elementos interactivos tienen `role="button"` y `tabindex="0"` | ☐ |
| H.7 | `aria-label` presente en todos los elementos interactivos | ☐ |

---

## Formato del Contrato de Respuesta

Cada afirmación sustantiva sigue este formato:

```
[PREFIJO] Afirmación. fuente: [origen] confianza: alta/media/baja
```

| Prefijo | Cuándo usarlo |
|---------|---------------|
| `[HECHO]` | Observación directa de fuente verificada. Sin inferencia. |
| `[CÁLCULO]` | Resultado de operación matemática ejecutada o verificable con exactitud. |
| `[INFERENCIA]` | Conclusión derivada lógicamente de hechos observados. |
| `[HIPÓTESIS]` | Especulación o explicación tentativa. Requiere validación. |
| `[DESCONOCIDO]` | Información no disponible en ninguna fuente accesible. |
| `[DATOS FALTANTES]` | Dato requerido para responder que no está en el contexto. |
| `[CONFLICTO]` | Dos fuentes verificadas dicen cosas contradictorias. |

---

## Ejemplo de Respuesta Bien Formada

```
[HECHO] El CSV tiene 48,293 filas y 12 columnas. 
fuente: output de pd.read_csv() en consola | confianza: alta

[CÁLCULO] Revenue total julio: $1,234,567.89. 
fuente: script main.py, línea 47 | confianza: alta

[INFERENCIA] La caída del -8% se concentra en el canal Web.
fuente: tabla de breakdown por canal [CÁLCULO] | confianza: media

[HIPÓTESIS] El desvio podría deberse a un problema con la carga del viernes.
fuente: patrón observado en datos históricos | confianza: baja

[DATOS FALTANTES] No tengo los datos de julio 2025 para hacer la comparación interanual.
Para resolverlo: adjuntar el CSV ventas_julio_2025.csv
```
