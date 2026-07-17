# Manejo de CSVs Grandes

> Para archivos grandes, el LLM nunca procesa los datos directamente. Siempre delegar a código.
> Versión: 1.1 — Agrega profiling, chunking por MB, check de RAM y idempotencia.

---

## ¿Qué es un CSV "grande"?

| Tamaño | Filas aprox. | Estrategia |
|--------|-------------|------------|
| < 10 MB | < 100,000 filas | Carga directa |
| 10 – 100 MB | 100,000 – 1,000,000 filas | **Chunking 10,000 filas** |
| 100 MB – 1 GB | 1M – 10M filas | **Chunking 50,000 filas + streaming** |
| > 1 GB | > 10M filas | **Particionado por archivo** |

**Regla práctica:** Si el usuario comparte un CSV y no sabés el tamaño, lo primero que hace el script es imprimir `shape` y verificar memoria.

---

## Protocolo de Primer Contacto con un CSV

Cada vez que se recibe un CSV por primera vez, ejecutar este diagnóstico antes de cualquier análisis:

```python
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

RUTA_CSV = 'archivo.csv'
ENCODINGS = ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1', 'cp1252']

# 1. Leer con fallback de encoding
df = None
for enc in ENCODINGS:
    try:
        df = pd.read_csv(RUTA_CSV, encoding=enc, low_memory=False)
        print(f'✅ Leído con encoding: {enc}')
        break
    except (UnicodeDecodeError, Exception):
        continue

if df is None:
    print(f'❌ No se pudo leer con ningún encoding: {ENCODINGS}')
    sys.exit(1)

# 2. Diagnóstico completo
nulos = df.isnull().sum()
nulos_reporte = nulos[nulos > 0].to_string() if nulos.any() else 'Ninguno'
mem_mb = df.memory_usage(deep=True).sum() / 1024**2

diag = f"""
===== DIAGNÓSTICO INICIAL — {Path(RUTA_CSV).name} =====
Ejecutado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SHAPE:
  Filas:    {df.shape[0]:,}
  Columnas: {df.shape[1]}
  Memoria:  {mem_mb:.2f} MB

COLUMNAS Y TIPOS:
{df.dtypes.to_string()}

VALORES NULOS:
{nulos_reporte}

ESTADÍSTICAS BÁSICAS (numéricas):
{df.describe().to_string()}

MUESTRA (primeras 3 filas):
{df.head(3).to_string()}
{'='*50}
"""
print(diag)
```

**El diagnóstico se muestra al usuario antes de cualquier análisis.**

---

## Estrategias según Tamaño

### Estrategia 1: Leer solo las columnas necesarias
```python
cols_necesarias = ['fecha', 'canal', 'revenue', 'producto']
df = pd.read_csv('archivo.csv', usecols=cols_necesarias, encoding='utf-8')
```

### Estrategia 2: Chunking para agregaciones
```python
import pandas as pd

CHUNK_SIZE = 10_000  # Ajustar según RAM disponible
resultados = []

for i, chunk in enumerate(pd.read_csv('archivo.csv', chunksize=CHUNK_SIZE, encoding='utf-8')):
    # Check de RAM en cada chunk
    import psutil
    if psutil.virtual_memory().percent > 80:
        print(f"ALERTA: RAM al {psutil.virtual_memory().percent:.0f}%. Reduciendo chunk.")
        break
    resultado_chunk = chunk.groupby('canal')['revenue'].sum()
    resultados.append(resultado_chunk)
    if i % 10 == 0:
        print(f"  Procesados {(i+1)*CHUNK_SIZE:,} registros...")

resultado_final = pd.concat(resultados).groupby(level=0).sum()
print(resultado_final)
```

