# CHANGELOG — Context Engineering Agents Playbook

> Registro de cambios del repositorio. Todo cambio requiere entrada aquí con justificación.

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
- `05_HONESTIDAD_Y_LIMITES/protocolo_anti_alucinacion.md` — 5 tipos de alucinación y cómo evitarlos
- `05_HONESTIDAD_Y_LIMITES/kill_switches.md` — 10 prohibiciones absolutas universales
- `05_HONESTIDAD_Y_LIMITES/doble_click.md` — Profundización conversacional
- `06_PLANTILLAS/plantilla_agente_nuevo.md` — Template para crear un agente desde cero
- `06_PLANTILLAS/plantilla_bitacora.md` — Template para memoria a largo plazo
- `06_PLANTILLAS/plantilla_iteracion.md` — Template para log de ejecución
- `07_EJEMPLOS/ejemplo_agente_csv.md` — Agente CSV con flujo completo
- `07_EJEMPLOS/ejemplo_agente_programador.md` — Agente programador con flujo PLAN→BUILD

### Decisiones de diseño v1.0:
- Se prioriza la honestidad sobre la utilidad percibida: mejor decir "no sé" que inventar.
- El timestamp en HTMLs es una regla absoluta, no una recomendación.
- El protocolo de inicio de chat es obligatorio porque el costo de saltarlo supera al beneficio de velocidad.
- Se documenta el paradigma Analista/Orquestador como la decisión de diseño más crítica.

---

## Próximas versiones (backlog)

- [ ] v1.1: Agregar sección `08_SEGURIDAD/` con protocolo de manejo de datos sensibles
- [ ] v1.1: Agregar plantilla para agente con SQL (no solo Python)
- [ ] v1.2: Agregar ejemplos de agentes multi-archivo (orquestación entre agentes)
- [ ] v2.0: Incorporar principios de evaluación automática de outputs (evals)
