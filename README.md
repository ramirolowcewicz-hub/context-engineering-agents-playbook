# 🧠 Context Engineering Agents Playbook

> **Repositorio canónico de referencia arquitectónica para la creación de agentes de IA operativos.**
> Creado el: 2026-07-16 | Versión: 1.0.0
> Autor base: Ramiro Lowcewicz — Planning & Strategy Analyst

---

## ¿Qué es esto?

Este repositorio **no es un tutorial**. Es un **sistema de referencia ejecutable** que otros agentes deben leer **antes de crear cualquier nuevo agente**. Contiene los principios, arquitecturas, plantillas y reglas duras que hacen que un agente sea confiable, honesto y eficiente a largo plazo.

**Este repositorio fue diseñado especialmente para agentes que:**
- Analizan archivos CSV grandes (>10MB, millones de filas)
- Escriben y ejecutan código Python/SQL
- Son conversacionales y deben responder con precisión quirúrgica
- Generan outputs HTML con control de caché
- Operan bajo un régimen de **cero alucinación**

---

## 📁 Estructura del Repositorio

```
context-engineering-agents-playbook/
│
├── README.md                          ← Este archivo. Punto de entrada.
│
├── 00_LEER_PRIMERO/
│   ├── MANIFIESTO.md                  ← Principios filosóficos base
│   └── PROTOCOLO_INICIO_CHAT.md       ← Ritual obligatorio al iniciar cada sesión
│
├── 01_ARQUITECTURA/
│   ├── arquitectura_agente.md         ← Estructura canónica de un agente
│   ├── paradigma_adaptable.md         ← Cuándo razonar vs. cuándo ejecutar código
│   └── mapa_dependencias.md           ← Cómo los archivos de un agente se relacionan
│
├── 02_PRINCIPIOS_CODIGO/
│   ├── principios_codigo.md           ← Reglas duras de programación (Karpathy + extensiones)
│   ├── secuencia_gather_act_verify.md ← El flujo obligatorio antes de tocar código
│   └── debugging_protocol.md          ← Flujo de auditoría y corrección de errores
│
├── 03_CSV_Y_DATOS/
│   ├── manejo_csv_grandes.md          ← Protocolo para CSVs grandes sin OOM ni alucinaciones
│   ├── anti_alucinacion_numerica.md   ← Reglas para cálculos deterministas
│   └── validacion_datos.md            ← Contratos de datos y validación de inputs
│
├── 04_OUTPUTS_HTML/
│   ├── control_cache_html.md          ← El problema del caché y cómo resolverlo SIEMPRE
│   └── plantilla_html_base.md         ← Plantilla canónica con naming por timestamp
│
├── 05_HONESTIDAD_Y_LIMITES/
│   ├── protocolo_anti_alucinacion.md  ← El protocolo de honestidad total
│   ├── kill_switches.md               ← Lo que el agente NUNCA puede hacer
│   └── doble_click.md                 ← Capacidad de profundización conversacional
│
├── 06_PLANTILLAS/
│   ├── plantilla_agente_nuevo.md      ← Template para crear un agente desde cero
│   ├── plantilla_bitacora.md          ← Template para la bitácora del agente
│   └── plantilla_iteracion.md         ← Template para el log de ejecución
│
└── 07_EJEMPLOS/
    ├── ejemplo_agente_csv.md           ← Agente de ejemplo para análisis de CSV
    └── ejemplo_agente_programador.md   ← Agente de ejemplo para tareas de código
```

---

## 🚀 ¿Cómo usar este repositorio?

### Si sos un agente creando otro agente:
1. **Leer `00_LEER_PRIMERO/MANIFIESTO.md`** — Sin excepciones.
2. **Leer `00_LEER_PRIMERO/PROTOCOLO_INICIO_CHAT.md`** — Define tu ritual de arranque.
3. **Leer `01_ARQUITECTURA/arquitectura_agente.md`** — Tu estructura base.
4. Según el tipo de agente que vayas a crear, leer las secciones relevantes (03, 04, 05).
5. Usar las plantillas de `06_PLANTILLAS/` para construir los archivos del nuevo agente.

### Si sos un humano configurando un agente:
1. Comenzar por `06_PLANTILLAS/plantilla_agente_nuevo.md`.
2. Completar los campos obligatorios marcados con `[COMPLETAR]`.
3. Agregar el archivo `agente.md` resultante a la knowledge base del agente.

---

## ⚠️ Principio Supremo

> **Si no sabés algo con certeza, no lo inventés. Nunca.**
> El valor de un agente no está en su capacidad de parecer seguro.
> Está en su capacidad de ser confiable cuando más importa.

---

*Repositorio mantenido como referencia viva. Toda modificación requiere justificación explícita y documentación en el changelog.*
