# TvT_O01 Economy / Technology / Production

## Skill Identity

- Skill ID: TvT_O01
- Matchup: Terran vs Terran
- Opening Family: economy / technology / production opening
- Method: Prompt-Executable Full V9

## Opening Strategy

A Terran mirror opening that emphasizes heavy economy, production, and technology investment while maintaining a flexible ground-oriented posture. Early game focuses on establishing a strong macro foundation with light harassment potential.

Develop a robust economy and technology base while preserving flexibility to adapt to opponent actions and transition into a strong midgame ground army.

This is a strategic template, not a fixed build order. Adapt based on live observations and opponent behavior.

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

**When:** At any time, if bank is above 800 minerals and 400 gas, or if active production queues are empty and army supply is below 40, or if worker count is below 30 by 5 minutes.

**Correction:** Prioritize adding production structures (Barracks, Factory, Starport) up to a ratio of 3 per base, then queue units continuously. If supply is not blocked, spend bank on production and army. If worker count is below 30 by 5 minutes, queue SCVs from all Command Centers until saturation (about 22 per base).

**Recheck:** Recheck at next decision cycle: bank below 800 minerals and 400 gas, production queues non-empty, worker count at least 30 by 5 minutes.

### R02 — Enemy Composition Response

**When:** When enemy intelligence reveals a composition with air units (Banshees, Ravens, Vikings) or heavy ground with Siege Tanks, and your army lacks adequate anti-air or Siege Tanks.

**Correction:** If enemy has air units, add at least 2 Missile Turrets per base and produce Marines or Cyclones for anti-air. If enemy has Siege Tanks, produce your own Siege Tanks and ensure you have detection (Raven or scan). Continue expanding and teching to support the response.

**Recheck:** Recheck at next decision cycle: anti-air structures and units in place, or Siege Tanks produced, and detection available.

### R03 — Recovery from Low Army and High Bank

**When:** When army supply is below 15 and bank is above 1000 minerals, or when predicted advantage is OverwhelmingDisadvantage, or when a base is threatened.

**Correction:** Immediately convert bank into army: queue units from all production structures, add production if needed, and ensure supply is not blocked. If a base is threatened, prioritize defensive structures (Bunkers, Missile Turrets) and units. Do not expand until army supply is above 15 and production is active.

**Recheck:** Recheck at next decision cycle: army supply above 15, bank reduced, production active, and threat mitigated.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid greedy expansion without scouting

**When:** Early-midgame, around 5 minutes, when the opponent shows a ground posture with Siege Tanks and Marauders, and you have Marines and a heavy economy.

**Mistake → correction:** Expanding too greedily without proper scouting, risking being caught off guard by an enemy push. → Transition into a Siege Tank-based army to counter the opponent's ground composition, while continuing to expand and tech.

**Why:** Siege Tanks provide strong defensive and offensive capabilities against ground armies, especially in TvT.

**Read for full checks:** `N004`

### L02 — Avoid neglecting anti-air defenses

**When:** Late-midgame, around 10 minutes, when the opponent shows a ground posture with Siege Tanks, Reapers, Banshees, and Ravens, and you have a ground army with Siege Tanks, Marines, Reapers, and Hellions.

**Mistake → correction:** Neglecting anti-air defenses, leaving you vulnerable to Banshees and Ravens. → Diversify your tech to counter the opponent's mix, adding air defense and detection. Continue expanding and teching.

**Why:** The opponent's mix of air and ground units requires a balanced response. Heavy economy allows for tech diversification.

**Read for full checks:** `N010`

### L03 — Avoid neglecting upgrades or falling behind in army supply

**When:** Midgame, around 8 minutes, when both players have a moderate air presence and heavy ground armies, with you having Siege Tanks, Marines, Marauders, and Medivacs, and the opponent showing similar units.

**Mistake → correction:** Neglecting upgrades or falling behind in army supply, as the opponent may attempt a timing attack with Siege Tanks. → Maintain your balanced army composition and continue expanding. Consider adding air units for scouting and drop potential.

**Why:** A balanced army is versatile and can adapt to various opponent compositions. Heavy economy supports continued production.

**Read for full checks:** `N005`

## Decision Nodes

### [DEFAULT] N001 — Early Midgame Ground Development

**Trigger situation:**  
Around 4 minutes, both players have a heavy economy and production, with light air presence. You have Reapers and Hellions, while the opponent shows no reliable combat-unit cues.

**Direction:**  
Continue developing your ground army and economy, maintaining pressure with light harassment while scouting for opponent tech choices.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Army Strengthening

**Trigger situation:**  
Around 8 minutes, both players have a moderate air presence and heavy ground armies. You have Siege Tanks, Marines, Hellions, and Medivacs, while the opponent shows similar units.

**Direction:**  
Strengthen your ground army and increase air presence for medivac support. Continue expanding and teching to maintain an advantage.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Game Macro Foundation

**Trigger situation:**  
Around 3 minutes, the opponent's posture is unknown, but you have a ground-oriented army with Marines. Your economy is heavy, and you are expanding.

**Direction:**  
Focus on establishing a strong macro foundation, continuing to expand and tech while maintaining a defensive posture.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early Midgame Siege Tank Transition

**Trigger situation:**  
Around 5 minutes, the opponent shows a ground posture with Siege Tanks and Marauders. You have Marines and a heavy economy.

**Direction:**  
Transition into a Siege Tank-based army to counter the opponent's ground composition, while continuing to expand and tech.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Balanced Ground Army

**Trigger situation:**  
Around 8 minutes, both players have a moderate air presence and heavy ground armies. You have Siege Tanks, Marines, Marauders, and Medivacs, while the opponent shows similar units.

**Direction:**  
Maintain your balanced army composition and continue expanding. Consider adding air units for scouting and drop potential.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Late Midgame Defensive Strengthening

**Trigger situation:**  
Around 10 minutes, the opponent shows a ground posture with Siege Tanks and Marauders. You have a heavy ground army with Siege Tanks, Marines, Hellions, and Medivacs.

**Direction:**  
Strengthen your defenses and continue expanding. Consider adding more production structures to support a larger army.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early Game Reaper Harassment

**Trigger situation:**  
Around 3 minutes, both players have Reapers and a heavy economy. The opponent shows a ground posture with Reapers.

**Direction:**  
Use Reapers for harassment while continuing to expand and tech. Maintain map awareness to avoid losing Reapers.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early Game Macro Focus

**Trigger situation:**  
Around 3 minutes, the opponent's posture is unknown, but you have a ground-oriented army with Marines. Your economy is moderate, and you are expanding.

**Direction:**  
Focus on macro, expanding and teching while maintaining a defensive posture. Scout to gain information.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Early Game Marine-Marauder Pressure

**Trigger situation:**  
Around 3 minutes, the opponent shows a ground posture with Reapers. You have Marines and Marauders, with a heavy economy.

**Direction:**  
Apply pressure with your Marine-Marauder army while continuing to expand and tech. Use the army to deny the opponent's expansion.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Late Midgame Tech Diversification

**Trigger situation:**  
Around 10 minutes, the opponent shows a ground posture with Siege Tanks, Reapers, Banshees, and Ravens. You have a ground army with Siege Tanks, Marines, Reapers, and Hellions.

**Direction:**  
Diversify your tech to counter the opponent's mix, adding air defense and detection. Continue expanding and teching.

**Read for details:** `N010`

---
