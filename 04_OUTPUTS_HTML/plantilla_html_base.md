# Plantilla HTML Base Canónica

> Plantilla lista para usar. Copiar y completar los campos marcados con `[VARIABLE]`.

---

## Código de Generación

```python
from datetime import datetime
from pathlib import Path

# =====================================================
# CONFIGURACIÓN (editar según el agente)
# =====================================================
NOMBRE_REPORTE = "analisis"   # prefijo del nombre de archivo
TITULO_REPORTE = "Análisis de Ventas"  # título visible en el HTML
AUTOR_AGENTE = "Agente CSV Analyst v1.0"

# =====================================================
# GENERAR TIMESTAMP (nunca cambiar esta lógica)
# =====================================================
now = datetime.now()
timestamp_archivo = now.strftime('%Y%m%d_%H%M%S')
timestamp_legible = now.strftime('%d/%m/%Y %H:%M:%S')
nombre_archivo = f"{NOMBRE_REPORTE}_{timestamp_archivo}.html"

# =====================================================
# DATOS DEL REPORTE (reemplazar con datos reales)
# =====================================================
filas_procesadas = 0   # [VARIABLE: int]
periodo_desde = ""     # [VARIABLE: str 'YYYY-MM-DD']
periodo_hasta = ""     # [VARIABLE: str 'YYYY-MM-DD']
cuerpo_html = ""       # [VARIABLE: contenido principal del reporte en HTML]

# =====================================================
# TEMPLATE HTML (no modificar la estructura base)
# =====================================================
html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Anti-caché -->
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>{TITULO_REPORTE} — {timestamp_legible}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 0;
            background: #f5f5f5;
            color: #333;
        }}
        .header-meta {{
            background: #1a1a2e;
            color: #fff;
            padding: 12px 24px;
            font-size: 13px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header-meta .generado {{
            color: #a0a0c0;
            font-family: monospace;
        }}
        .titulo {{
            background: #16213e;
            color: #e0e0ff;
            padding: 20px 24px;
            font-size: 24px;
            font-weight: 600;
        }}
        .contenido {{
            max-width: 1200px;
            margin: 24px auto;
            padding: 0 24px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background: #1a1a2e;
            color: white;
            padding: 12px 16px;
            text-align: left;
            font-weight: 500;
        }}
        td {{
            padding: 10px 16px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover td {{ background: #f9f9ff; }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .kpi-card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #4a90d9;
        }}
        .kpi-label {{ font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; }}
        .kpi-value {{ font-size: 28px; font-weight: 700; color: #1a1a2e; margin-top: 4px; }}
        .footer {{
            text-align: center;
            color: #999;
            font-size: 11px;
            padding: 24px;
            border-top: 1px solid #eee;
            margin-top: 40px;
        }}
        .badge-script {{
            display: inline-block;
            background: #27ae60;
            color: white;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
        }}
    </style>
</head>
<body>

<div class="header-meta">
    <span>🤖 {AUTOR_AGENTE}</span>
    <span class="generado">⏱️ Generado: {timestamp_legible} &nbsp;|
    Archivo: {nombre_archivo} &nbsp;|
    Filas: {filas_procesadas:,} &nbsp;|
    Período: {periodo_desde} → {periodo_hasta}</span>
</div>

<div class="titulo">{TITULO_REPORTE}</div>

<div class="contenido">
    
    <!-- INSERTAR CONTENIDO AQUÍ -->
    {cuerpo_html}
    <!-- FIN CONTENIDO -->
    
    <div class="footer">
        <span class="badge-script">CALCULADO POR SCRIPT</span>
        Todos los números de este reporte fueron calculados por código determinista, no estimados por IA.
        <br>Generado por {AUTOR_AGENTE} el {timestamp_legible} | Archivo: {nombre_archivo}
    </div>
</div>

</body>
</html>"""

# =====================================================
# GUARDAR Y REPORTAR
# =====================================================
Path(nombre_archivo).write_text(html, encoding='utf-8')

print(f"""
✅ Output generado exitosamente:
• Archivo: {nombre_archivo}
• Generado: {timestamp_legible}

⚠️  Si tenés abierta una versión anterior, abrí ESTE archivo por su nombre exacto.
No recargues el anterior: puede estar cacheado.
""")
```

---

## Semáforos HTML (Reutilizable)

Para reportes con indicadores de estado:

```python
def semaforo(valor, umbral_verde, umbral_amarillo, invertido=False):
    """
    Retorna el HTML del semáforo según umbrales.
    invertido=True: mayor valor es peor (ej: tasa de error)
    """
    if invertido:
        if valor <= umbral_verde: color = '🟢'
        elif valor <= umbral_amarillo: color = '🟡'
        else: color = '🔴'
    else:
        if valor >= umbral_verde: color = '🟢'
        elif valor >= umbral_amarillo: color = '🟡'
        else: color = '🔴'
    return color

# Uso:
# semaforo(conversion_rate, 0.05, 0.03)  → '🟢' si > 5%, '🟡' si > 3%, '🔴' si < 3%
```
