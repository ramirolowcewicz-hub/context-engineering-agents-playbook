# Data Contracts — Contratos Formales de Datos

> Todo paso entre el CSV crudo y el output final se define con un contrato explícito.
> Los contratos son la diferencia entre un pipeline confiable y uno que falla silenciosamente.

---

## Qué es un Contrato de Datos

Un contrato de datos define explícitamente:
- **Input**: qué columnas se esperan, con qué tipos y qué restricciones.
- **Operación**: qué transformación se aplica.
- **Output**: qué columnas produce, con qué tipos.

Sin contrato, un cambio en el CSV rompe el pipeline sin warning claro.

---

## Formato del Contrato (Markdown)

```markdown
## CONTRATO DE DATOS — [Nombre del Script / Operación]

Versión: 1.0 | Fecha: YYYY-MM-DD

### INPUT
| Columna | Tipo esperado | Nulos permitidos | Rango válido | Notas |
|---------|-------------|-----------------|-------------|-------|
| fecha | datetime | No | 2020-01-01 a hoy | Formato YYYY-MM-DD |
| canal | string (category) | No | Ver diccionario.md | Case-sensitive |
| revenue | float | No | > 0 | En USD |
| producto_id | int | No | 1 – 99999 | FK a tabla productos |

### OPERACIÓN
Agrupación por canal, suma de revenue, filtrado por rango de fechas.

### OUTPUT
| Columna | Tipo | Notas |
|---------|------|-------|
| canal | string | Igual que input |
| revenue_total | float | Suma del período |
| pct_del_total | float | 0.0 – 100.0 |

### CRITERIO DE ÉXITO
- Revenue total output ≤ Revenue total input (suma parcial, no puede ser mayor)
- pct_del_total de todos los canales suma 100.0 (±0.01 por redondeo)
- Filas output ≤ Filas input (agregación reduce filas)
```

---

## Esquema JSON (Para Validación Programmática)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DataContract",
  "type": "object",
  "required": ["version", "operation", "input", "output"],
  "properties": {
    "version": { "type": "string" },
    "operation": { "type": "string" },
    "input": {
      "type": "object",
      "required": ["source", "expected_columns"],
      "properties": {
        "source": { "type": "string" },
        "filters": { "type": "object" },
        "expected_columns": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "type"],
            "properties": {
              "name": { "type": "string" },
              "type": { "type": "string", "enum": ["string", "int", "float", "datetime", "bool", "category"] },
              "nullable": { "type": "boolean", "default": false },
              "min": {},
              "max": {}
            }
          }
        }
      }
    },
    "output": {
      "type": "object",
      "required": ["columns"],
      "properties": {
        "columns": { "type": "array", "items": { "type": "object" } }
      }
    }
  }
}
```

---

## Validador Python

```python
import pandas as pd
from typing import List, Dict, Any

def validate_contract(df: pd.DataFrame, contract: Dict[str, Any]) -> Dict:
    """
    Valida un DataFrame contra un contrato de datos.
    Retorna dict con {valid: bool, errors: list, warnings: list}.
    """
    errors = []
    warnings = []
    
    expected_cols = {c['name']: c for c in contract['input']['expected_columns']}
    
    # 1. Columnas faltantes (BLOCKER)
    missing = set(expected_cols.keys()) - set(df.columns)
    if missing:
        errors.append(f"[BLOCKER] Columnas faltantes: {sorted(missing)}")
    
    # 2. Columnas inesperadas (WARNING)
    unexpected = set(df.columns) - set(expected_cols.keys())
    if unexpected:
        warnings.append(f"[WARNING] Columnas no esperadas en el contrato: {sorted(unexpected)}")
    
    # 3. Tipos de datos (BLOCKER si critico)
    type_map = {'float': 'float64', 'int': 'int64', 'string': 'object', 'datetime': 'datetime64[ns]'}
    for col_name, col_spec in expected_cols.items():
        if col_name not in df.columns:
            continue
        expected_type = col_spec.get('type', '')
        actual_type = str(df[col_name].dtype)
        if expected_type == 'float' and not pd.api.types.is_numeric_dtype(df[col_name]):
            errors.append(f"[BLOCKER] '{col_name}': se esperaba numérico, es {actual_type}")
        if expected_type == 'datetime':
            try:
                pd.to_datetime(df[col_name].dropna().iloc[:5])
            except Exception:
                errors.append(f"[BLOCKER] '{col_name}': no se puede convertir a datetime")
    
    # 4. Nulos en columnas no-nullable (BLOCKER)
    for col_name, col_spec in expected_cols.items():
        if col_name not in df.columns:
            continue
        if not col_spec.get('nullable', False) and df[col_name].isnull().any():
            nulos = df[col_name].isnull().sum()
            errors.append(f"[BLOCKER] '{col_name}': {nulos} nulos en columna no-nullable")
    
    # Resumen
    valid = len(errors) == 0
    print(f"{'\u2705' if valid else '\u274c'} Validación del contrato: {'PASADA' if valid else 'FALLIDA'}")
    if errors:
        for e in errors: print(f"  {e}")
    if warnings:
        for w in warnings: print(f"  {w}")
    
    return {'valid': valid, 'errors': errors, 'warnings': warnings}
```

---

## Detección de Cambios de Schema

```python
def detectar_schema_drift(df_nuevo: pd.DataFrame, contrato: dict, nombre_archivo: str):
    """
    Detecta si el schema del CSV cambió respecto al contrato.
    Llama esto cuando un CSV que antes funcionaba ahora falla.
    """
    cols_esperadas = {c['name'] for c in contrato['input']['expected_columns']}
    cols_actuales = set(df_nuevo.columns)
    
    perdidas = cols_esperadas - cols_actuales
    nuevas = cols_actuales - cols_esperadas
    
    if perdidas:
        raise ValueError(f"❌ SCHEMA DRIFT DETECTADO en '{nombre_archivo}':\n"
                         f"  Columnas que desaparecieron: {sorted(perdidas)}\n"
                         f"  Esto rompe el contrato. Revisar el origen del CSV.")
    if nuevas:
        print(f"⚠️  Columnas nuevas en '{nombre_archivo}' (no estaban en el contrato): {sorted(nuevas)}\n"
              f"  Pueden ser inofensivas. Verificar si alguna reemplaza a una existente.")
```

---

## Principio de Versionado de Contratos

- Los contratos se versionar junto con los scripts (`v1.0`, `v1.1`, etc.).
- Un cambio de schema en el CSV que rompe el contrato requiere:
  1. Actualizar el contrato (nueva versión).
  2. Actualizar el script.
  3. Documentar en `bitacora.md` qué cambió y por qué.
- **Nunca silenciar un error de schema** para que el script "funcione" con datos incorrectos.
