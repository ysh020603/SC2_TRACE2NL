# TvP_O02 Technology / Economy / Production

## Skill Identity

- Skill ID: TvP_O02
- Matchup: Terran vs Protoss
- Opening Family: technology / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

This opening focuses on developing a technology and economy foundation while keeping production flexible. Early game is characterized by light or uncertain production and technology, with the option to transition into a heavier ground-oriented composition as the game progresses.

Develop a technology / economy / production posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

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

### G05 — Terran production interpretation

- Scale Barracks/Factory/Starport capacity before ordering add-ons or units that lack a completed parent structure.

## V4 Matchup-Specific Corrections

### R01 — Production Tempo with Tech/Economy Balance

**When:** At 4-6 minutes, if army supply is below 10 and bank is above 800, or if production structures are fewer than 2 and supply is below 30.

**Correction:** Prioritize building additional production structures (Barracks, Factory, Starport) up to at least 3 total, and queue units from existing structures to keep them active. Continue tech upgrades only if bank remains above 500 after production investment. Avoid expanding until army supply is at least 15 and production is active.

**Recheck:** Recheck at next decision cycle: ensure army supply is at least 10, production structures are at least 3, and no production structure is idle for more than 10 seconds.

### R02 — Counter Ground Composition with Marauders and Siege Tanks

**When:** If enemy intelligence shows a ground-heavy Protoss composition with Zealots and Stalkers or Sentries, and your army includes Marines and Reapers.

**Correction:** Add Marauders from Barracks with Tech Labs, and if tech allows, produce Siege Tanks from Factories. Prioritize these units over other tech investments. Ensure at least 2 Barracks with Tech Labs and 1 Factory with Tech Lab are active. Queue Marauders and Siege Tanks to maintain a mix that counters Zealots and Stalkers.

**Recheck:** Recheck at next decision cycle: confirm enemy composition remains ground-heavy, and adjust production if they transition to air or other tech.

### R03 — Recovery from Low Army and High Bank

**When:** If army supply is below 15 and bank is above 1500, or if predicted advantage is OverwhelmingDisadvantage, or if any owned base is threatened.

**Correction:** Immediately convert bank into army by producing units from all available production structures, prioritizing combat units over workers and tech. If production is insufficient, build additional production structures (up to 4-5 total) and queue units. Do not expand or invest in new tech until army supply is at least 20 and bank is below 500. If threatened, also produce defensive units like Siege Tanks or Bunkers.

**Recheck:** Recheck at next decision cycle: army supply should be at least 20, bank below 500, and production structures active. If still low, continue the recovery process.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Match Opponent's Economy

**When:** Early game when opponent has heavy economy and technology, moderate production, and your own economy is moderate with heavy technology.

**Mistake → correction:** Focusing on technology and economy while neglecting army production, leaving you vulnerable to an attack. → Increase your economy and production to match the opponent's heavy economy, while continuing technology development.

**Why:** The opponent's heavy economy and technology indicate a macro-oriented game; matching their economy and production keeps you competitive.

**Read for full checks:** `N006`

### L02 — Counter Ground Composition

**When:** Late-midgame when both sides have ground posture, opponent has Zealots and Stalkers with heavy economy, production, and technology, and your ground forces include Marines, Reapers, and Widow Mines.

**Mistake → correction:** Neglecting upgrades or tech that could give the opponent an advantage in the ground engagement. → Strengthen your ground forces further, considering adding Siege Tanks or Marauders to counter Zealots and Stalkers.

**Why:** The opponent's ground army is strong; Siege Tanks provide area denial and Marauders are effective against Zealots.

**Read for full checks:** `N007`

### L03 — Adapt to Sentry Threats

**When:** Early-midgame when opponent has ground posture with Zealots and Sentries, heavy economy, production, and technology, and your ground forces include Marines.

**Mistake → correction:** Over-committing to a single unit composition that could be countered by Sentry abilities. → Strengthen your ground forces, considering adding Marauders to counter Zealots and Sentries.

