# TvT_O06 Technology / Economy / Production

## Skill Identity

- Skill ID: TvT_O06
- Matchup: Terran vs Terran
- Opening Family: technology / economy / production opening
- Method: Knowledge-Constrained Executable Full V14

## Opening Strategy

A Terran mirror opening that emphasizes heavy technology and economy investment while maintaining a moderate production base. The early game is characterized by a ground-oriented posture with possible early pressure from Reapers or Marines. The strategic focus is on developing a strong macro foundation and tech advantage, with flexibility to adapt to opponent moves.

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

### R01 — Maintain production tempo and economy

**When:** At any time before 6 minutes, if army supply is below 15 and bank is above 800, or if production structures are fewer than 3 and bank is above 600.

**Correction:** Queue additional Barracks or Factory if prerequisites are met, prioritizing production structures over expansions. Ensure workers are continuously produced up to saturation (around 22 per base) without exceeding supply. Convert excess minerals into production structures and army units.

**Recheck:** Recheck at next decision cycle.

### R02 — Counter enemy composition

**When:** If enemy intelligence shows a ground-heavy composition with Marines and Siege Tanks, and you have Siege Tanks and Marines.

**Correction:** Maintain a balanced ground army, adding Siege Tanks for defensive positioning. Continue increasing economy and production, and ensure tech upgrades are progressing. Avoid attacking into fortified positions without Siege Tank support.

**Recheck:** Recheck at next decision cycle.

### R03 — Recover from low army and high bank

**When:** If army supply is below 15 and bank is above 1500, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately convert bank into army units by queueing units from all available production structures. Prioritize combat units over economy or technology. If production is insufficient, add production structures first. Do not expand until army supply is above 15 and production is active.

**Recheck:** Recheck at next decision cycle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Siege Tank Support

**When:** Early midgame (~5 min) with both players ground-oriented, heavy economy and tech, opponent shows Marine cues, you have Siege Tanks and Marines.

**Mistake → correction:** Pushing without Siege Tank support or into a fortified position. → Continue strengthening your ground army, particularly with Siege Tanks for defensive positioning. Increase economy and maintain production and tech.

**Why:** Siege Tanks provide strong defensive and positional advantages in TvT. Maintaining a heavy economy and tech allows transition to advanced units if needed.

**Read for full checks:** `N003`

### L02 — Avoid Tank Pushes

**When:** Midgame (~7 min) with opponent ground posture with Marines, you have Marines and Marauders.

**Mistake → correction:** Attacking into Siege Tanks without proper positioning or support. → Maintain your ground army and continue increasing economy. Keep production and tech steady.

**Why:** A balanced Marine/Marauder composition is strong in TvT. Maintaining economy and tech allows adaptation to opponent's composition.

**Read for full checks:** `N007`

### L03 — Avoid Siege Stalemate

**When:** Late midgame (~10 min) with opponent ground posture with Marines, you have Siege Tanks, Marines, Marauders, and Hellions.

**Mistake → correction:** Getting into a siege war without breaking their defenses; failing to use mobility to force engagements. → Maintain your ground army and continue increasing economy. Keep production and tech steady.

**Why:** Your army composition is strong and versatile. Maintaining economy and tech ensures sustainability and response to opponent moves.

**Read for full checks:** `N008`

## Decision Nodes

### [DEFAULT] N001 — Early Game Ground Macro with Heavy Tech

**Trigger situation:**  
Early game (around 3 minutes) with both players having a ground-oriented posture, heavy economy, and heavy technology investment. Opponent shows light or uncertain air presence and possible Reaper cues.

**Direction:**  
Continue developing your ground forces and economy while maintaining defensive structures. Increase economy and continue technology upgrades. Keep production steady.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early Game Heavy Production with Moderate Economy

**Trigger situation:**  
Early game (around 3 minutes) with opponent showing a ground posture and possible Reaper cues. Your own posture is ground-oriented with heavy production and heavy technology, but economy is moderate.

