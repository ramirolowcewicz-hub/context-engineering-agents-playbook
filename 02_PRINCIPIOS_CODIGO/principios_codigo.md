# Principios de Código

> Reglas duras de programación que aplican a todo código que el agente escribe o revisa.
> Fuente base: principios Karpathy + extensiones operativas.
> Versión: 1.1 — Agrega TDD, linters, blast radius, idempotencia y clasificación de hallazgos.

---

## Los 4 Principios Base (Karpathy)

### 1. THINK BEFORE CODING
Aclarar suposiciones antes de escribir. Si algo es ambiguo o tiene trade-offs no resueltos, preguntar.
**NUNCA asumir un default silencioso.**

> Aplicación práctica: Antes de escribir el primer import, declarar:
> - ¿Qué input espera este script?
> - ¿Qué output produce?
> - ¿Qué pasa si el input está mal formado?
> - ¿Cuál es el blast radius? (qué puede romperse)

### 2. SIMPLICITY FIRST
Escribir la solución más simple que funcione. Evitar sobre-ingeniería, abstracciones innecesarias o código defensivo para casos imposibles en el contexto del problema.

> Regla de oro: Si podés explicar lo que hace el código en una oración, es suficientemente simple.

### 3. SURGICAL CHANGES
Modificar estrictamente lo que la tarea requiere. Los diffs deben ser limpios y enfocados.

> Prohibido: *drive-by refactoring*. Si encontrás algo mejorable fuera del scope, documentálo. No lo toqueés ahora.

### 4. GOAL-DRIVEN
Toda tarea de programación debe tener un criterio de éxito explícito, medible y verificable antes de empezar.

> Formato: "El script tiene éxito si produce [OUTPUT X] dado [INPUT Y] sin errores en la consola."

---

## Reglas Duras de Cambios Quirúrgicos

- **NUNCA** modificar archivos no mencionados en la planificación de la tarea.
- **NUNCA** cambiar formato, estilo o nombres en código que no se está editando.
- **SIEMPRE** confirmar el alcance antes de editar más de 3 archivos en una misma iteración.
- **UN SOLO OBJETIVO** por cambio. Diffs pequeños, aislados y fácilmente revisables.
- **BLAST RADIUS DOCUMENTADO** antes de ejecutar cualquier cambio no trivial.

**Por qué esto importa:** Los cambios masivos y dispersos son el origen principal del colapso de calidad y la introducción de regresiones sobre código que ya funcionaba.

---

## Blast Radius

**Blast radius:** El conjunto de archivos, funciones y comportamientos que podrían verse afectados como consecuencia no intencional del cambio.

```
MAPEO DE BLAST RADIUS (antes de implementar):
• Archivos directamente modificados: [lista]
• Archivos que dependen de lo modificado: [lista]
• Comportamientos que podrían cambiar: [descripción]
• Plan de mitigación: [qué verificar después]
```

Si durante la implementación el blast radius es mayor al estimado: **pausar, documentar, pedir confirmación**.

---

## Reglas de Scripts Autocontenidos

Todo script que el agente escribe debe poder ejecutarse en un entorno Python limpio sin fallar.

**Checklist obligatorio antes de entregar un script:**

```
☐ ¿Empieza con todos los imports necesarios?
☐ ¿Carga o recrea todos los datos que usa?
☐ ¿No asume variables de ejecuciones anteriores?
☐ ¿Todo archivo referenciado está en el contexto actual?
☐ ¿Funcionaria en una sesión Python completamente nueva?
☐ ¿El script es idempotente? (re-ejecutar no acumula efectos)
```

---

## Idempotencia

**Regla:** Un script de producción debe poder ejecutarse múltiples veces con el mismo resultado.

```python
# ❌ NO idempotente: acumula filas en cada ejecución
with open("output.csv", "a") as f:
    f.write(row)

# ✅ Idempotente: sobrescribe
with open("output.csv", "w") as f:
    f.write(row)

# ✅ Idempotente con timestamp: cada ejecución genera un archivo nuevo
nombre = f"output_{datetime.now().strftime('%Y%m%dT%H%M%S')}.csv"
```

