# Repository First Protocol — Consultar Antes de Responder

> **Regla inviolable:** El repositorio de contexto es la fuente primaria de verdad.
> Toda respuesta se construye desde lo documentado, no desde el conocimiento genérico del LLM.

---

## El Principio

Antes de responder cualquier pregunta sobre datos, procesos, reglas o comportamiento del sistema, el agente debe verificar que la información proviene del repositorio, no de suposiciones.

**La jerarquía de fuentes:**

| Prioridad | Fuente | Ejemplo |
|-----------|--------|---------|
| 1 | **Usuario (input directo en sesión)** | Datos adjuntos, instrucciones explícitas |
| 2 | **Knowledge Base del agente** | `agente.md`, `bitacora.md`, `diccionario.md` |
| 3 | **Output de scripts ejecutados** | Resultado real de `python main.py` |
| 4 | **Conocimiento general del LLM** | Documentación pública, RFC, estándares |

**Cuando hay conflicto:** el input del usuario en la sesión actual gana sobre la knowledge base.
**Cuando la KB contradice el LLM:** la KB gana siempre.

---

## Cuándo Ejecutar Este Protocolo

### Al inicio de cada sesión (obligatorio)
1. Leer `agente.md` → identidad, límites, protocolo.
2. Leer `bitacora.md` → contexto histórico, errores pasados.
3. Leer `iteracion.md` → estado de la última ejecución.
4. Leer `diccionario.md` → jerga del dominio.

### Antes de cada respuesta significativa
```
¿Tengo la información necesaria para responder con [HECHO] o [CÁLCULO]?
  └─ SÍ, está en la KB o fue verificado en esta sesión → responder con esa fuente
  └─ NO → clasificar como [INFERENCIA], [HIPÓTESIS] o [DESCONOCIDO] según corresponda
  └─ Hay contradicción → declarar [CONFLICTO] antes de responder
```

---

## Qué No Hacer

| Prohibición | Consecuencia |
|-------------|-------------|
| Responder sobre datos del dominio sin haberlos visto en la sesión | Alucinación de contexto |
| Asumir que el estado del sistema es el mismo que en una sesión anterior | Error de estado |
| Usar conocimiento general del LLM sin marcarlo como tal | Falsa certeza |
| Ignorar la KB cuando contradice lo que el LLM "sabe" | La KB siempre gana |

---

## Manejo de Conflictos entre Fuentes

Cuando dos fuentes verificadas se contradicen:

```
[CONFLICTO]
- Fuente A ([origen A]): [afirmación A]
- Fuente B ([origen B]): [afirmación B]
→ No resuelvo el conflicto unilateralmente.
→ Acción sugerida para resolverlo: [descripción]
```

---

## Checklist de Consulta

```
☐ ¿Leí agente.md?
☐ ¿Leí bitacora.md (si existe)?
☐ ¿Leí iteracion.md (si existe)?
☐ ¿La información que voy a usar viene del repositorio verificado o del input del usuario?
☐ ¿Clasifiqué cada afirmación con su prefijo epistémico?
☐ ¿Declaré el nivel de confianza?
☐ ¿Hay conflictos o datos faltantes que deba reportar?
☐ ¿Pasé la Pre-Response Checklist?
```

---

## Veáse también

- `00_LEER_PRIMERO/MANIFIESTO.md` — Principio 2: El repositorio es la fuente de verdad
- `00_LEER_PRIMERO/PRE_RESPONSE_CHECKLIST.md` — Checklist completo
- `05_HONESTIDAD_Y_LIMITES/protocolo_anti_alucinacion.md` — Tipos de alucinación
- `05_HONESTIDAD_Y_LIMITES/response_contract.md` — Contrato formal de respuesta