**Why:** The opponent's ground army is strong; Marauders are effective against Zealots and can help break Sentry force fields.

**Read for full checks:** `N008`

## Decision Nodes

### [DEFAULT] N001 — Early Game Development with Safety Checks

**Trigger situation:**  
At the start of the game, both sides are in an early phase with limited information. The opponent's posture is unknown, and your own production and technology are light or uncertain.

**Direction:**  
Maintain current development path with a focus on economy and technology. Keep production flexible and avoid committing to a specific army composition.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Mid Game Development Continuation

**Trigger situation:**  
As the game progresses into the early-mid game, the situation remains largely unknown. Both sides are still developing, with no significant combat-unit cues.

**Direction:**  
Continue maintaining your current development path. Keep production and technology investment balanced, and avoid unnecessary risks.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Development with Safety Checks

**Trigger situation:**  
Entering the midgame, the situation remains unclear. The opponent's posture is still unknown, and your own development is still light or uncertain.

**Direction:**  
Continue maintaining your current development path. Keep production and technology investment balanced, and avoid unnecessary risks.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Development with Safety Checks

**Trigger situation:**  
In the late-midgame, the situation remains unclear. The opponent's posture is still unknown, and your own development is still light or uncertain.

**Direction:**  
Continue maintaining your current development path. Keep production and technology investment balanced, and avoid unnecessary risks.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Ground Posture Adaptation

**Trigger situation:**  
Early-midgame: The opponent shows a ground posture with Zealots, heavy economy and expansion, and heavy technology. Your own posture is still unknown.

**Direction:**  
Maintain your current development path while preparing to strengthen your ground forces. Consider adding units that counter Zealots, such as Marauders or Hellions.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early Game Heavy Economy and Technology

**Trigger situation:**  
Early game: The opponent has a heavy economy and expansion, with moderate production and heavy technology. Your own economy is moderate, and technology is heavy.

**Direction:**  
Increase your economy and production to match the opponent's heavy economy. Continue technology development.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Late-Midgame Ground vs Ground

**Trigger situation:**  
Late-midgame: Both sides have a ground posture. The opponent has Zealots and Stalkers, heavy economy, production, and technology. Your own ground forces include Marines, Reapers, and Widow Mines.

**Direction:**  
Strengthen your ground forces further. Consider adding Siege Tanks or Marauders to counter the opponent's Zealot and Stalker composition.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early-Midgame Ground vs Ground

**Trigger situation:**  
Early-midgame: The opponent has a ground posture with Zealots and Sentries, heavy economy, production, and technology. Your own ground forces include Marines.

**Direction:**  
Strengthen your ground forces. Consider adding Marauders to counter Zealots and Sentries.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Early Game Heavy Economy and Technology

**Trigger situation:**  
Early game: The opponent has a heavy economy and expansion, with moderate production and heavy technology. Your own economy is moderate, and expansion is heavy.

**Direction:**  
Increase your economy and production to match the opponent's heavy economy. Continue technology development.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Early-Midgame Ground vs Ground

**Trigger situation:**  
Early-midgame: The opponent has a ground posture with Zealots and Sentries, heavy economy, production, and technology. Your own ground forces include Marines.

**Direction:**  
Strengthen your ground forces. Consider adding Marauders to counter Zealots and Sentries.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early-Midgame Unknown vs Unknown

**Trigger situation:**  
Early-midgame: The opponent has a heavy economy and expansion, with moderate production and heavy technology. Your own economy is moderate, and expansion is heavy.

**Direction:**  
Strengthen your ground forces. Consider adding Marauders to counter Zealots.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Midgame Ground vs Ground

**Trigger situation:**  
Midgame: The opponent has a ground posture with Zealots, heavy economy, production, and technology. Your own ground forces include Marines.

**Direction:**  
Strengthen your ground forces. Consider adding Marauders or Siege Tanks to counter Zealots.

**Read for details:** `N012`

---
