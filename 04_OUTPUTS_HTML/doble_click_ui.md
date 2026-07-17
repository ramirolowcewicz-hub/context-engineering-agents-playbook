# Doble Click UI — Patrones de Interacción Profunda en HTML

> Para agentes que generan interfaces HTML con elementos cliqueables que abren vistas de detalle (drill-down).
> Combina el protocolo conversacional de `doble_click.md` con la implementación técnica accesible.

---

## 1. Distinción de Interacción

| Gesto | Elemento | Propósito |
|-------|---------|----------|
| Click simple | Fila del reporte | Selección / highlight |
| Doble click | Celda de dato | Drill-down a detalle |
| Tecla `Enter` en elemento con foco | Celda | Equivalente a doble click (accesibilidad) |
| Tecla `Escape` | Panel de detalle | Cerrar y volver al contexto |
| Tecla `Tab` | Elementos interactivos | Navegar entre elementos |

---

## 2. Affordance Visible (Obligatorio)

Todo elemento con drill-down debe tener AL MENOS UNA señal visual:

```html
<!-- Fila cliqueable: cursor + hover + focus visible + accesibilidad -->
<tr class="clickable-row" tabindex="0" role="button"
    aria-label="Ver detalle de Revenue para canal Web"
    data-item="revenue" data-canal="web">
  <td>Web</td>
  <td class="value">$567,890</td>
  <td class="delta positive">+5.2%</td>
</tr>

<style>
  .clickable-row { cursor: pointer; transition: background 0.15s; }
  .clickable-row:hover { background: #f0f4ff; outline: 2px solid #4a90d9; }
  .clickable-row:focus { outline: 2px solid #4a90d9; outline-offset: 2px; }
</style>
```

### Elementos SIN drill-down (no deben ser navegables):
```html
<!-- Celda sin drill-down: no tiene tabindex, no es button -->
<td aria-label="Sin detalle disponible para esta línea">
  <span class="value">$1,234</span>
  <span style="color:#ccc" aria-hidden="true"> —</span>
</td>
```

---

## 3. Panel de Detalle

```html
<aside id="detail-panel" class="detail-panel" role="complementary"
       aria-label="Detalle de la línea seleccionada" hidden>
  <header class="detail-header">
    <h2 id="detail-title">Detalle — [Título dinámico]</h2>
    <button id="close-detail" aria-label="Cerrar panel de detalle">✕</button>
  </header>
  <div id="detail-content" class="detail-content">
    <p aria-live="polite">Cargando detalle…</p>
  </div>
  <footer>
    <nav aria-label="Breadcrumb">
      <ol>
        <li><a href="#" id="breadcrumb-parent">Resumen</a></li>
        <li aria-current="page" id="breadcrumb-current">Detalle</li>
      </ol>
    </nav>
  </footer>
</aside>
```

---

## 4. JavaScript Mínimo Funcional

```javascript
// Abrir drill-down
document.querySelectorAll('.clickable-row').forEach(row => {
  const open = () => {
    const item = row.dataset.item;
    const canal = row.dataset.canal;
    document.getElementById('detail-title').textContent = `Detalle \u2014 ${item} \u00b7 ${canal}`;
    document.getElementById('detail-content').textContent = 'Datos del drill-down aquí.';
    document.getElementById('detail-panel').removeAttribute('hidden');
    document.getElementById('close-detail').focus();
    // Actualizar breadcrumb
    document.getElementById('breadcrumb-current').textContent = `${item} \u00b7 ${canal}`;
  };
  row.addEventListener('click', open);
  row.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') open(); });
});

// Cerrar panel
document.getElementById('close-detail').addEventListener('click', () => {
  document.getElementById('detail-panel').setAttribute('hidden', '');
});

// Cerrar con Escape
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    const panel = document.getElementById('detail-panel');
    if (!panel.hasAttribute('hidden')) {
      panel.setAttribute('hidden', '');
    }
  }
});
```

---

## 5. Niveles de Profundidad

| Nivel | Nombre | Alcance | Cuándo ofrecer |
|-------|--------|---------|----------------|
| 1 | **Resumen** | Respuesta directa | Siempre |
| 2 | **Detalle** | Respuesta + contexto necesario | Si el usuario hace una pregunta de seguimiento |
| 3 | **Auditoría** | Investigación completa, múltiples fuentes | Solo si se pide explícitamente |

**Límite de profundidad: máximo 3 niveles.** Nunca más.

---

## 6. Formato Conversacional del Doble Click

Cuando el agente ofrece profundización en texto (sin HTML):

```
[OBJETIVO] Explicar el desvío -8% en GB esta semana
[ANCLA] ¿Qué causó la variación específica?

[CÁLCULO] Revenue GB: $X | L4W promedio: $Y | Desvío: -8%
fuente: script, 48,293 filas | confianza: alta

[INFERENCIA] El 92% del desvío ocurrió el viernes 13/06.
fuente: breakdown diario [CÁLCULO] | confianza: media

¿Doble click en algún punto?
→ A. Ver el breakdown día a día
→ B. Comparar con el mismo período del año anterior
→ C. Analizar el canal específico con mayor desvío
```

---

## 7. Checklist de QA para UI de Doble Click

```
☐ Todo elemento con drill-down tiene cursor: pointer y :hover visible
☐ Todo elemento con drill-down tiene tabindex="0" y role="button"
☐ Todo elemento con drill-down tiene aria-label descriptivo
☐ Elementos SIN drill-down NO son navegables por teclado
☐ Panel de detalle tiene role="complementary" y aria-label
☐ Breadcrumb presente y funcional
☐ Tecla Escape cierra el panel y restaura el foco al elemento anterior
☐ Tecla Enter/Space abre drill-down en el elemento focalizado
☐ Foco visible en todos los elementos interactivos (:focus con outline)
☐ No simular drill-down si no hay datos: mensaje claro en su lugar
☐ Máximo 3 niveles de profundidad
```
