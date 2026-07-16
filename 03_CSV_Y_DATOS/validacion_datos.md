# Validación de Datos y Contratos de Input

> Todo dato que entra al sistema debe ser validado antes de ser procesado. Los datos rotos producen resultados rotos.

---

## Contrato de Input

Antes de procesar cualquier archivo, el agente debe declarar explícitamente qué espera:

```markdown
## CONTRATO DE INPUT — [Nombre del Script]

| Campo | Tipo esperado | Nulos permitidos | Rango válido | Notas |
|-------|-------------|-------------------|-------------|-------|
| fecha | datetime | No | 2020-01-01 a hoy | Formato YYYY-MM-DD |
| canal | string (category) | No | Ver diccionario | Case-sensitive |
| revenue | float | No | > 0 | En USD |
| producto_id | int | No | 1 – 99999 | FK a tabla productos |
```

**El contrato se define antes de escribir el script.** No después de que el script falla.

---

## Script de Validación de Input (Template)

```python
import pandas as pd
from datetime import datetime

def validar_input(df: pd.DataFrame, nombre_archivo: str) -> bool:
    """Valida el DataFrame contra el contrato de input. Retorna True si pasa."""
    errores = []
    
    # 1. Columnas obligatorias
    cols_requeridas = ['fecha', 'canal', 'revenue', 'producto_id']
    cols_faltantes = [c for c in cols_requeridas if c not in df.columns]
    if cols_faltantes:
        errores.append(f"Columnas faltantes: {cols_faltantes}")
    
    # 2. Tipos de datos
    if 'revenue' in df.columns:
        if not pd.api.types.is_numeric_dtype(df['revenue']):
            errores.append("'revenue' no es numérico")
    
    # 3. Nulos en columnas críticas
    for col in ['fecha', 'canal', 'revenue']:
        if col in df.columns and df[col].isnull().any():
            errores.append(f"'{col}' tiene {df[col].isnull().sum()} nulos")
    
    # 4. Valores negativos donde no corresponde
    if 'revenue' in df.columns and (df['revenue'] < 0).any():
        errores.append(f"revenue negativo en {(df['revenue'] < 0).sum()} filas")
    
    # Reporte final
    if errores:
        print(f"❌ VALIDACIÓN FALLIDA para '{nombre_archivo}':")
        for e in errores:
            print(f"  • {e}")
        print("ACCIÓN: Corregir el input antes de continuar.")
        return False
    else:
        print(f"✅ VALIDACIÓN PASADA para '{nombre_archivo}' ({len(df):,} filas)")
        return True

# Uso:
df = pd.read_csv('datos.csv', encoding='utf-8')
if not validar_input(df, 'datos.csv'):
    raise SystemExit("Input inválido. No se puede continuar.")
```

---

## Manejo de Encodings

Los CSVs en entornos corporativos latinoamericanos suelen tener problemas de encoding:

```python
def leer_csv_seguro(path: str) -> pd.DataFrame:
    """Intenta leer un CSV con múltiples encodings. Retorna el DataFrame o lanza error claro."""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc, low_memory=False)
            print(f"✅ CSV leído con encoding: {enc}")
            return df
        except (UnicodeDecodeError, Exception):
            continue
    
    raise ValueError(f"No se pudo leer '{path}' con ninguno de los encodings probados: {encodings}")
```

---

## Detectar Cambios de Schema

Cuando un CSV que antes funcionaba ahora falla:

```python
def verificar_schema(df_nuevo: pd.DataFrame, cols_esperadas: list, dtypes_esperados: dict) -> None:
    """Detecta si el schema del CSV cambió respecto a lo esperado."""
    # Columnas nuevas (pueden ser inofensivas o problemáticas)
    cols_nuevas = set(df_nuevo.columns) - set(cols_esperadas)
    if cols_nuevas:
        print(f"⚠️  Columnas nuevas detectadas (no esperadas): {cols_nuevas}")
    
    # Columnas desaparecidas (PROBLEMA CRÍTICO)
    cols_perdidas = set(cols_esperadas) - set(df_nuevo.columns)
    if cols_perdidas:
        raise ValueError(f"❌ SCHEMA ROTO: Faltan columnas críticas: {cols_perdidas}")
    
    # Cambio de tipos
    for col, dtype_esperado in dtypes_esperados.items():
        if col in df_nuevo.columns:
            dtype_actual = str(df_nuevo[col].dtype)
            if dtype_actual != dtype_esperado:
                print(f"⚠️  '{col}': tipo cambió de '{dtype_esperado}' a '{dtype_actual}'")
```

---

## Principio de Desconfianza por Defecto

Todo dato externo debe ser considerado potencialmente roto hasta que la validación lo confirme.

- No asumir que un CSV que funcionaba la semana pasada tiene el mismo schema hoy.
- No asumir que los valores de una columna `canal` son los mismos de siempre (pueden haberse agregado nuevos).
- No asumir que las fechas están en el formato documentado (verificar siempre).
