# TvZ_O05 Technology / Economy / Production

## Skill Identity

- Skill ID: TvZ_O05
- Matchup: Terran vs Zerg
- Opening Family: technology / economy / production opening
- Method: Prompt-Executable Full V9

## Opening Strategy

A Terran opening that emphasizes heavy technology and economy while keeping production moderate, aiming for a flexible ground-oriented midgame.

Develop a technology / economy / production posture while preserving flexibility for live observation-driven adaptation.

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

### G05 — Terran production interpretation

- Scale Barracks/Factory/Starport capacity before ordering add-ons or units that lack a completed parent structure.

## V4 Matchup-Specific Corrections

### R01 — Production Tempo and Bank Conversion

**When:** At any point before 6 minutes, if bank is above 400 minerals or 200 gas, or if active production queues are empty while army supply is below 30.

**Correction:** Queue units from all available production structures, prioritizing marines, marauders, and tanks. If no production structures are available, build a Barracks or Factory if prerequisites are met. If supply is not blocked and bank remains high after queuing, add one additional production structure if resources allow, but do not exceed 3 total production structures before 6 minutes.

**Recheck:** Recheck at next decision cycle.

### R02 — Enemy Composition Response

**When:** If enemy intelligence reveals a heavy ground composition with possible air (e.g., Roach/Ravager or Hydralisk), or if air units are detected (e.g., Mutalisks, Corruptors).

**Correction:** Ensure at least 2 Missile Turrets per base if air threat is detected. Add a Starport with a Tech Lab and produce Vikings or Liberators if air units are confirmed. Continue producing ground units (Marines, Marauders, Tanks) to maintain ground strength. If no air threat is detected, focus on ground upgrades and production.

**Recheck:** Recheck at next decision cycle.

### R03 — Recovery from Low Army and High Bank

**When:** If army supply is below 15 and bank is above 1000 minerals or 500 gas, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all production structures, prioritizing combat units (Marines, Marauders, Tanks). If production is insufficient, build additional Barracks or Factory if prerequisites are met. Do not expand or invest in technology until army supply is above 30 and bank is below 500 minerals. If supply is blocked, build a Supply Depot if no supply provider is already queued or completed.

**Recheck:** Recheck at next decision cycle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Stabilize before expanding

**When:** Early-midgame, own ground army with heavy production and tech, opponent ground with light air.

**Mistake → correction:** Risky aggression or overexpansion without sufficient army strength or defense. → Stabilize then develop, increase production, maintain ground strength.

**Why:** Ensure safety before expanding further, leveraging tech advantage.

**Read for full checks:** `N004`

### L02 — Add air flexibility while maintaining ground

**When:** Midgame, own ground army with heavy production and tech, opponent heavy ground with possible air.

**Mistake → correction:** Over-investing in air without proper scouting, or neglecting upgrades. → Increase air presence, strengthen ground army, continue tech and production.

**Why:** Maintain ground dominance while adding air flexibility to counter potential tech switches.

**Read for full checks:** `N002`

### L03 — Prepare defense for late-game

**When:** Late-midgame, own heavy ground army, opponent heavy ground with possible air.

**Mistake → correction:** Neglecting anti-air, as Mutalisks can harass. → Increase defense, continue tech, strengthen ground army.

**Why:** Prepare for potential late-game engagements with solid defense.

**Read for full checks:** `N007`

## Decision Nodes

### [DEFAULT] N001 — Early Tech/Economy Development

**Trigger situation:**  
Early game, own posture unknown but heavy tech/economy, opponent ground macro with light air.

**Direction:**  
Continue developing economy and technology, strengthen ground forces, maintain defense.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Army Strengthening

**Trigger situation:**  
Midgame, own ground army with heavy production/tech, opponent heavy ground with possible air.

**Direction:**  
Increase air presence, strengthen ground army, continue tech and production.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Heavy Production Push

**Trigger situation:**  
Early game, own heavy production/tech, opponent ground macro with light air.

**Direction:**  
Increase production, continue tech, strengthen ground forces.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early-Mid Stabilization

**Trigger situation:**  
Early-midgame, own ground army with heavy production/tech, opponent ground with light air.

**Direction:**  
Stabilize then develop, increase production, maintain ground strength.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early-Mid Tech Development

**Trigger situation:**  
Early-midgame, own ground army with heavy tech, opponent ground with light air.

**Direction:**  
Continue tech development, maintain ground army, increase economy.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early-Mid Harass and Expand

**Trigger situation:**  
Early-midgame, own ground army with Reapers/Hellions, opponent ground with light air.

**Direction:**  
Continue harassment, expand, maintain ground army.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Late-Midgame Defense and Tech

**Trigger situation:**  
Late-midgame, own heavy ground army, opponent heavy ground with possible air.

**Direction:**  
Increase defense, continue tech, strengthen ground army.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Air Transition

**Trigger situation:**  
Midgame, own ground army, opponent ground with moderate air presence.

**Direction:**  
Maintain current army path, consider air defense.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Early Game Flexibility

**Trigger situation:**  
Early game, own posture unknown with moderate economy, opponent ground macro.

**Direction:**  
Maintain current path, keep options open.

**Read for details:** `N009`

---
