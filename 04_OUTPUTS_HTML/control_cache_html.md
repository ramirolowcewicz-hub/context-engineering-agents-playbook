# Control de Caché en Outputs HTML

> Este es uno de los problemas más frecuentes y frustrantes al trabajar con reportes HTML generados por agentes. Este archivo lo resuelve de raíz.

---

## El Problema

Cuando un agente genera un archivo HTML con un nombre fijo (ej: `reporte.html`) y el usuario lo abre en el browser:

1. El browser cachéa el archivo.
2. El agente genera una nueva versión del archivo con el mismo nombre.
3. El usuario abre el archivo nuevamente.
4. **El browser sirve la versión cacheada anterior, no la nueva.**
5. El usuario no ve los cambios y cree que el agente no los hizo.

Esto genera confusión, iteraciones inútiles y pérdida de confianza en el agente.

---

## La Solución Canónica: Timestamp en el Nombre del Archivo

**Regla absoluta:** Todo archivo de output HTML (y cualquier output que el usuario va a abrir en un browser) debe incluir fecha y hora de creación en el nombre.

```python
from datetime import datetime

# CORRECTO:
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
nombre_output = f"reporte_{timestamp}.html"  # ej: reporte_20260716_220606.html

# INCORRECTO (nunca hacer esto para outputs que el usuario abre):
nombre_output = "reporte.html"              # Se cachea
nombre_output = "reporte_julio.html"        # Sigue cacheando si se regenera el mismo día
nombre_output = "reporte_20260716.html"     # Caché problemático si hay más de una versión por día
```

---

## Patrón de Naming Completo

```python
from datetime import datetime
from pathlib import Path

def generar_nombre_output(prefijo: str, extension: str = 'html') -> str:
    """
    Genera un nombre de archivo con timestamp que garantiza unicidad.
    
    Ejemplo: generar_nombre_output('reporte_ventas') 
    Output:  'reporte_ventas_20260716_220606.html'
    """
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefijo}_{ts}.{extension}"

# Uso:
nombre = generar_nombre_output('analisis_canales')
path_output = Path('outputs') / nombre
print(f"Generando: {path_output}")
```

---

## Meta-Tags Anti-Caché en el HTML

Además del naming con timestamp, incluir estos meta-tags dentro del `<head>` del HTML generado:

```html
<head>
  <meta charset="UTF-8">
  <!-- Anti-caché: fuerza al browser a no cachear este archivo -->
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  
  <!-- Siempre incluir la fecha de generación visible en el título -->
  <title>Reporte Ventas — Generado: {timestamp_legible}</title>
</head>
```

---

## Timestamp Visible en el Cuerpo del HTML

El archivo HTML debe mostrar claramente cuándo fue generado. Esto permite al usuario verificar que está viendo la versión correcta:

```python
from datetime import datetime

timestamp_legible = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

html_header = f"""
<div class="metadata" style="
    background: #f0f0f0; 
    padding: 8px 16px; 
    font-size: 12px; 
    color: #666;
    border-bottom: 1px solid #ddd;
    font-family: monospace;
">
    ⏱️ Reporte generado el: <strong>{timestamp_legible}</strong> &nbsp;|
    Filas procesadas: <strong>{filas_procesadas:,}</strong> &nbsp;|
    Archivo: <strong>{nombre_output}</strong>
</div>
"""
```

---

## Limpieza de Outputs Anteriores (Opcional pero Recomendado)

```python
import glob
import os
from pathlib import Path

def limpiar_outputs_anteriores(patron: str, directorio: str = '.', mantener_ultimos: int = 5):
    """
    Mantiene solo los N archivos más recientes que coincidan con el patrón.
    Evita acumulación de versiones antiguas.
    
    Ejemplo: limpiar_outputs_anteriores('reporte_ventas_*.html')
    """
    archivos = sorted(
        glob.glob(os.path.join(directorio, patron)),
        key=os.path.getmtime,
        reverse=True
    )
    
    if len(archivos) > mantener_ultimos:
        para_borrar = archivos[mantener_ultimos:]
        for archivo in para_borrar:
            os.remove(archivo)
            print(f"  Eliminado: {archivo}")
        print(f"  Mantenidos: {mantener_ultimos} archivos más recientes")
```

---

## Checklist de Output HTML

```
☐ El nombre del archivo incluye timestamp (YYYYMMDD_HHMMSS)
☐ El <head> incluye meta-tags anti-caché
☐ El <title> incluye fecha y hora de generación
☐ El cuerpo muestra visiblemente cuándo fue generado
☐ El agente imprime en consola el nombre exacto del archivo generado
☐ El agente informa al usuario: "Abrir el archivo [NOMBRE EXACTO] para ver los cambios"
```

---

## Cómo Informar al Usuario

Al terminar de generar un HTML, el agente siempre debe comunicar:

```
✅ Output generado exitosamente:
• Archivo: reporte_ventas_20260716_220606.html
• Tamaño: 45 KB
• Generado: 16/07/2026 22:06:06

⚠️  Si tenés abierta una versión anterior en el browser, abrí este nuevo archivo 
por su nombre exacto. No recargues el anterior (puede estar cacheado).
```