---

## TDD — Test-Driven Development

Cuando el criterio de éxito es automatizable: escribir la prueba antes del código.

**Secuencia:**
1. **Rojo:** Escribir la prueba que falla (el test define el comportamiento esperado).
2. **Verde:** Implementar el código mínimo que hace pasar la prueba.
3. **Refactor:** Mejorar el código sin romper la prueba.
4. **Evidencia:** Mostrar el output de pytest.

**Cuándo aplicar TDD:**
- ✅ El criterio de éxito es una aserción cuantificable.
- ✅ Se modifica una función pura con inputs/outputs bien definidos.
- ❌ El criterio es cualitativo ("debe verse bien").

```python
# Ejemplo:
def test_calcular_revenue_total():
    df = pd.DataFrame({'canal': ['Web', 'App'], 'revenue': [100.0, 200.0]})
    resultado = calcular_revenue_total(df)
    assert resultado == 300.0, f"Esperado 300.0, obtenido {resultado}"
    assert isinstance(resultado, float), "El resultado debe ser float"
```

---

## Clasificación de Hallazgos en REVIEW

En modo REVIEW, cada hallazgo se clasifica:

| Etiqueta | Significado | Acción requerida |
|----------|------------|-----------------|
| **BLOCKER** | Afecta corrección o requisitos. Bloquea el uso. | Corregir antes de cualquier avance. |
| **WARNING** | Potencial problema. No bloquea pero debe resolverse. | Corregir en follow-up o documentar. |
| **SUGGESTION** | Mejora opcional. No bloquea. | Aceptar o rechazar con justificación. |

**Solo reportar lo que afecta corrección o requisitos.** Nunca marcar BLOCKER algo que es preferencia de estilo.

---

## Linters y Análisis Estático

| Lenguaje | Linter recomendado | Cuándo correr |
|----------|-------------------|----------------|
| Python | `ruff` o `flake8` | Antes de entregar el script |
| SQL | `sqlfluff` | Antes de ejecutar en producción |
| JavaScript | `eslint` | Antes de cada commit |

**Regla de no-print en producción:** `print()` para debugging está permitido durante el desarrollo pero debe eliminarse (o convertirse a logging) antes de producción.

---

## Rollback

Antes de aplicar un cambio destructivo (DELETE, DROP, overwrite de archivo de producción):

```bash
# 1. Crear checkpoint
cp archivo_critico.py archivo_critico.py.bak

# 2. Aplicar el cambio
# 3. Ejecutar tests
# 4. Si falla: restaurar
cp archivo_critico.py.bak archivo_critico.py
```

---

## Disciplina en Dependencias

- Toda nueva librería o dependencia debe ser explícitamente justificada.
- No agregar dependencias para resolver algo que puede hacerse con la stdlib.
- Los accesos a credenciales, tokens y APIs requieren revisión y aprobación humana. Nunca hardcodear secrets.

---

## Evidencia de Funcionamiento

**No declarar que algo "funciona": probarlo con evidencia.**

```
→ Comando ejecutado: python main.py --input ventas_julio.csv
→ Output consola:
   [HECHO] Filas procesadas: 48,293
   [CÁLCULO] Revenue total: $1,234,567.89
   Output generado: reporte_20260716T220606.html
→ Tests: 5/5 passed in 0.34s
→ Criterio de éxito: PASADO ✔
```

---

## Paquetes Disponibles (Referencia Rápida)

```
Datos:          pandas, numpy, scipy, polars, tabulate
Visualización: altair, seaborn, plotly, matplotlib
ML/Stats:       scikit-learn, statsmodels, prophet
Office:         openpyxl, xlrd, python-docx, reportlab
Serialización:  pyyaml, jsonschema, lxml
Texto/NLP:      nltk, textblob
Geo/Red:        networkx, geopandas, folium
Imagen:         pillow, opencv-python
Cómputo:        numba, sympy
```

**NO intentar pip installs si el paquete no está disponible.** Informar al usuario y proponer alternativa con lo disponible.
