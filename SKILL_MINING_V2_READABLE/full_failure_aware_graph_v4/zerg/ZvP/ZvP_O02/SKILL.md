# ZvP_O02 Economy / Expansion / Ground

## Skill Identity

- Skill ID: ZvP_O02
- Matchup: Zerg vs Protoss
- Opening Family: economy / expansion / ground opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg opening that prioritizes economy and expansion while maintaining a flexible ground-oriented posture. Early information is limited, so the plan emphasizes safe development and adaptation based on scouting.

Develop a strong economy and expand while keeping a ground army core, preserving flexibility to respond to Protoss tech or pressure.

This is a strategic template, not a fixed build order. Adjust based on live scouting and enemy actions.

## Strategic Characteristics

- Economy: light_or_uncertain
- Production: light_or_uncertain
- Technology: light_or_uncertain
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

### G05 — Zerg production interpretation

- Treat Hatchery/Lair/Hive count, larvae, Overlords, and worker/army larva competition as the production-capacity check.

## V4 Matchup-Specific Corrections

### R01 — Maintain Zerg production tempo and worker saturation

**When:** At any time before 6 minutes, if bank is above 800 minerals and either (a) active larvae plus hatchery count is below 3, or (b) workers are below 32 by 4 minutes or below 38 by 5 minutes.

**Correction:** Spend bank on hatcheries (up to 3 bases total) and inject larvae with queens; queue drones from all hatcheries until worker count reaches 38-44, but keep at least 2 larvae in reserve for defensive units if threat is detected.

**Recheck:** Recheck at next decision cycle: bank below 500, workers at target, and at least 3 hatcheries with active larvae.

### R02 — Counter Protoss ground composition with roaches

**When:** If enemy intelligence shows a ground-heavy Protoss army (Zealots, Stalkers, Sentries, or Immortals) and your army supply is below 30, or if you have fewer than 6 roaches.

**Correction:** Prioritize building roach warren if not already completed, then queue roaches from all hatcheries until you have at least 12 roaches; ensure you have enough supply (build overlords if needed) and keep 2-3 queens for creep and defense.

**Recheck:** Recheck at next decision cycle: roach count at least 12, roach warren completed, and army supply above 30.

### R03 — Recover from low army and high bank

**When:** If army supply is below 15 and bank is above 1500 minerals, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately convert bank into combat units: queue zerglings and roaches from all hatcheries, prioritizing roaches if enemy has stalkers/immortals; build additional hatcheries if larvae are insufficient, and ensure supply is not blocked by building overlords if needed.

**Recheck:** Recheck at next decision cycle: army supply above 25, bank below 800, and production capacity (hatcheries + larvae) sufficient to sustain unit production.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Avoid Straight-Up Fight

**When:** Midgame, enemy scouted as ground-heavy with Zealots, Stalkers, Sentries, possibly Immortals; your army is ground-based with Zerglings, Roaches, Queens.

**Mistake → correction:** Engaging in a straight-up fight without proper army composition, or over-investing in economy at the expense of defense. → Strengthen your ground army, continue teching, and add units that counter the enemy's composition (e.g., Roaches against Zealots/Stalkers).

**Why:** Matching the enemy's ground strength is necessary to hold off potential pushes and maintain map control.

**Read for full checks:** `N004`

### L02 — Unknown Enemy: Avoid Overcommitting Without Scouting

**When:** Early-midgame, enemy shows heavy economy and tech investment with moderate production; your army is ground-based with Zerglings and Queens.

**Mistake → correction:** Over-committing to an attack without knowing the opponent's composition, or neglecting scouting to confirm their greed. → Increase your economy and tech, strengthen your ground army, and keep scouting to identify the enemy's plan.

**Why:** Matching the enemy's economy and tech is important to avoid falling behind, while maintaining a defensive ground army.

**Read for full checks:** `N006`

### L03 — Stalker Ground: Avoid Straight-Up Fight

**When:** Early-midgame, enemy scouted with Stalkers and a heavy ground posture; your army is ground-based with Zerglings and Queens.

