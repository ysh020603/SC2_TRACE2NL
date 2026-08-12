# PvT_O04 Technology / Defense / Economy

## Skill Identity

- Skill ID: PvT_O04
- Matchup: Protoss vs Terran
- Opening Family: technology / defense / economy opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Protoss opening that emphasizes heavy technology investment, a solid defensive posture, and a strong economy. It aims to develop a versatile foundation that can transition into either a ground or air-oriented army based on scouting information.

Develop a technology / defense / economy posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

## Strategic Characteristics

- Economy: moderate
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

### R01 — Maintain tech-defense tempo with continuous production

**When:** Before 6 minutes, with heavy tech investment and moderate production, and bank above 800 minerals or 400 gas.

**Correction:** Prioritize completing prerequisite tech structures and keep all existing production structures active. If any production structure is idle or has an empty queue, add a unit to its queue. If army supply is below 15, do not expand; instead, convert bank into additional production structures (e.g., Warp Gates) and units. Ensure worker production continues toward saturation without exceeding 2 per base.

**Recheck:** At the next decision cycle, verify that all production structures have active queues and that bank has decreased by at least 300 minerals or 200 gas.

### R02 — Counter Terran ground composition with tech and defense

**When:** Enemy Intelligence shows a ground-heavy Terran army with Marines, Reapers, or Siege Tanks, and your army supply is below 30.

**Correction:** If Siege Tanks are detected, prioritize Dark Templar tech and add a Dark Shrine if not already present. If Reapers are present, ensure at least one Stalker or Adept per Reaper and consider a Robo for Observer or Immortal. Maintain a defensive posture with Photon Cannons at natural and third expansions if threatened. Continue producing from all structures, prioritizing units that counter the observed composition.

**Recheck:** At the next decision cycle, confirm that the required tech structures are completed or queued, and that army supply has increased by at least 5.

### R03 — Recover from low army and high bank with defensive production

**When:** Army supply is below 15, bank exceeds 1500 minerals or 800 gas, or predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately convert bank into army and production: add Warp Gates or Robo facilities if production is insufficient, and queue units from all structures. Do not expand or invest in new technology until army supply is above 20. If threatened, add defensive structures (Photon Cannons) at vulnerable bases. Prioritize units that counter the enemy's known composition.

**Recheck:** At the next decision cycle, verify that army supply has increased by at least 5 and bank has decreased by at least 500 minerals or 300 gas.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid head-on engagement against Siege Tank lines

**When:** Midgame, around 9 minutes, with a heavy ground army and heavy tech. Opponent has a strong ground army with Siege Tanks and Medivacs.

**Mistake → correction:** Engaging head-on into a well-positioned Siege Tank line without proper support or a plan to break it. → Continue strengthening your ground army and increase production. Maintain your defensive posture while preparing for a potential engagement.

**Why:** Your ground army is well-suited to counter the Terran's composition. Dark Templars can be effective against Siege Tanks if positioned well.

**Read for full checks:** `N002`

### L02 — Avoid over-extending with expansions or tech

**When:** Early-midgame, around 5-6 minutes, with heavy production and tech. Opponent shows a ground posture with Marines and Reapers.

**Mistake → correction:** Over-extending with expansions or tech that leaves you vulnerable to early pressure. → Maintain your defensive posture while increasing your production and tech. Continue to expand to support your growing army.

**Why:** A strong economy and tech advantage will allow you to outproduce the opponent in the mid-game. Your defensive structures buy you time.

**Read for full checks:** `N003`

### L03 — Avoid over-committing to expansions or air units

**When:** Early-midgame, around 4-5 minutes, with heavy tech investment and moderate production. Opponent shows a ground posture with Reapers.

**Mistake → correction:** Over-committing to expansions or air units before confirming the opponent's intentions, leaving you exposed to early aggression. → Continue to invest in technology while maintaining a defensive posture. Keep your options open for either a ground or air transition.

**Why:** Heavy tech investment gives you flexibility to counter the opponent's eventual composition. A defensive posture prevents early game losses.

**Read for full checks:** `N004`

## Decision Nodes

### [DEFAULT] N001 — Early Game Stabilization

**Trigger situation:**  
Early game, around 3 minutes, with heavy technology investment and moderate production. Opponent shows a ground posture with possible Reaper pressure.

**Direction:**  
Focus on stabilizing your defense while continuing to develop your economy and technology. Maintain a defensive posture to deter early aggression.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Army Development

**Trigger situation:**  
Midgame, around 9 minutes, with a heavy ground army and heavy tech. Opponent has a strong ground army with Siege Tanks and Medivacs.

**Direction:**  
Continue strengthening your ground army and increase production. Maintain your defensive posture while preparing for a potential engagement.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early-Midgame Expansion and Tech

**Trigger situation:**  
Early-midgame, around 5-6 minutes, with heavy production and tech. Opponent shows a ground posture with Marines and Reapers.

**Direction:**  
Maintain your defensive posture while increasing your production and tech. Continue to expand to support your growing army.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early-Midgame Tech Investment

**Trigger situation:**  
Early-midgame, around 4-5 minutes, with heavy tech investment and moderate production. Opponent shows a ground posture with Reapers.

**Direction:**  
Continue to invest in technology while maintaining a defensive posture. Keep your options open for either a ground or air transition.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Late-Midgame Ground/Air Hybrid

**Trigger situation:**  
Late-midgame, around 10-12 minutes, with a heavy ground army and some air support. Opponent has a heavy ground army with Marines.

**Direction:**  
Continue to strengthen your ground army while adding air support to deal with potential threats. Maintain your defensive posture.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early Game Tech and Defense

**Trigger situation:**  
Early game, around 3 minutes, with heavy tech investment and moderate production. Opponent's posture is unknown, but a Marine is seen.

**Direction:**  
Focus on stabilizing your defense and continuing your tech investment. Keep your options open for either a ground or air transition.

**Read for details:** `N006`

---
