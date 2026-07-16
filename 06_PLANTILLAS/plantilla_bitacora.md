# Plantilla: bitácora.md

> Copiar este archivo como `bitacora.md` en el repositorio del nuevo agente.
> La bitácora crece con el tiempo. Las entradas se agregan, nunca se borran.

---

```markdown
# Bitácora — [NOMBRE DEL AGENTE]

> Memoria a largo plazo del agente. Registro histórico de aprendizajes, errores y decisiones.
> Última actualización: [FECHA]

---

## CONTEXTO INICIAL (First Principles)

> Verdades inmutables del dominio. Solo cambian con revisión humana explícita.

[COMPLETAR: describir las verdades del dominio que el agente debe conocer siempre.
Ejemplos:
- "El año fiscal empieza en [MES]."
- "Las métricas se calculan sobre ventanas cerradas de N semanas."
- "La jerarquía de productos es: Categoría > Subcategoría > SKU."
- "Revenue = Fee + Upfronts, nunca incluye reembolsos."]

---

## ARQUITECTURA VIGENTE

Última actualización: [FECHA]

[COMPLETAR: descripción del estado actual del agente. Incluir:
- Qué scripts existen y qué hacen
- Qué fuentes de datos consume
- Cómo se genera el output
- Conocimientos pendientes o work in progress]

---

## DECISIONES DE DISEÑO

### [FECHA] — [Título de la decisión]

**Contexto:** [Por qué surgió esta decisión]
**Opciones evaluadas:**
- Opción A: [descripción]
- Opción B: [descripción]
**Elección:** [Cuál se eligió]
**Razón:** [Por qué]

---

## REGISTRO DE ERRORES PASADOS

> Formato: [FECHA] | ERROR | CAUSA RAÍZ | SOLUCIÓN | PREVENCIÓN FUTURA

### [FECHA] — [Título del error]

**Error:** [Descripción del comportamiento incorrecto]
**Causa raíz:** [Dónde estaba el bug real]
**Solución aplicada:** [Qué se modificó exactamente]
**Cómo prevenir en el futuro:** [Regla o chequeo a agregar]

---

## BUGS CONOCIDOS (PENDIENTES)

| ID | Descripción | Impacto | Estado | Fecha detención |
|----|------------|---------|--------|------------------|
| BUG-001 | [descripción] | [Alto/Medio/Bajo] | [Pendiente/En progreso] | [FECHA] |

---

## CHANGELOG

| Versión | Fecha | Descripción del cambio |
|---------|-------|------------------------|
| 1.0 | [FECHA] | Creación inicial del agente |
```
