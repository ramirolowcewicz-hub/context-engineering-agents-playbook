# Observabilidad — Logs, Trazabilidad y Métricas de Ejecución

> Todo script de producción debe dejar una traza completa de su ejecución.
> Sin observabilidad, el debugging es adivinanza.

---

## El Principio

Cada ejecución de un script o agente debe poder responderse estas preguntas post-ejecución:
- ¿Cuándo corrió?
- ¿Qué datos processó exactamente?
- ¿Cuánto tardó?
- ¿Cuánta memoria usó?
- ¿Hubo errores? ¿De qué tipo?
- ¿El output es confiable?

---

## Execution ID

Cada ejecución recibe un ID único. Todos los logs, outputs y archivos generados lo incluyen.

```python
import hashlib
from datetime import datetime, timezone

def generate_execution_id(operation: str) -> str:
    """Genera un ID único por ejecución. Incluye timestamp y operación."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    suffix = hashlib.md5(f"{operation}{ts}".encode()).hexdigest()[:6]
    return f"{ts}_{suffix}"  # ej: 20260716T220606_a3f7c2

# Uso al inicio de todo script de producción:
EXECUTION_ID = generate_execution_id("analisis_canales")
print(f"Execution ID: {EXECUTION_ID}")
```

---

## Structured Logging

Los logs de scripts de producción deben ser estructurados (JSON) para facilitar el análisis:

```python
import logging
import json
from datetime import datetime, timezone
from pathlib import Path

class StructuredLogger:
    """Logger que emite JSON para fácil análisis post-ejecución."""
    
    def __init__(self, name: str, execution_id: str, log_file: str = None):
        self.execution_id = execution_id
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(message)s')
        
        # Handler a consola
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        
        # Handler a archivo (opcional)
        if log_file:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
    
    def _emit(self, level: str, event: str, **kwargs):
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "execution_id": self.execution_id,
            "level": level,
            "event": event,
            **kwargs
        }
        getattr(self.logger, level)(json.dumps(record, ensure_ascii=False))
    
    def info(self, event: str, **kwargs): self._emit("info", event, **kwargs)
    def warning(self, event: str, **kwargs): self._emit("warning", event, **kwargs)
    def error(self, event: str, **kwargs): self._emit("error", event, **kwargs)

# Uso:
logger = StructuredLogger("csv_analyst", EXECUTION_ID, log_file="outputs/execution.log")
logger.info("inicio_ejecucion", archivo="ventas_julio.csv")
logger.info("csv_leido", filas=48293, columnas=12, memoria_mb=8.3)
logger.info("calculo_completado", operacion="revenue_total", resultado=1234567.89)
logger.warning("nulos_detectados", columna="descuento", cantidad=1203, accion="tratados_como_0")
logger.info("output_generado", archivo="reporte_20260716_220606.html")
```

---

## Métricas a Registrar

Todo script de producción debe registrar:

```python
import time
import psutil
import os
from datetime import datetime

class ExecutionMetrics:
    """Registra métricas clave de ejecución."""
    
    def __init__(self):
        self.start_time = time.time()
        self.start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024**2
        self.checkpoints = []
    
    def checkpoint(self, nombre: str, filas_procesadas: int = None):
        elapsed = time.time() - self.start_time
        mem = psutil.Process(os.getpid()).memory_info().rss / 1024**2
        self.checkpoints.append({
            "nombre": nombre,
            "elapsed_s": round(elapsed, 2),
            "memoria_mb": round(mem, 1),
            "filas_procesadas": filas_procesadas
        })
        print(f"  [{nombre}] {elapsed:.1f}s | {mem:.0f}MB RAM")
    
    def check_memory_limit(self, threshold_pct: float = 80.0) -> bool:
        """Retorna True si se superó el umbral de RAM. Abortar si es True."""
        uso_pct = psutil.virtual_memory().percent
        if uso_pct > threshold_pct:
            print(f"ALERTA: RAM al {uso_pct:.0f}% (límite: {threshold_pct}%). Abortando.")
            return True
        return False
    
    def resumen(self) -> dict:
        total = time.time() - self.start_time
        peak_mem = max(c['memoria_mb'] for c in self.checkpoints) if self.checkpoints else 0
        return {
            "execution_id": EXECUTION_ID,
            "duracion_total_s": round(total, 2),
            "memoria_peak_mb": round(peak_mem, 1),
            "checkpoints": self.checkpoints
        }

# Uso:
metrics = ExecutionMetrics()
# ... procesamiento ...
metrics.checkpoint("csv_leido", filas_procesadas=48293)
# ... más procesamiento ...
metrics.checkpoint("calculo_completado")
print(json.dumps(metrics.resumen(), indent=2))
```

---

## Kill-Switches de Observabilidad

| Condición | Límite | Acción |
|-----------|--------|--------|
| RAM > 80% disponible | configurable | Abortar y loguear |
| Tiempo de ejecución > 5 min | configurable | Alertar, abortar si supera 10 min |
| Errores > 5% de las filas | configurable | Abortar con reporte |
| Output vacío (0 filas) | siempre | Abortar con error explícito |

```python
# Kill-switch de tiempo
if time.time() - metrics.start_time > 300:  # 5 minutos
    logger.error("timeout", elapsed_s=time.time() - metrics.start_time)
    raise TimeoutError("Ejecución superó el límite de 5 minutos. Abortando.")

# Kill-switch de output vacío
if len(resultado) == 0:
    logger.error("output_vacio", operacion="groupby_revenue")
    raise ValueError("El resultado está vacío. Verificar filtros y datos de entrada.")
```

---

## Actualización de `iteracion.md` al Final de Cada Ejecución

```python
from pathlib import Path
from datetime import datetime

def actualizar_iteracion(execution_id: str, input_file: str, output_file: str, 
                          filas: int, errores: list, criterio_exito: bool):
    """Actualiza iteracion.md automáticamente al terminar un script."""
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    estado = '✅ Completado' if criterio_exito else '❌ Fallido'
    errores_txt = '\n'.join(f'- {e}' for e in errores) if errores else 'Ninguno'
    
    contenido = f"""## Iteración {ts} — Execution ID: {execution_id}

### Input
- Archivo: {input_file}
- Filas procesadas: {filas:,}

### Output
- Archivo: {output_file}

### Criterio de éxito: {estado}

### Errores
{errores_txt}

---
"""
    path = Path('iteracion.md')
    existing = path.read_text(encoding='utf-8') if path.exists() else '# Log de Iteraciones\n\n'
    path.write_text(existing + contenido, encoding='utf-8')
    print(f"✅ iteracion.md actualizado")
```
