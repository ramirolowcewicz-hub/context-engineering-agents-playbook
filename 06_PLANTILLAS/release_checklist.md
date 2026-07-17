# Release Checklist — Antes de Activar un Agente

> Checklist por niveles para validar que un agente está listo.
> L1 es obligatorio siempre. L2 antes de cualquier uso en producción. L3 para releases críticos.

---

## Niveles de Release

| Nivel | Cuándo | Tiempo estimado |
|-------|--------|-----------------|
| **L1 — Mínimo** | Antes de cada activación del agente | 5 minutos |
| **L2 — Completo** | Antes de usar en producción | 15 minutos |
| **L3 — Crítico** | Antes de compartir con otros usuarios | 30 minutos |

---

## L1 — Validación Mínima (Siempre Obligatorio)

### Archivos obligatorios
```
☐ agente.md existe
☐ bitacora.md existe (aunque sea con el template vacío)
☐ iteracion.md existe
```

### Contenido de agente.md
```
☐ Tiene sección IDENTIDAD con nombre, versión y rol
☐ Tiene sección KILL-SWITCHES con los 10 universales copiados
☐ Tiene sección PROTOCOLO DE INICIO DE SESIÓN
☐ Tiene sección CRITERIO DE ÉXITO
☐ Los prefijos epistémicos están documentados ([HECHO], [CÁLCULO], etc.)
```

### Honestidad
```
☐ El agente no tiene kill-switches rotos ("NUNCA inventar" debe estar presente)
☐ El protocolo de inicio incluye lectura de la knowledge base
```

---

## L2 — Validación Completa (Producción)

### Protocolo Repository First
```
☐ agente.md menciona que consulta la knowledge base al inicio de cada sesión
☐ El orden de lectura es: agente.md → bitacora.md → iteracion.md → diccionario.md
```

### Honestidad y Categorías Epistémicas
```
☐ [HECHO] definido: observación directa de fuente verificada
☐ [CÁLCULO] definido: resultado de script ejecutado
☐ [INFERENCIA] definido: conclusión lógica
☐ [HIPÓTESIS] definido: especulación que requiere validación
☐ [DESCONOCIDO] / [DATOS FALTANTES] definidos
☐ NO hay afirmaciones sin prefijo en los ejemplos del agente
```

### Si es Modo CSV
```
☐ diccionario.md existe y define todas las columnas clave
☐ El script tiene diagnóstico inicial (shape, dtypes, nulos)
☐ El script valida el schema antes de procesar
☐ El script usa chunking para archivos > 10MB
☐ El script tiene sanity checks en los resultados numéricos
☐ Todos los números del output están marcados [CÁLCULO]
```

### Si es Modo HTML
```
☐ El nombre del archivo incluye timestamp YYYYMMDDTHHMMSS
☐ `<title>` y `<h1>` incluyen fecha y hora legible
☐ Meta tags anti-caché presentes (Cache-Control, Pragma, Expires)
☐ Sin CDNs externos (todo CSS/JS inline o embebido)
☐ Metadatos de versión (generator, artifact-version, created) presentes
☐ El agente informa al usuario el nombre exacto del archivo a abrir
```

### Si es Modo HTML con Drill-Down
```
☐ Elementos clicables tienen cursor: pointer y :hover visible
☐ Elementos clicables tienen tabindex="0" y role="button"
☐ aria-label descriptivo en todos los elementos interactivos
☐ Tecla Escape cierra el panel de detalle
☐ Tecla Enter/Space activa el drill-down
☐ Breadcrumb funcional en el panel de detalle
☐ Máximo 3 niveles de profundidad de drill-down
```

### Si es Modo CODING
```
☐ Scripts son completamente autocontenidos (import + load + process + output)
☐ No hay secretos hardcodeados (API keys, passwords, tokens)
☐ Los scripts son idempotentes (re-ejecutar no acumula efectos)
☐ Existe al menos un test unitario para las funciones clave
☐ El script corre el linter sin errores críticos
```

### Evidencia y Logs
```
☐ El agente muestra el output real de consola (no una descripción de él)
☐ El script actualiza iteracion.md al finalizar
☐ El script genera un execution_id trazable
```

---

## L3 — Release Crítico (Compartir con Otros)

### Documentación
```
☐ README.md del agente existe con instrucciones de uso claras
☐ bitacora.md tiene el contexto inicial (first principles del dominio)
☐ CHANGELOG documentado con la versión 1.0 y fecha de creación
☐ Las decisiones de diseño no triviales están documentadas en bitacora.md
```

### Testing
```
☐ Los tests corren sin errores: pytest pasa
☐ Los tests cubren los casos borde documentados
☐ El agente fue probado con un primer arranque real y pasó
☐ El flujo de debugging (Modo Auditor) fue probado al menos una vez
```

### Seguridad
```
☐ Secret scanner corrido: no hay credenciales en ningún archivo
☐ No hay rutas absolutas del sistema local (solo rutas relativas)
☐ No hay datos reales de producción en los ejemplos o fixtures
```

---

## Comandos Rápidos de Verificación

```bash
# Verificar que no hay secrets hardcodeados
grep -r 'sk-' . --include='*.py' --include='*.md'
grep -r 'password' . --include='*.py' --include='*.md'
grep -r 'api_key' . --include='*.py' --include='*.md'

# Verificar que los tests pasan
python3 -m pytest tests/ -v

# Verificar que el script principal corre
python3 scripts/main.py --dry-run
```