**Mistake → correction:** Engaging in a straight-up fight without proper army composition, or over-investing in economy at the expense of defense. → Strengthen your ground army, continue teching, and consider adding units that counter the enemy's composition (e.g., Roaches against Stalkers).

**Why:** Matching the enemy's ground strength is necessary to hold off potential pushes and maintain map control.

**Read for full checks:** `N007`

## Decision Nodes

### [DEFAULT] N001 — Midgame Unknown Posture

**Trigger situation:**  
At around 480-540 seconds, both sides have limited confirmed information. Enemy posture is unknown, and your own development is still flexible.

**Direction:**  
Maintain current development path, keep scouting, and avoid overcommitting to a specific army composition.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Midgame Unknown Posture

**Trigger situation:**  
At around 240-360 seconds, both sides are still in early-midgame with limited information. Enemy posture is unknown, and your own development is flexible.

**Direction:**  
Maintain current development path, keep scouting, and avoid overcommitting to a specific army composition.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Late-Midgame Unknown Posture

**Trigger situation:**  
At around 600-720 seconds, the game is in late-midgame. Enemy posture is still unknown, and your own development is flexible.

**Direction:**  
Maintain current development path, keep scouting, and avoid overcommitting to a specific army composition.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground vs Ground

**Trigger situation:**  
At around 480-540 seconds, enemy has been scouted as a ground-heavy Protoss with Zealots, Stalkers, Sentries, and possibly Immortals. Your own army is ground-based with Zerglings, Roaches, and Queens.

**Direction:**  
Strengthen your ground army, continue teching, and consider adding units that counter the enemy's composition (e.g., Roaches against Zealots/Stalkers).

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game Heavy Economy

**Trigger situation:**  
At around 180 seconds, enemy shows a heavy economy posture with moderate production and heavy tech investment, but no confirmed combat units.

**Direction:**  
Maintain your development, focus on economy and scouting to determine the enemy's tech path.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early-Midgame Heavy Economy

**Trigger situation:**  
At around 240 seconds, enemy shows a heavy economy and tech investment, with moderate production. Your own army is ground-based with Zerglings and Queens.

**Direction:**  
Increase your economy and tech, strengthen your ground army, and keep scouting to identify the enemy's plan.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early-Midgame Ground vs Ground

**Trigger situation:**  
At around 360 seconds, enemy has been scouted with Stalkers and a heavy ground posture. Your own army is ground-based with Zerglings and Queens.

**Direction:**  
Strengthen your ground army, continue teching, and consider adding units that counter the enemy's composition (e.g., Roaches against Stalkers).

**Read for details:** `N007`

---

### [DEFAULT] N008 — Late-Midgame Ground vs Ground

**Trigger situation:**  
At around 600 seconds, enemy has been scouted with Stalkers and a heavy ground posture. Your own army is ground-based with Queens and possibly Zerglings.

**Direction:**  
Continue to strengthen your ground army, increase production, and consider adding upgrades or tech to counter the enemy's composition.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Early Game Heavy Tech

**Trigger situation:**  
At around 180 seconds, enemy shows a heavy tech investment with moderate economy and light production. Your own economy is moderate with a heavy expansion.

**Direction:**  
Increase your economy and tech, strengthen your ground army, and keep scouting to identify the enemy's plan.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Early Game Heavy Tech

**Trigger situation:**  
At around 180 seconds, enemy shows a heavy tech investment with moderate economy and light production. Your own economy is moderate with a heavy expansion.

**Direction:**  
Increase your economy and tech, strengthen your ground army, and keep scouting to identify the enemy's plan.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early-Midgame Heavy Economy

**Trigger situation:**  
At around 240 seconds, enemy shows a heavy economy and tech investment, with heavy production. Your own army is ground-based with no confirmed units.

**Direction:**  
Increase your economy and tech, strengthen your ground army, and keep scouting to identify the enemy's plan.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Late-Midgame Ground vs Ground

**Trigger situation:**  
At around 600 seconds, enemy has been scouted with Stalkers and a heavy ground posture. Your own army is ground-based with Zerglings.

**Direction:**  
Continue to strengthen your ground army, increase production, and consider adding upgrades or tech to counter the enemy's composition.

**Read for details:** `N012`

---
