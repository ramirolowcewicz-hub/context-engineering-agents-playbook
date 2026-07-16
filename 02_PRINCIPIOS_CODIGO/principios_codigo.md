# Principios de Código

> Reglas duras de programación que aplican a todo código que el agente escribe o revisa.
> Fuente base: principios Karpathy + extensiones operativas propias.

---

## Los 4 Principios Base (Karpathy)

### 1. THINK BEFORE CODING
Aclarar suposiciones antes de escribir. Si algo es ambiguo o tiene trade-offs no resueltos, preguntar.
**NUNCA asumir un default silencioso.**

> Aplicación práctica: Antes de escribir el primer import, declarar:
> - ¿Qué input espera este script?
> - ¿Qué output produce?
> - ¿Qué pasa si el input está mal formado?

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

**Por qué esto importa:** Los cambios masivos y dispersos son el origen principal del colapso de calidad y la introducción de regresiones sobre código que ya funcionaba.

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
```

Si alguna respuesta es "no": reescribir el script completo antes de entregarlo.

---

## Disciplina en Dependencias

- Toda nueva librería o dependencia de software debe ser explícitamente justificada.
- No agregar dependencias para resolver algo que puede hacerse con la stdlib.
- Los accesos a credenciales, tokens y APIs requieren revisión y aprobación humana explícita. Nunca hardcodear secrets.

---

## Contratos de Código

Respetar estrictamente:
- Los tipos de datos de inputs y outputs.
- Los schemas de bases de datos existentes.
- Las firmas de funciones ya implementadas.

**Sin breaking changes** sin aprobación explícita.

---

## Evidencia de Funcionamiento

**No declarar que algo "funciona": probarlo con evidencia.**

Fomato de evidencia aceptable:
```
→ Comando ejecutado: python main.py --input ventas_julio.csv
→ Output consola:
   Filas procesadas: 48,293
   Columnas validadas: 12/12 ✔
   Revenue total: $1,234,567.89
   Output generado: reporte_20260716_220606.html
→ Criterio de éxito: PASADO
```

---

## Trade-off de Rigor

| Modo | Cuándo aplica | Nivel de proceso |
|------|--------------|------------------|
| Rigor completo | Scripts de producción, recurrentes, compartidos | Toda la secuencia gather→act→verify |
| Modo ágil | One-liners, prototipos desechables, PoCs | Plan informal, sin documentación |

**Ante la duda sobre en qué modo nos encontramos: asumir rigor completo.**

---

## Paquetes Disponibles (Referencia Rápida)

```
Datos:          pandas, numpy, scipy, polars, tabulate
Visualización: altair, seaborn, plotly, matplotlib
ML/Stats:       scikit-learn, statsmodels, prophet
Office:         openpyxl, xlrd, python-docx, reportlab
Serialization:  pyyaml, jsonschema, lxml
Texto/NLP:      nltk, textblob
Geo/Red:        networkx, geopandas, folium
Imagen:         pillow, opencv-python
Computo:        numba, sympy
```

**NO intentar pip installs si el paquete no está disponible.** Informar al usuario y proponer alternativa con lo disponible.
