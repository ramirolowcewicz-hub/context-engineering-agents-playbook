# Mapa de Dependencias del Ecosistema de Archivos

> Este archivo sirve como guía para entender cómo fluye la información entre los componentes de un agente. Adaptá este diagrama para cada agente nuevo.

---

## Flujo General de Información

```
┌──────────────────────────────────────────────────────────────┐
│                  CAPA DE CONFIGURACIÓN                          │
│                                                                  │
│   agente.md  ←──────────  bitacora.md  ←───  diccionario.md    │
│   (identidad,         (memoria largo      (jerga del            │
│   límites,            plazo, errores       dominio)              │
│   protocolo)          históricos)                                │
│                                ↑                                 │
│                        iteracion.md                              │
│                        (estado última                            │
│                        ejecución)                                │
└──────────────────────────────────────────────────────────────┘
                                ↓
                    ┌─────────────────────┐
                    │   CAPA DE PROCESO   │
                    │                    │
                    │  datos.csv / .xlsx  │
                    │        ↓            │
                    │    main.py / .sql   │
                    │   (lógica dura,      │
                    │   determinista)     │
                    └─────────────────────┘
                                ↓
                    ┌─────────────────────┐
                    │   CAPA DE OUTPUT    │
                    │                    │
                    │  reporte_           │
                    │  YYYYMMDD_HHMMSS    │
                    │  .html / .csv       │
                    └─────────────────────┘
```

---

## Dependencias por Tipo de Archivo

| Archivo | Depende de | Lo usan |
|---------|-----------|----------|
| `agente.md` | Nada (es la raíz) | El agente en cada sesión |
| `bitacora.md` | `agente.md` (para saber qué registrar) | El agente al iniciar sesión |
| `iteracion.md` | Ejecución anterior | Modo Auditor del agente |
| `diccionario.md` | Conocimiento del dominio | `main.py`, el agente al interpretar |
| `main.py` | `datos.csv`, `diccionario.md` | El agente (Modo Orquestador) |
| `plantilla.md` | Diseño del output | El agente al generar reportes |

---

## Regla de Actualización

| Archivo | ¿Cuándo se actualiza? | ¿Quién lo actualiza? |
|---------|----------------------|---------------------|
| `agente.md` | Solo cuando el rol o protocolo cambia formalmente | El humano |
| `bitacora.md` | Después de cada aprendizaje significativo | El agente + revisión humana |
| `iteracion.md` | Después de cada ejecución | El agente automáticamente |
| `diccionario.md` | Cuando aparece terminología nueva y validada | El humano |
| `main.py` | Solo bajo la secuencia gather→act→verify | El agente con aprobación humana |
