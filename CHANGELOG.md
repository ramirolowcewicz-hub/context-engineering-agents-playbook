# CHANGELOG — Context Engineering Agents Playbook

> Registro de cambios del repositorio. Todo cambio requiere entrada aquí con justificación.

---

## v1.1.0 — 2026-07-17

**Síntesis con `context-engineering-agents` — Combinación de los mejores elementos de ambos repositorios.**

### Fuente de la síntesis
Repositorio origen: `ramirolowcewicz-hub/context-engineering-agents`
Método: análisis completo de todos los documentos de ambos repos + identificación de fortalezas únicas de cada uno.

### Qué aportó `context-engineering-agents` a este playbook:
- Sistema formal de **prefijos epistémicos** ([HECHO], [CÁLCULO], [INFERENCIA], [HIPÓTESIS], [DESCONOCIDO], [DATOS FALTANTES], [CONFLICTO])
- **Repository First Protocol** como documento independiente y formal
- **Pre-Response Checklist** estructurada y verificable por modo (PLAN/BUILD/REVIEW/CSV/HTML)
- **Double-Click UI**: implementación técnica accesible con aria, tabindex, keyboard navigation
- **generate_artifact_name.py**: script funcional anti-colisión con UTC y sufijo de versión
- **Release Checklist L1/L2/L3** por niveles de rigurosidad
- **TDD formal**: secuencia rojo-verde-refactor con ejemplo
- **Observabilidad**: execution_id, structured logging, métricas de RAM/tiempo
- **Data Contracts**: formato markdown + JSON schema + validador Python + detección de schema drift
- **Chunking por tabla de MB**: umbrales explícitos con estrategia por rango
- **Check de RAM con psutil**: kill-switch de memoria en scripts de producción
- **Self-contained HTML**: prohibición explícita de CDNs externos
- **Clasificación de hallazgos**: BLOCKER / WARNING / SUGGESTION
- **Blast radius**: concepto formalizado y documentado
- **Idempotencia y rollback**: reglas explícitas con ejemplos de código
- **Confianza calibrada**: sistema alta/media/baja vinculado a prefijos epistémicos

### Qué mantuvo el playbook de su versión v1.0 (mejor expresado aquí):
- Manifiesto filosófico con narrativa y principios ordenados
- Protocolo de inicio de chat como ritual ejecutable paso a paso
- Árbol de decisión visual Analista vs. Orquestador
- Script de diagnóstico inicial CSV con fallback de encodings
- Templates con campos [COMPLETAR] claramente marcados
- Ejemplos de flujos conversacionales completos (chat real simulado)
- Control de caché HTML como protocolo separado con checklist
- Modo Auditor de debugging detallado
- Kill-Switches como lista numerada independiente (KS-1 a KS-10)

### Archivos nuevos en v1.1:
- `00_LEER_PRIMERO/PRE_RESPONSE_CHECKLIST.md` — Checklist verificable por modo
- `01_ARQUITECTURA/repository_first_protocol.md` — Repository First formal
- `02_PRINCIPIOS_CODIGO/observabilidad.md` — execution_id, logging estructurado, métricas
- `03_CSV_Y_DATOS/data_contracts.md` — Contratos formales + JSON schema + validador
- `04_OUTPUTS_HTML/doble_click_ui.md` — Double-Click UI con a11y
- `05_HONESTIDAD_Y_LIMITES/response_contract.md` — Contrato formal de respuesta
- `06_PLANTILLAS/quickstart.md` — Guía por modo operativo
- `06_PLANTILLAS/release_checklist.md` — Release Checklist L1/L2/L3
- `scripts/generate_artifact_name.py` — Script canónico de naming anti-colisión

