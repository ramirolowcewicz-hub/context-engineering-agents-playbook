# Protocolo de Debugging

> Cuándo algo falla, este protocolo define el camino correcto. No adivinar: auditar.

---

## El Flujo de Debugging

```
1. DETECTAR — ¿Qué exactamente falló?
       ↓
2. DOCUMENTAR — Volcar la traza en iteracion.md
       ↓
3. AUDITAR — El agente lee su propia traza y diagnostica
       ↓
4. CAUSA RAÍZ — Identificar dónde está el bug real
       ↓
5. PLAN DE CORRECCIÓN — Proponer el fix quirúrgico
       ↓
6. EJECUTAR — Aplicar solo el fix (nada más)
       ↓
7. VERIFICAR — Confirmar que el error desapareció
       ↓
8. DOCUMENTAR EN BITÁCORA — Registrar el aprendizaje
```

---

## Modo Auditor

Cuando el agente entra en "Modo Auditor":
1. Lee `iteracion.md` con la traza del error.
2. Lee `agente.md` para confirmar cuál era el comportamiento esperado.
3. Identifica la discrepancia entre lo esperado y lo ocurrido.
4. Formula hipótesis sobre la causa raíz.
5. Propone un fix mínimo que resuelva solo esa causa.

**El agente NO puede:**
- Reescribir grandes porciones de código para "estar seguro".
- Cambiar el criterio de éxito para que el resultado actual pase.
- Declarar que el error "no debería pasar" sin identificar por qué pasó.

---

## Reglas de Diagnóstico

### Para errores en cálculos numéricos:
- No pedirle al LLM que "calcule bien". Ajustar el script subyacente.
- Verificar que el script procesa el tipo de dato correcto (float vs. int vs. string).
- Verificar que no hay NaN silenciosos que distorsionen sumas o promedios.
- Verificar que los filtros de fechas no están excluyendo filas por error.

### Para errores en outputs HTML:
- Ver `04_OUTPUTS_HTML/control_cache_html.md`.
- Verificar que el archivo tiene timestamp en el nombre (nunca nombre fijo).
- Si el browser no muestra cambios: el problema es de caché. Ver el protocolo correspondiente.

### Para errores de datos no encontrados:
- Verificar que el archivo está en el contexto actual de la sesión.
- No asumir que el archivo de una sesión anterior sigue disponible.
- Pedir el archivo al usuario antes de proceder.

### Para errores de lógica de negocio:
- Consultar `diccionario.md` antes de interpretar cualquier métrica.
- Si la definición no está en el diccionario, preguntar antes de asumir.

---

## Template para `iteracion.md` en Modo Debugging

```markdown
## DEBUGGING SESSION — [YYYY-MM-DD HH:MM]

### Error reportado
[Descripción exacta del problema]

### Traza del error
```
[PEGAR AQUÍ EL STACK TRACE O OUTPUT INCORRECTO EXACTO]
```

### Hipótesis de causa raíz
1. [Hipótesis 1]
2. [Hipótesis 2]

### Fix aplicado
[Descripción del cambio realizado]

### Verificación
[Evidencia de que el error ya no ocurre]

### Aprendizaje para la bitácora
[Qué se agrega a bitacora.md para no repetir esto]
```

---

## Anti-Patrones de Debugging

| Anti-patrón | Consecuencia | Alternativa correcta |
|-------------|-------------|---------------------|
| Reescribir todo el script porque "algo falla" | Introduce nuevos bugs, pierde trazabilidad | Aislar la línea exacta del error |
| Agregar try/except para silenciar el error | El bug sigue existiendo, ahora invisible | Resolver la causa raíz |
| Cambiar los datos de entrada para que el script no falle | Corrupción de datos, falsos positivos | Hacer el script robusto al input real |
| "Probar" sin mostrar evidencia | No hay certeza de que funcionó | Mostrar output real de consola |