### Estrategia 3: Tipado explícito para reducir memoria (hasta 70%)
```python
dtypes = {
    'id': 'int32',           # en vez de int64
    'canal': 'category',     # para strings repetitivos (gran reducción)
    'revenue': 'float32',    # en vez de float64
    'activo': 'bool'
}
df = pd.read_csv('archivo.csv', dtype=dtypes, encoding='utf-8')
print(f"Memoria con tipado explícito: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
```

### Estrategia 4: Profiling rápido con muestra (sin cargar todo)
```python
def profile_csv(filepath: str, sample_size: int = 5000) -> dict:
    """Perfila el CSV con una muestra sin cargarlo completo en RAM."""
    df_sample = pd.read_csv(filepath, nrows=sample_size, encoding='utf-8')
    total_rows = sum(1 for _ in open(filepath)) - 1  # -1 por el header
    
    profile = {
        "filepath": filepath,
        "total_rows_estimado": total_rows,
        "columnas": len(df_sample.columns),
        "columnas_con_nulos": [
            {"col": c, "pct_nulos": df_sample[c].isnull().mean() * 100}
            for c in df_sample.columns if df_sample[c].isnull().any()
        ],
        "tipos": df_sample.dtypes.to_dict()
    }
    return profile
```

---

## Validaciones Obligatorias Antes de Calcular

```python
# 1. Sin duplicados inesperados
assert df.duplicated().sum() == 0, f"ALERTA: {df.duplicated().sum()} filas duplicadas"

# 2. Columnas clave sin nulos
for col in ['fecha', 'canal', 'revenue']:
    nulos = df[col].isnull().sum()
    if nulos > 0:
        print(f"ALERTA: {nulos} valores nulos en '{col}'")
        # Decidir explícitamente: dropna, fillna(0), o reportar al usuario

# 3. Rango de fechas verificado
df['fecha'] = pd.to_datetime(df['fecha'])
print(f"Rango de fechas: {df['fecha'].min()} — {df['fecha'].max()}")

# 4. Valores numéricos en rango lógico
if (df['revenue'] < 0).any():
    print(f"ALERTA: {(df['revenue'] < 0).sum()} filas con revenue negativo")
```

---

## Inferencia Segura desde el Nombre del Archivo

```python
import re
from pathlib import Path

nombre = Path('ventas_julio_2026_v2.csv').stem  # 'ventas_julio_2026_v2'

# Extraer año-mes si está en el nombre
match = re.search(r'(\d{4})_(\d{2})', nombre)
if match:
    anio, mes = match.groups()
    print(f"[HECHO] Período inferido del nombre: {anio}-{mes} | confianza: alta")
else:
    print("[DESCONOCIDO] No se pudo inferir el período del nombre. Verificar con el usuario.")
```

**Por qué:** Es más confiable que buscar el `max()` de una columna de fechas que podría estar rota.

---

## Output Seguro de Resultados Numéricos

```python
# SIEMPRE marcar los números como [CÁLCULO] y mostrar su procedencia
print(f"""
[CÁLCULO] Revenue total: ${revenue_total:,.2f}
fuente: script main.py, groupby().sum() | confianza: alta
• Filas procesadas: {len(df):,}
• Período: {df['fecha'].min().strftime('%Y-%m-%d')} → {df['fecha'].max().strftime('%Y-%m-%d')}
• Canales incluidos: {df['canal'].nunique()} únicos
""")
```

---

## Kill-Switches de Procesamiento

```python
import psutil, time

# KS-RAM: abortar si se supera el 80% de RAM
if psutil.virtual_memory().percent > 80:
    raise MemoryError("Proceso abortado: RAM > 80%. Usar chunking o columnas selectivas.")

# KS-TIEMPO: abortar si supera 5 minutos
if time.time() - start_time > 300:
    raise TimeoutError("Proceso abortado: superó 5 minutos de ejecución.")

# KS-OUTPUT-VACÍO: abortar si el resultado está vacío
if len(resultado) == 0:
    raise ValueError("El resultado está vacío. Verificar filtros y datos de entrada.")
```