### Archivos actualizados en v1.1:
- `00_LEER_PRIMERO/MANIFIESTO.md` — Principio 11 (prefijos epistémicos) + jerarquía de fuentes
- `02_PRINCIPIOS_CODIGO/principios_codigo.md` — TDD, blast radius, idempotencia, BLOCKER/WARNING/SUGGESTION
- `03_CSV_Y_DATOS/manejo_csv_grandes.md` — Profiling, psutil, kill-switches, chunking por MB
- `04_OUTPUTS_HTML/control_cache_html.md` — Self-contained, UTC ISO 8601, metadatos de versión
- `05_HONESTIDAD_Y_LIMITES/protocolo_anti_alucinacion.md` — 7 prefijos epistémicos formales
- `06_PLANTILLAS/plantilla_agente_nuevo.md` — Prefijos epistémicos integrados en el template

### Decisiones de diseño v1.1:
- Los prefijos epistémicos son el mecanismo más efectivo para eliminar la alucinación. Se integran en todos los niveles del playbook.
- El timestamp en UTC (no local) garantiza unicidad entre zonas horarias y es el estándar de `generate_artifact_name.py`.
- La Pre-Response Checklist es el único punto de control que cubre todos los protocolos de forma verificable.
- La regla self-contained (sin CDNs) es absoluta: un reporte que depende de internet externo puede fallar en cualquier momento.

---

## v1.0.0 — 2026-07-16

**Creación inicial del repositorio.**

### Archivos creados:
- `README.md` — Punto de entrada y mapa del repositorio
- `00_LEER_PRIMERO/MANIFIESTO.md` — 10 principios filosóficos base
- `00_LEER_PRIMERO/PROTOCOLO_INICIO_CHAT.md` — Ritual obligatorio de arranque
- `01_ARQUITECTURA/arquitectura_agente.md` — Ecosistema canónico de archivos
- `01_ARQUITECTURA/paradigma_adaptable.md` — Analista vs. Orquestador
- `01_ARQUITECTURA/mapa_dependencias.md` — Flujo de información entre componentes
- `02_PRINCIPIOS_CODIGO/principios_codigo.md` — Reglas Karpathy + extensiones
- `02_PRINCIPIOS_CODIGO/secuencia_gather_act_verify.md` — Flujo obligatorio pre-código
- `02_PRINCIPIOS_CODIGO/debugging_protocol.md` — Modo Auditor y flujo de debugging
- `03_CSV_Y_DATOS/manejo_csv_grandes.md` — Protocolo para CSVs grandes
- `03_CSV_Y_DATOS/anti_alucinacion_numerica.md` — Cálculos deterministas vs. estimaciones
- `03_CSV_Y_DATOS/validacion_datos.md` — Contratos de input y validaciones
- `04_OUTPUTS_HTML/control_cache_html.md` — El problema del caché y su solución
- `04_OUTPUTS_HTML/plantilla_html_base.md` — Template canónico con timestamp
- `05_HONESTIDAD_Y_LIMITES/protocolo_anti_alucinacion.md` — 5 tipos de alucinación
- `05_HONESTIDAD_Y_LIMITES/kill_switches.md` — 10 prohibiciones absolutas universales
- `05_HONESTIDAD_Y_LIMITES/doble_click.md` — Profundización conversacional
- `06_PLANTILLAS/plantilla_agente_nuevo.md` — Template para crear un agente desde cero
- `06_PLANTILLAS/plantilla_bitacora.md` — Template para memoria a largo plazo
- `06_PLANTILLAS/plantilla_iteracion.md` — Template para log de ejecución
- `07_EJEMPLOS/ejemplo_agente_csv.md` — Agente CSV con flujo completo
- `07_EJEMPLOS/ejemplo_agente_programador.md` — Agente programador con flujo PLAN→BUILD

---

## Próximas versiones (backlog)

- [ ] v1.2: Agregar `08_SEGURIDAD/` con protocolo de manejo de datos sensibles en CSVs
- [ ] v1.2: Agregar plantilla para agente con SQL (no solo Python)
- [ ] v1.3: Agregar ejemplos de agentes multi-archivo (orquestación entre agentes)
- [ ] v2.0: Incorporar principios de evaluación automática de outputs (evals)
- [ ] v2.0: Validador automatizado `scripts/validate_agent_repo.py` con 7 reglas
