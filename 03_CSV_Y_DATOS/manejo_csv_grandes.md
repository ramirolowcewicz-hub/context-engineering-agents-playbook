# Manejo de CSVs Grandes

> Para archivos grandes, el LLM nunca procesa los datos directamente. Siempre delegar a código.

---

## ¿Qué es un CSV "grande"?

| Tamaño | Filas aprox. | Modo recomendado |
|--------|-------------|------------------|
| < 100 KB | < 2,000 filas | Analista puede leer si son pocas columnas |
| 100 KB – 5 MB | 2,000 – 100,000 filas | **Orquestador obligatorio** |
| > 5 MB | > 100,000 filas | Orquestador + chunking |
| > 100 MB | > 1,000,000 filas | Orquestador + chunking + columnas selectivas |

**Regla práctica:** Si el usuario comparte un CSV y no sabés el tamaño, lo primero que hace el script es imprimir `shape` y `dtypes`.

---

## Protocolo de Primer Contacto con un CSV

Cada vez que se recibe un CSV por primera vez, ejecutar este diagnóstico antes de cualquier análisis:

```python
import pandas as pd

# SIEMPRE especificar dtypes si se conocen de antemano
# SIEMPRE usar encoding='utf-8' como default; si falla, probar 'latin-1'
df = pd.read_csv('archivo.csv', encoding='utf-8', low_memory=False)

diag = f"""
===== DIAGNÓSTICO INICIAL =====
Shape:          {df.shape[0]:,} filas x {df.shape[1]} columnas
Tamaño memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB

Columnas y tipos:
{df.dtypes.to_string()}

Valores nulos por columna:
{df.isnull().sum()[df.isnull().sum() > 0].to_string() if df.isnull().sum().any() else 'Ninguno'}

Muestra (primeras 3 filas):
{df.head(3).to_string()}
================================
"""
print(diag)
```

**El diagnóstico se muestra al usuario antes de cualquier análisis.**

---

## Estrategias para CSVs Muy Grandes (>50MB)

### Estrategia 1: Leer solo las columnas necesarias
```python
# NO: pd.read_csv('archivo.csv')  ← carga todo en RAM
# SÍ:
cols_necesarias = ['fecha', 'canal', 'revenue', 'producto']
df = pd.read_csv('archivo.csv', usecols=cols_necesarias, encoding='utf-8')
```

### Estrategia 2: Chunking para agregaciones
```python
import pandas as pd

chunk_size = 100_000
resultados = []

for chunk in pd.read_csv('archivo.csv', chunksize=chunk_size, encoding='utf-8'):
    # Procesar cada chunk, agregar solo el resultado
    resultado_chunk = chunk.groupby('canal')['revenue'].sum()
    resultados.append(resultado_chunk)

# Combinar todos los resultados
resultado_final = pd.concat(resultados).groupby(level=0).sum()
print(resultado_final)
```

### Estrategia 3: Tipado explícito para reducir memoria
```python
dtypes = {
    'id': 'int32',          # en vez de int64
    'canal': 'category',    # para strings repetitivos
    'revenue': 'float32',   # en vez de float64
    'activo': 'bool'
}
df = pd.read_csv('archivo.csv', dtype=dtypes, encoding='utf-8')
# El tipado correcto puede reducir el uso de RAM hasta un 70%
```

---

## Validaciones Obligatorias Antes de Calcular

Antes de cualquier cálculo que va a ir a un reporte:

```python
# 1. Verificar que no hay duplicados inesperados
assert df.duplicated().sum() == 0, f"ALERTA: {df.duplicated().sum()} filas duplicadas"

# 2. Verificar que las columnas clave no tienen nulos
for col in ['fecha', 'canal', 'revenue']:
    nulos = df[col].isnull().sum()
    if nulos > 0:
        print(f"ALERTA: {nulos} valores nulos en columna '{col}'")
        # Decidir explícitamente qué hacer: dropna, fillna, o reportar al usuario

# 3. Verificar rangos de fechas
df['fecha'] = pd.to_datetime(df['fecha'])
print(f"Rango de fechas: {df['fecha'].min()} hasta {df['fecha'].max()}")

# 4. Verificar que los valores numéricos son positivos (si aplica)
if (df['revenue'] < 0).any():
    print(f"ALERTA: {(df['revenue'] < 0).sum()} filas con revenue negativo")
```

---

## Inferencia de Contexto desde el Nombre del Archivo

Una técnica segura: extraer metadatos del nombre del archivo en vez de asumir o buscar en el contenido.

```python
import re
from pathlib import Path

nombre = Path('ventas_julio_2026_v2.csv').stem  # 'ventas_julio_2026_v2'

# Extraer fecha si está en el nombre
match = re.search(r'(\d{4})_(\d{2})', nombre)  # YYYY_MM
if match:
    anio, mes = match.groups()
    print(f"Período inferido del nombre: {anio}-{mes}")
else:
    print("No se pudo inferir período del nombre. Verificar manualmente.")
```

**Por qué:** Es más confiable que buscar el `max()` de una columna de fechas que podría estar rota, truncada o no actualizada.

---

## Output Seguro de Resultados Numéricos

Cuando el agente reporta números al usuario:

```python
# Siempre mostrar:
# 1. El número calculado
# 2. De cuántas filas se calculó
# 3. El rango de fechas cubierto

print(f"""
RESULTADO VERIFICADO (calculado por script, no estimado):
• Revenue total: ${revenue_total:,.2f}
• Filas procesadas: {len(df):,}
• Período: {df['fecha'].min().strftime('%Y-%m-%d')} a {df['fecha'].max().strftime('%Y-%m-%d')}
• Canales incluidos: {df['canal'].nunique()} únicos
""")
```
