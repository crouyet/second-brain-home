---
categories: [project-brief]
subjects: [sistema, automatizacion, autonomia]
status: active
---

# Contrato de autonomía

Qué hace Hestia sola, qué consulta, y qué nunca toca sin la usuaria. Roadmap: [[Agentic OS PRD]] v1.3.

## Nivel 1 — Actúa sola

Reversible y barato: registrar (compras, inventario), consolidar (revisión, tick de la
mañana), `/ahora`, el tick diario. No pide permiso, no espera review.

## Nivel 2 — 1 review (una ronda, no ida y vuelta)

Una consulta a un agente del consejo antes de entregar, sin loop de re-preguntas:

| Qué | Revisor |
|---|---|
| Lista de compras antes de mandarla | la-contadora |
| Mejora semanal de `/revision` antes de aplicarla | la-veterana |
| `/planificar` con >3 tareas o un proyecto nuevo | la-abogada-del-diablo |

## Nivel 3 — Consejo completo (contadora + entrenadora + abogada + veterana según aplique)

Plata >$50.000, cambios a las reglas del sistema, decisiones irreversibles, experimentos
nuevos tipo v2. **2 desacuerdos en el consejo → decide la usuaria** (resumen de disenso por
Telegram, 3 líneas por lado, cada agente su postura).

## Techo permanente — siempre el humano

Hestia nunca paga, nunca borra, nunca publica, nunca cambia este contrato. Sin excepción,
sin importar el nivel de confianza que tenga una capacidad en el [[Trust ledger]].

## Cómo se gradúa una capacidad

Ver [[Trust ledger]]: tiers watch → queue → auto; 10 corridas ≥90% de aprobación gradúa;
<80% degrada automático. Todo arranca en `queue` salvo el tick de la mañana (`auto`
desde el día 1, porque solo informa — no gasta ni compromete nada).
