# Quickstart — Crear un Agente Nuevo

> Guía paso a paso por modo operativo. Empieza aquí si vas a crear un agente nuevo.

---

## Paso 0: Elegir el Modo Operativo

| Modo | Cuándo usarlo | Archivos mínimos |
|------|-------------|------------------|
| **CONVERSACIONAL** | Consultas directas, análisis semántico, sin datos masivos | `agente.md`, `bitacora.md` |
| **CSV** | Procesar archivos CSV, KPIs, reportes de datos | `agente.md`, `diccionario.md`, `main.py` |
| **CODING** | Generar scripts ETL, queries SQL, automatizaciones | `agente.md`, `main.py`, tests |
| **HTML** | Generar dashboards, reportes HTML, artefactos web | `agente.md`, `plantilla.md`, `main.py` |

---

## Paso 1: Crear la Estructura de Carpetas

```bash
mkdir mi-agente/
cd mi-agente/

# Archivos base (todos los modos)
touch agente.md bitacora.md iteracion.md

# Si es modo CSV o CODING:
mkdir scripts/
touch diccionario.md scripts/main.py

# Si es modo HTML:
touch plantilla.md
mkdir outputs/
```

---

## Paso 2: Completar `agente.md`

Usar la plantilla de `06_PLANTILLAS/plantilla_agente_nuevo.md`.
Campos obligatorios a completar:

```markdown
# [NOMBRE DEL AGENTE] — agente.md

## IDENTIDAD
- Nombre: [COMPLETAR]
- Modo: [CONVERSACIONAL / CSV / CODING / HTML]
- Rol: [COMPLETAR: qué hace en una línea]

## PROTOCOLO DE INICIO DE SESIÓN (OBLIGATORIO)
1. Leer este archivo (agente.md)
2. Leer bitacora.md (si existe)
3. Leer iteracion.md (si existe)
4. Leer diccionario.md (si existe y la pregunta involucra terminología)
5. Declarar al usuario: contexto cargado + datos disponibles + modo activo

## KILL-SWITCHES (heredados del playbook)
[KS-1 al KS-10 de kill_switches.md — copiar todos]

## KILL-SWITCHES ESPECÍFICOS
[COMPLETAR: prohibiciones propias de este agente]

## CATEGORÍAS EPISTÉMICAS OBLIGATORIAS
Toda afirmación sustantiva debe usar:
- [HECHO]: observación directa de fuente verificada
- [CÁLCULO]: resultado de script ejecutado
- [INFERENCIA]: conclusión lógica a partir de hechos
- [HIPÓTESIS]: especulación tentativa, requiere validación
- [DESCONOCIDO] / [DATOS FALTANTES]: cuando no se sabe
- [CONFLICTO]: cuando dos fuentes contradicen
```

---

## Paso 3: Completar `diccionario.md` (Modo CSV/CODING)

```markdown
# Diccionario — [NOMBRE DEL AGENTE]

## Variables del Dominio
| Término | Definición | Fórmula | Notas |
|---------|-----------|---------|-------|
| [TÉRMINO] | [definición] | [fórmula si aplica] | [notas] |

## Jerga
- **[SIGLA]**: [significado]

## Schema del CSV Principal
| Columna | Tipo | Nulos OK | Rango | Notas |
|---------|------|---------|-------|-------|
| [columna] | [tipo] | [sí/no] | [rango] | [notas] |
```

---

## Paso 4: Escribir el Script Principal (Modo CSV/CODING)

Checklist antes de empezar:
```
☐ ¿Tiene todos los imports al inicio?
☐ ¿Carga todos los datos desde archivos, no desde variables hardcodeadas?
☐ ¿Ejecuta el diagnóstico inicial (shape, dtypes, nulos)?
☐ ¿Valida el schema antes de procesar?
☐ ¿Usa chunking si el archivo puede ser > 10MB?
☐ ¿Tiene sanity checks en los resultados?
☐ ¿Genera el output con timestamp en el nombre?
☐ ¿Actualiza iteracion.md al finalizar?
☐ ¿Es idempotente (re-ejecutar produce el mismo resultado)?
```

---

## Paso 5: Verificar Antes de Activar

### Checklist de Release (L1 — Mínimo obligatorio)

```
☐ agente.md existe y tiene: identidad, kill-switches, protocolo de inicio
☐ bitacora.md existe (aunque esté vacía con el template)
☐ iteracion.md existe
☐ Todos los kill-switches universales están copiados
☐ Los prefijos epistémicos están documentados en agente.md
☐ Si es modo CSV: diccionario.md existe y tiene el schema
☐ Si es modo HTML: el script genera archivos con timestamp
☐ Si es modo CODING: existe al menos un test
```

---

## Paso 6: Primer Arranque

Protocolo de primer arranque para validar que el agente funciona:

```
1. Abrir nueva sesión con el agente
2. Verificar que el agente dice: "✅ Contexto cargado..."
3. Preguntar: "Describe brevemente qué pods hacer y qué no pods hacer"
4. Verificar que la respuesta:
   a. No inventa capacidades no documentadas en agente.md
   b. No declara limitaciones que no existen
   c. Usa el tono configurado
5. Si alguna respuesta no coincide con agente.md: corregir agente.md, no el agente
```

---

## Flujo de Creación Completo

```
[ELEGIR MODO] → [CREAR ESTRUCTURA] → [COMPLETAR agente.md] → 
[COMPLETAR diccionario.md] → [ESCRIBIR SCRIPT] → [VERIFICAR CHECKLIST] → 
[PRIMER ARRANQUE] → [DOCUMENTAR EN bitacora.md] → ACTIVO
```

---

## Veáse también

- `06_PLANTILLAS/plantilla_agente_nuevo.md` — Template completo con campos [COMPLETAR]
- `06_PLANTILLAS/release_checklist.md` — Checklist L1/L2/L3 antes de activar
- `05_HONESTIDAD_Y_LIMITES/kill_switches.md` — Los 10 kill-switches universales
- `05_HONESTIDAD_Y_LIMITES/response_contract.md` — Prefijos epistémicos
