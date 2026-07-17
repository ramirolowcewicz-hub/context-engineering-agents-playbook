# Control de Caché en Outputs HTML

> Versión: 1.1 — Agrega self-contained (sin CDNs), metadatos de versión y accesibilidad.

---

## El Problema

Cuando un agente genera un archivo HTML con un nombre fijo (ej: `reporte.html`) y el usuario lo abre en el browser:

1. El browser cachéa el archivo.
2. El agente genera una nueva versión con el mismo nombre.
3. El usuario abre el archivo nuevamente.
4. **El browser sirve la versión cacheada anterior, no la nueva.**
5. El usuario no ve los cambios y cree que el agente no los hizo.

Esto genera confusión, iteraciones inútiles y pérdida de confianza en el agente.

---

## La Solución Canónica: Timestamp UTC en el Nombre

**Regla absoluta:** Todo output HTML debe incluir timestamp en el nombre.

```python
from datetime import datetime, timezone

# CORRECTO — UTC ISO 8601 compacto (garantiza unicidad entre zonas horarias):
ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
nombre = f"reporte_ventas.{ts}.html"  # ej: reporte_ventas.20260716T220606.html

# También aceptable (timestamp local):
ts_local = datetime.now().strftime('%Y%m%d_%H%M%S')
nombre = f"reporte_ventas_{ts_local}.html"

# NUNCA (se cachea):
nombre = "reporte.html"
nombre = "reporte_julio.html"
nombre = "reporte_20260716.html"  # Sigue cacheando si hay > 1 versión por día
```

---

## Usar el Script Canónico

```bash
# Usar generate_artifact_name.py del playbook:
python3 scripts/generate_artifact_name.py html reporte_ventas
# Output: reporte-ventas.20260716T220606.html

# Con directorio:
python3 scripts/generate_artifact_name.py html reporte_ventas --output-dir ./outputs

# Ver los meta tags a incluir en el <head>:
python3 scripts/generate_artifact_name.py html reporte_ventas --meta-tags
```

---

## Estructura HTML Mínima Obligatoria

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- TÍTULO con fecha visible — permite identificar la versión sin abrir el archivo -->
  <title>Reporte Ventas — 16/07/2026 22:06:06 UTC</title>

  <!-- ANTI-CACHÉ: fuerza al browser a no cachear este archivo -->
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">

  <!-- METADATOS DE VERSIÓN: trazabilidad del artefacto -->
  <meta name="generator" content="nombre-agente/1.0">
  <meta name="artifact-version" content="1.0">
  <meta name="artifact-id" content="reporte-ventas.20260716T220606.html">
  <meta name="created" content="2026-07-16T22:06:06Z">

  <!-- CSS INLINE — SIN CDNs EXTERNOS (self-contained) -->
  <style>
    /* Todo el CSS va aquí, inline. NUNCA <link href="https://..."> */
    body { font-family: -apple-system, sans-serif; margin: 0; }
  </style>
</head>
<body>
  <!-- H1 VISIBLE con fecha — el usuario ve inmediatamente qué versión es -->
  <h1>Reporte Ventas — 16/07/2026 22:06:06 UTC</h1>

  <!-- JS INLINE — SIN CDNs EXTERNOS -->
  <script>
    /* Todo el JavaScript va aquí, inline. NUNCA <script src="https://..."> */
  </script>
</body>
</html>
```

---

## Regla Self-Contained (Sin CDNs Externos)

**Todo HTML generado por un agente debe ser completamente autocontenido.**

```html
<!-- ❌ NUNCA hacer esto: -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5...">
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

<!-- ✅ Siempre: CSS y JS inline o embebido -->
<style>
  /* El CSS completo aquí */
</style>
<script>
  /* El JS completo aquí */
</script>
```

**Por qué:** Un HTML con CDNs externos deja de funcionar sin conexión a internet y puede tener problemas de versioning cuando cambia el CDN.

---

## Timestamp Visible en el Cuerpo

```python
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
ts_archivo = now.strftime('%Y%m%dT%H%M%S')
ts_legible = now.strftime('%d/%m/%Y %H:%M:%S UTC')
nombre_archivo = f"reporte_ventas.{ts_archivo}.html"

header_metadata = f"""
<div style="background:#1a1a2e;color:#a0a0c0;padding:8px 16px;font-size:12px;font-family:monospace;">
    ⏱️ Generado: <strong style="color:white">{ts_legible}</strong> &nbsp;|
    Archivo: <strong style="color:white">{nombre_archivo}</strong> &nbsp;|
    Filas: <strong style="color:white">{filas_procesadas:,}</strong> &nbsp;|
    <span style="background:#27ae60;color:white;padding:2px 6px;border-radius:3px">CALCULADO POR SCRIPT</span>
</div>
"""
```

---

## Cómo Informar al Usuario (Obligatorio)

Al terminar de generar un HTML, **siempre** comunicar:

```
✅ Output generado:
• Archivo: reporte_ventas.20260716T220606.html
• Generado: 16/07/2026 22:06:06 UTC
• Tamaño: 45 KB
• Filas procesadas: 48,293

⚠️  Si tenés abierta una versión anterior:
   → Abrí el nuevo archivo por su nombre EXACTO
   → No recargues el anterior (puede estar cacheado)
```

---

## Limpieza de Versiones Anteriores (Opcional)

```python
import glob, os

def limpiar_outputs_anteriores(patron: str, directorio: str = 'outputs', mantener_n: int = 5):
    """Mantiene solo los N archivos más recientes."""
    archivos = sorted(
        glob.glob(os.path.join(directorio, patron)),
        key=os.path.getmtime, reverse=True
    )
    for archivo in archivos[mantener_n:]:
        os.remove(archivo)
        print(f"  Eliminado: {archivo}")
    if archivos[mantener_n:]:
        print(f"  Mantenidos: {mantener_n} archivos más recientes")

# Uso: limpiar_outputs_anteriores('reporte_ventas.*.html')
```

---

## Checklist de QA — Output HTML

```
☐ Nombre del archivo incluye timestamp (YYYYMMDDTHHMMSS o YYYYMMDD_HHMMSS)
☐ <title> incluye fecha y hora legible
☐ <h1> visible incluye fecha y hora
☐ Meta tags anti-caché presentes (Cache-Control, Pragma, Expires)
☐ Meta tags de versión presentes (generator, artifact-id, created)
☐ SIN CDNs externos (no hay <link href="https://..."> ni <script src="https://...">)
☐ El agente imprimió en consola el nombre EXACTO del archivo
☐ El agente informó al usuario: "Abrir [NOMBRE EXACTO], no recargar el anterior"
```

---

## Véase también

- `scripts/generate_artifact_name.py` — Script canónico de naming
- `04_OUTPUTS_HTML/doble_click_ui.md` — Accesibilidad en elementos interactivos
- `04_OUTPUTS_HTML/plantilla_html_base.md` — Template HTML completo listo para usar
