# TvT_O04 Expansion / Economy / Technology

## Skill Identity

- Skill ID: TvT_O04
- Matchup: Terran vs Terran
- Opening Family: expansion / economy / technology opening
- Method: Executable Full V8

## Opening Strategy

A Terran mirror opening that prioritizes economy and technology development, with a flexible ground-oriented posture. Early game focuses on heavy economy and technology investment, transitioning to a strong ground army with Siege Tanks and Marines in the midgame.

Develop a strong economy and technology base while maintaining flexibility to adapt to opponent's composition, aiming for a midgame ground army with Siege Tank support.

This is a strategic template, not a fixed build order. Adapt based on live scouting and opponent's actions.

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

**When:** At 240-360 seconds, if bank exceeds 800 minerals and 400 gas, or if active production structures are fewer than 2, or if any production structure is idle with bank above 300 minerals.

**Correction:** Queue Marines from Barracks and ensure at least 2 Barracks are active; if Factory is available, queue a Siege Tank. Prioritize spending bank on production and army over expansions or upgrades. Keep workers producing toward saturation (target 2 per mineral line and 3 per gas).

**Recheck:** Recheck at next decision cycle: bank below 600 minerals and 300 gas, and all production structures have active queues.

### R02 — Enemy Composition Response

**When:** If enemy intelligence shows air units (e.g., Banshees, Medivacs, Vikings) or if threat flags indicate air harassment, and your army lacks anti-air capability.

**Correction:** Add a Tech Lab on a Barracks and queue a Marauder or produce a Viking from a Starport if available; if Starport is not built, prioritize constructing one. Maintain ground army production (Marines, Siege Tanks) while adding anti-air. Ensure at least one Engineering Bay is upgrading if feasible.

**Recheck:** Recheck at next decision cycle: army includes at least 2 anti-air units or a Starport with a Viking queued, and ground production remains active.

### R03 — Recovery from Low Army and High Bank

**When:** If army supply is below 15 and bank exceeds 1000 minerals and 500 gas, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all available production structures (Barracks, Factory, Starport) prioritizing Marines and Siege Tanks. If production structures are insufficient, construct additional Barracks (up to 3 total) and attach Tech Labs as needed. Do not expand or invest in upgrades until army supply is above 20 and bank is below 500 minerals.

**Recheck:** Recheck at next decision cycle: army supply above 20 and bank below 500 minerals, or production structures are all active with queues.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Midgame Ground vs. Air Flexibility

**When:** At around 540 seconds, both players have transitioned to a midgame ground army with Siege Tanks, Marines, and supporting units. The opponent shows moderate air presence.

**Mistake → correction:** Tempting to focus solely on strengthening your ground army and continuing production, economy, and technology without adding air units, leaving you vulnerable to drops or air harassment. → Increase your air presence to counter potential drops or air threats, continue strengthening your ground army, and maintain your economy.

**Why:** With both players having similar ground compositions, adding air units provides flexibility and counters potential medivac drops or air harassment.

**Read for full checks:** `N002`

### L02 — Late Midgame Sustained Pressure

**When:** At around 600 seconds, both players have a heavy ground army with Siege Tanks and Marines, and a moderate air presence. The opponent has a heavy defense.

**Mistake → correction:** Tempting to overcommit to ground forces and neglect air upgrades or economy, potentially losing a prolonged engagement due to lack of air support or resource exhaustion. → Continue strengthening your ground army, increase your air presence, and maintain your economy to support a long fight.

**Why:** With both players having strong ground armies, adding air units and maintaining a robust economy gives you an edge in the late game.

**Read for full checks:** `N005`

### L03 — Early Midgame Economy and Defense

**When:** At around 300 seconds, both players have a heavy economy and technology investment, with a ground-oriented army. The opponent shows possible pressure with Reapers and Hellions.

**Mistake → correction:** Tempting to over-extend or attack into a fortified position, or to neglect defensive readiness while focusing on economy and technology. → Continue developing your economy and technology, strengthen your ground army, and maintain defensive readiness.

**Why:** Both players are in a similar economic and technological state. Maintaining a strong economy and technology lead while building a versatile ground army positions you well for the midgame.

**Read for full checks:** `N001`

## Decision Nodes

### [DEFAULT] N001 — Early-Midgame Ground Development

**Trigger situation:**  
At around 300 seconds, both players have a heavy economy and technology investment, with a ground-oriented army. The opponent shows possible pressure with Reapers and Hellions.

**Direction:**  
Continue developing your economy and technology, strengthen your ground army, and maintain defensive readiness.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Siege Tank Transition

**Trigger situation:**  
At around 540 seconds, both players have transitioned to a midgame ground army with Siege Tanks, Marines, and supporting units. The opponent shows moderate air presence.

**Direction:**  
Increase your air presence to counter potential drops or air threats, continue strengthening your ground army, and maintain your economy.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Game Economy Focus

**Trigger situation:**  
At around 180 seconds, the opponent has a heavy economy and technology, with a ground army including Marines. Your own army composition is still unknown.

**Direction:**  
Focus on expanding your economy and technology, while scouting to determine the opponent's intentions.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early Game Ground Orientation

**Trigger situation:**  
At around 180 seconds, you have a ground-oriented army with Marines and Reapers, while the opponent's army composition is unknown but they have a heavy economy.

**Direction:**  
Continue developing your ground army and economy, while scouting to identify the opponent's plan.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Late Midgame Army Strengthening

**Trigger situation:**  
At around 600 seconds, both players have a heavy ground army with Siege Tanks and Marines, and a moderate air presence. The opponent has a heavy defense.

**Direction:**  
Continue strengthening your ground army, increase your air presence, and maintain your economy to support a long fight.

**Read for details:** `N005`

---
