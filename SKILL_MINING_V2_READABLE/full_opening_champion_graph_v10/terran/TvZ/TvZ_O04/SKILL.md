# TvZ_O04 Technology / Economy / Production

## Skill Identity

- Skill ID: TvZ_O04
- Matchup: Terran vs Zerg
- Opening Family: technology / economy / production opening
- Method: Opening-Champion Full V10

## Opening Strategy

A Terran opening that emphasizes heavy production and technology investment while maintaining a strong economy. The army is ground-leaning with early Reapers and Marines, transitioning into Siege Tanks and Medivacs. The strategy is to outscale the Zerg through superior tech and production, while staying flexible to adapt to the opponent's composition.

Develop a technology / economy / production posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

## Strategic Characteristics

- Economy: heavy
- Production: heavy
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

**When:** At 4-6 minutes, if bank exceeds 800 minerals and 400 gas, or if active production structures are fewer than 3 with army supply below 30.

**Correction:** Queue units from all completed production structures, prioritizing Marines and Reapers to maintain ground pressure. If a Factory and Starport are complete, add Siege Tank and Medivac production. If supply is not blocked, add a Barracks if production capacity is insufficient. Convert bank into army before expanding.

**Recheck:** Recheck at next decision cycle: bank below 400 minerals and 200 gas, and active production structures at least 3.

### R02 — Enemy Composition Response

**When:** If enemy intelligence reveals heavy air (Mutalisks) or heavy ground (Roaches, Zerglings) with high production, and your army lacks appropriate counters.

**Correction:** If air threat, add a Starport with Tech Lab and produce Vikings or Liberators, and ensure an Engineering Bay for missile turrets at bases. If ground threat, add Marauders from Barracks with Tech Lab and produce Siege Tanks from Factory. Maintain worker saturation and expand if safe.

**Recheck:** Recheck at next decision cycle: appropriate counter units in production or completed, and army composition diversified.

### R03 — Recovery from Low Army and High Bank

**When:** If army supply is below 15 and bank exceeds 1000 minerals and 500 gas, or predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all production structures, prioritizing combat units (Marines, Marauders, Siege Tanks). If production is idle, add Barracks or Factory. Do not expand. If supply is blocked, add a supply provider. Convert bank into army to stabilize defense.

**Recheck:** Recheck at next decision cycle: army supply above 20 and bank reduced below 500 minerals and 250 gas.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Late Midgame: Avoid Passive Ground Focus

**When:** Around 10 minutes, with a strong ground army (Siege Tanks, Marines, Medivacs, Widow Mines) and the opponent fielding heavy ground forces (Zerglings, Roaches, Queens) with heavy production and tech.

**Mistake → correction:** Sticking purely to ground forces and production, being too passive, and neglecting to scout for tech switches like Mutalisks. → Increase air presence and technology while continuing to strengthen the ground army. Expand and keep production going.

**Why:** The opponent's heavy production demands a diversified force; adding air units and tech provides a late-game edge.

**Read for full checks:** `N005`

### L02 — Early Midgame: Avoid Overcommitting Without Scouting

**When:** Around 5-6 minutes, with Marines and Reapers, heavy production and tech, against Zerglings and Queens with moderate production and tech.

**Mistake → correction:** Over-committing to a single tech path without scouting, potentially missing tech switches. → Continue to increase economy and expansion while maintaining production and tech. Keep the army strong.

**Why:** Heavy tech and production provide an advantage; expanding secures the lead.

**Read for full checks:** `N006`

### L03 — Early Game: Avoid Delaying Expansion

**When:** Around 3 minutes, with a Marine and heavy production, moderate economy, against Zerglings and Queens with moderate production and light tech.

**Mistake → correction:** Over-committing to early pressure if the Zerg has a strong defense, delaying expansion or production. → Increase economy and maintain production and tech. Keep the army strong and be ready to defend.

**Why:** Heavy production and tech give an advantage; maintaining economy allows outscaling the Zerg.

**Read for full checks:** `N007`

## Decision Nodes

### [DEFAULT] N001 — Early-Mid Game Tech and Production Ramp

**Trigger situation:**  
At around 4 minutes, you have a solid ground army with Siege Tanks, Marines, and Reapers, and your economy and production are heavy. The opponent is likely on a ground-focused macro build with Queens and light tech.

**Direction:**  
Continue strengthening your ground army while increasing your economy. Maintain your production and technology development, and keep your defenses up.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early Game Reaper Pressure and Expansion

**Trigger situation:**  
At around 3 minutes, you have a Reaper and heavy production, while the opponent is still in the early game with no reliable combat units seen. Your economy is heavy but your expansion is uncertain.

**Direction:**  
Increase your economy and expansion, while continuing to produce units and tech. Use the Reaper for scouting and harassment.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Mid-Game Ground Army Consolidation

**Trigger situation:**  
At around 8-9 minutes, you have a strong ground army with Siege Tanks, Marines, Reapers, and Medivacs. The opponent has a heavy ground army with Zerglings, Roaches, and Queens, and heavy tech.

**Direction:**  
Maintain your ground army strength and economy, while continuing to tech up. Keep your defenses solid and be ready to respond to aggression.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Mid-Game Tech and Expansion Push

**Trigger situation:**  
At around 7 minutes, you have a diverse army with Marines, Marauders, Hellions, and Medivacs, and a moderate air presence. The opponent has a heavy ground army with Zerglings and Queens, and heavy tech.

**Direction:**  
Increase your air presence and technology, while continuing to strengthen your ground army. Expand and keep your production going.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Late-Mid Game Army and Tech Upgrade

**Trigger situation:**  
At around 10 minutes, you have a strong ground army with Siege Tanks, Marines, Medivacs, and Widow Mines. The opponent has a heavy ground army with Zerglings, Roaches, and Queens, and heavy tech.

**Direction:**  
Increase your air presence and technology, while continuing to strengthen your ground army. Expand and keep your production going.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early-Mid Game Tech and Expansion

**Trigger situation:**  
At around 5-6 minutes, you have Marines and Reapers, with heavy production and tech. The opponent has Zerglings and Queens, with moderate production and tech.

**Direction:**  
Continue to increase your economy and expansion, while maintaining your production and tech. Keep your army strong.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early Game Marine and Expansion

**Trigger situation:**  
At around 3 minutes, you have a Marine and heavy production, with a moderate economy. The opponent has Zerglings and Queens, with moderate production and light tech.

**Direction:**  
Increase your economy and maintain your production and tech. Keep your army strong and be ready to defend.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early Game Marine and Reaper Pressure

**Trigger situation:**  
At around 3 minutes, you have Marines and a Reaper, with heavy production and tech. The opponent has no reliable combat units seen, with moderate production and light tech.

**Direction:**  
Continue to increase your economy and production, while maintaining your tech. Use the Reaper for scouting and harassment.

**Read for details:** `N008`

---
