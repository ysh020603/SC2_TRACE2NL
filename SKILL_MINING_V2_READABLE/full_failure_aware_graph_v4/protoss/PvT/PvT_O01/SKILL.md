# PvT_O01 Technology/Economy/Expansion

## Skill Identity

- Skill ID: PvT_O01
- Matchup: Protoss vs Terran
- Opening Family: Technology / Economy / Expansion
- Method: Failure-Aware Full V4

## Opening Strategy

A Protoss opening that emphasizes heavy technology investment, a strong economy, and early expansion while maintaining a flexible ground-oriented posture. The opponent is Terran, and the early game is characterized by moderate production and a focus on tech.

Develop a technology/economy/expansion posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

## Strategic Characteristics

- Economy: heavy
- Production: moderate
- Technology: heavy
- Army direction: ground-leaning

## Strategic Priorities

- Preserve the opening's strategic identity without reproducing a fixed sequence.
- Check current Completed, Under Construction, Active Queues, resources, supply, and prerequisites before choosing exact macro actions.
- Match any adaptation against partial Enemy Intelligence and current Threat Flags.
- Re-evaluate economy, production, technology, and army trade-offs at every decision.

## V4 Failure-Aware Execution Guardrails

Apply these checks before following any strategic direction or matchup-specific lesson.

### G01 — Keep the queue executable

- Rebuild the ordered queue from the live Completed, Under Construction, Active Queues, resources, supply, and prerequisites.
- Put prerequisite structures before dependent add-ons, technology, upgrades, or units; omit actions whose parent will still be unavailable.
- Prefer a short queue that can begin now. Do not let repeated workers, supply providers, or future tech hide the immediate army-production action.

### G02 — Supply is just-in-time, not a spending plan

- Count completed, pending, and already queued supply together. Add one provider when free supply is at or below 4, or two only when several active production queues will consume the space immediately.
- Never add three or more supply providers in one decision. If supply is already comfortable, spend on workers, production, combat units, or required technology instead.

### G03 — Convert the bank into fighting capacity

- If the combined mineral and gas bank is at least 750 while production is idle or army supply is low, prioritize currently executable production structures and combat units before optional expansion or technology.
- Around 05:00, aim for at least two usable unit-production sources and roughly 10 army supply. Around 06:00, if army supply is below 15, pause optional greed and restore continuous army production.
- When predicted army advantage is OverwhelmingDisadvantage or an owned zone is threatened, army, counters, detection, and production take priority over expansion and nonessential technology until the live comparison improves.

### G04 — Balance workers against survival

- Keep worker production moving toward current base saturation, but do not queue many workers ahead of a missing production facility or urgent defensive units.
- Recheck worker count, ideal workers, income, army supply, production queues, and threat flags every cycle; replace the old queue when the bottleneck changes.

### G05 — Protoss production interpretation

- Scale Gateways or other unit-producing tech only after power, prerequisites, and production capacity are executable.

## V4 Matchup-Specific Corrections

### R01 — Maintain tech-economy tempo with production scaling

**When:** At 240-360s, if bank > 800 and (production < 3 or army supply < 14) and no OverwhelmingDisadvantage

**Correction:** Prioritize adding Gateways (up to 4-5 total) and a Robotics Facility if missing, then spend bank on Warp Prism and Observer. Keep probes producing toward 32-40 workers. Do not expand until army supply >= 15 and production is sufficient.

**Recheck:** Next decision cycle: verify production >= 3, army supply >= 14, and bank < 1000.

### R02 — Counter Terran ground with detection and splash

**When:** If enemy composition shows Marines/Marauders with Medivacs or Widow Mines, and you have at least 2 Gateways and a Robotics Facility

**Correction:** Queue Immortals and a Observer for detection. Add a Templar Archives if tech allows, and prepare to warp in Sentries for Guardian Shield. Maintain a ground core of Stalkers and Zealots. Do not neglect air defense if enemy adds Vikings or Banshees.

**Recheck:** Next decision cycle: confirm Observer is active or queued, and army composition includes at least 2 Immortals or 2 Sentries.

### R03 — Recover from low army and high bank

**When:** If army supply < 15 and bank > 1500, or predicted advantage is OverwhelmingDisadvantage

**Correction:** Immediately convert bank into army: queue units from all production structures, add Gateways if supply allows, and warp in units. Prioritize Stalkers and Zealots. Do not expand or tech until army supply >= 20 and bank < 800.

**Recheck:** Next decision cycle: verify army supply >= 20 and bank < 800, or threat level reduced.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid over-defending early

**When:** Early game, around 180 seconds, with heavy economy and tech investment, moderate production, and opponent showing ground posture with Marines/Marauders.

**Mistake → correction:** Over-committing to defense at the expense of economy, or neglecting scouting for tech switches or all-ins. → Continue developing your economy and tech, and prepare to build a ground army.

**Why:** Early game is about establishing a strong economy and tech base to support future production.

**Read for full checks:** `N004`

### L02 — Avoid neglecting air defense

**When:** Early-midgame, around 240-360 seconds, with heavy economy and tech investment, moderate production, and opponent showing ground posture with possible early pressure.

**Mistake → correction:** Neglecting air defense, as the opponent may transition to air later, or over-extending your army without proper scouting. → Continue developing your economy and tech, strengthen your ground army, and maintain defensive readiness.

**Why:** This phase rewards economic and tech growth while staying safe against potential early pressure. A strong ground core with Sentry support provides defensive options.

**Read for full checks:** `N001`

### L03 — Avoid assuming enemy build without scouting

**When:** Early game, around 180 seconds, with heavy economy and tech investment, moderate production, and opponent showing possible Reaper opening.

**Mistake → correction:** Making assumptions about the enemy's build without scouting, or neglecting defense while teching. → Continue developing your economy and tech, and prepare to defend against early Reaper harassment.

**Why:** Reapers can harass early, so defensive positioning and scouting are important.

**Read for full checks:** `N005`

## Decision Nodes

### [DEFAULT] N001 — Early-Midgame Tech/Economy Development

**Trigger situation:**  
At around 240-360 seconds, you have a heavy economy and tech investment, with moderate production. The opponent shows a ground posture with possible early pressure.

**Direction:**  
Continue developing your economy and tech, strengthen your ground army, and maintain defensive readiness.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Army Strengthening

**Trigger situation:**  
At around 540-600 seconds, you have heavy production and tech, with a ground army including Stalkers, Warp Prisms, Observers, and Immortals. The opponent has a heavy ground posture with Marines and Marauders.

**Direction:**  
Continue strengthening your ground army, increase production, and maintain defensive awareness.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Late-Midgame Ground Army Consolidation

**Trigger situation:**  
At around 600-720 seconds, you have a heavy ground army with Stalkers, Warp Prisms, Observers, and Immortals. The opponent shows a ground posture with Marines, Reapers, Medivacs, and Widow Mines.

**Direction:**  
Continue strengthening your ground army, increase production, and maintain defensive awareness.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early Game Tech/Economy Foundation

**Trigger situation:**  
At around 180 seconds, you have a heavy economy and tech investment, with moderate production. The opponent shows a ground posture with Marines and Marauders.

**Direction:**  
Continue developing your economy and tech, and prepare to build a ground army.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game Tech/Economy Foundation (Reaper Variant)

**Trigger situation:**  
At around 180 seconds, you have a heavy economy and tech investment, with moderate production. The opponent shows a possible Reaper opening.

**Direction:**  
Continue developing your economy and tech, and prepare to defend against early Reaper harassment.

**Read for details:** `N005`

---