**Direction:**  
Increase your economy to catch up to your heavy production and technology. Maintain production and continue technology upgrades. Keep defense solid.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Midgame Ground Army with Siege Tanks

**Trigger situation:**  
Early midgame (around 5 minutes) with both players having a ground-oriented posture, heavy economy, and heavy technology. Opponent shows possible Marine cues, and you have Siege Tanks and Marines.

**Direction:**  
Continue strengthening your ground army, particularly with Siege Tanks for defensive positioning. Increase economy and maintain production and tech.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground Army with Air Transition

**Trigger situation:**  
Midgame (around 7-9 minutes) with opponent showing a ground posture with Siege Tanks, Reapers, Hellions, and Ravens. Your own posture is ground-oriented with heavy production and tech, and you have Marines.

**Direction:**  
Increase air presence and strengthen ground forces. Continue expanding and increasing economy and technology. Maintain production.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Midgame Stabilize and Develop

**Trigger situation:**  
Early midgame (around 5 minutes) with opponent showing a ground posture and possible Reaper cues. Your own posture is ground-oriented with heavy production and tech, and you have Marauders.

**Direction:**  
Stabilize your position and then develop. Increase production and economy, maintain defense and tech.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early Midgame Defensive Expansion

**Trigger situation:**  
Early midgame (around 6 minutes) with opponent showing a ground posture with Marines and Reapers. Your own posture is ground-oriented with heavy production and tech, and you have Siege Tanks and Marines.

**Direction:**  
Increase defense and expansion. Continue production and tech, and increase economy.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Midgame Ground Army with Marines and Marauders

**Trigger situation:**  
Midgame (around 7 minutes) with opponent showing a ground posture with Marines. Your own posture is ground-oriented with heavy production and tech, and you have Marines and Marauders.

**Direction:**  
Maintain your ground army and continue increasing economy. Keep production and tech steady.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Late Midgame Ground Army with Siege Tanks

**Trigger situation:**  
Late midgame (around 10 minutes) with opponent showing a ground posture with Marines. Your own posture is ground-oriented with heavy production and tech, and you have Siege Tanks, Marines, Marauders, and Hellions.

**Direction:**  
Maintain your ground army and continue increasing economy. Keep production and tech steady.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Late Midgame Defensive Expansion with Air

**Trigger situation:**  
Late midgame (around 10 minutes) with opponent showing a ground posture with Marines, Reapers, Marauders, and Hellions. Your own posture is ground-oriented with heavy production and tech, and you have Siege Tanks, Marines, and Reapers.

**Direction:**  
Increase defense and expansion. Continue production and tech, and increase economy.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Midgame Air Transition with Ground Core

**Trigger situation:**  
Midgame (around 8-9 minutes) with opponent showing a ground posture with Siege Tanks, Reapers, and Battlecruisers. Your own posture is ground-oriented with heavy production and tech, and you have Siege Tanks, Marines, Marauders, and Hellions.

**Direction:**  
Increase air presence and strengthen air forces. Continue expanding and increasing economy and technology. Maintain production.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Midgame Maintain Current Army Path

**Trigger situation:**  
Midgame (around 9 minutes) with opponent showing a ground posture with Marines, Marauders, Hellions, and Widow Mines. Your own posture is ground-oriented with heavy production and tech, and you have Siege Tanks and Marines.

**Direction:**  
Maintain your current army path and continue developing. Keep economy, production, and tech steady.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Late Midgame Air Transition with Ground Core

**Trigger situation:**  
Late midgame (around 10 minutes) with opponent showing a ground posture with Marines and Medivacs. Your own posture is ground-oriented with heavy production and tech, and you have Siege Tanks, Marines, Medivacs, and Ravens.

**Direction:**  
Increase air presence and strengthen air forces. Continue expanding and increasing economy and technology. Maintain production.

**Read for details:** `N012`

---
