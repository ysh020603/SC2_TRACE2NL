# ZvP_O01 Economy / Expansion / Production

## Skill Identity

- Skill ID: ZvP_O01
- Matchup: Zerg vs Protoss
- Opening Family: economy / expansion / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg opening that prioritizes economy and expansion while maintaining moderate production and light technology. The early game focuses on building a strong economic base with Queens and Zerglings for defense, then transitions into a heavier ground army with tech upgrades as the game progresses.

Develop a robust economy and expansion lead while preserving flexibility to adapt to Protoss tech choices, whether they commit to ground or air.

This is a strategic template, not a fixed build order. Adapt based on live scouting and enemy tech choices.

## Strategic Characteristics

- Economy: heavy
- Production: moderate
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

### R01 — Production Tempo and Bank Conversion

**When:** At any time, if bank is above 800 minerals and 400 gas, or if army supply is below 15 and production is idle or insufficient, or if supply is not blocked but production is not active.

**Correction:** Prioritize spending bank on production structures (e.g., Hatcheries, Roach Warrens, Hydralisk Den) and unit queues. Ensure at least 3 Hatcheries are active or queued by 6 minutes. If supply is not blocked, queue units from all Hatcheries. If supply is blocked, add an Overlord only if no supply provider is already completed, pending, or queued. Do not expand until army supply is at least 15 and production is active.

**Recheck:** Next decision cycle: verify bank is below 500 minerals and 200 gas, army supply is above 15, and all Hatcheries have active queues.

### R02 — Enemy Composition Response

**When:** When enemy intelligence reveals a significant air presence (e.g., Phoenixes, Oracles, Void Rays) or a heavy ground composition with Observers, and current army lacks appropriate counters.

**Correction:** If enemy has air units, add anti-air: build Spore Crawlers at each base and queue Hydralisks or Corruptors from existing production. If enemy has heavy ground with Observers, add Roaches or Hydralisks for anti-armor and ensure detection with Overseers. Continue expanding and teching as per opening, but prioritize these counters.

**Recheck:** Next decision cycle: verify at least one Spore Crawler per base or Hydralisk/Corruptor count is increasing, and detection is available if needed.

### R03 — Recovery from Low Army and High Bank

**When:** When army supply is below 15, bank is above 1000 minerals and 500 gas, or predicted advantage is OverwhelmingDisadvantage, or a threatened owned zone is detected.

**Correction:** Immediately convert bank into army: queue units from all Hatcheries, prioritize Zerglings and Roaches for quick defense. If production is insufficient, build additional Hatcheries. Do not expand or tech until army supply is above 15 and threat is mitigated. If supply is blocked, add an Overlord only if no supply provider is already completed, pending, or queued.

**Recheck:** Next decision cycle: verify army supply is above 15, bank is below 500 minerals and 200 gas, and production is active.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Anti-Air Defense

**When:** Early-midgame, around 6 minutes, when enemy shows Phoenixes and Oracles.

**Mistake → correction:** Ignoring air threats and continuing pure ground army without anti-air. → Maintain ground army while adding anti-air like Hydralisks or Spore Crawlers. Continue expanding and teching.

**Why:** Phoenix and Oracle can harass workers and pick off units. Anti-air protects economy and army.

**Read for full checks:** `N007`

### L02 — Ground Composition Counter

**When:** Late-midgame, around 10-12 minutes, when enemy has heavy ground army with Observers.

**Mistake → correction:** Being out-teched and not adapting composition to enemy's heavy ground. → Continue strengthening ground army and tech. Add Roaches or Hydralisks for anti-armor. Maintain map control and prepare for decisive battle.

**Why:** With strong economy, you can afford larger army and tech upgrades. Matching enemy composition with counters is key.

**Read for full checks:** `N008`

### L03 — Transition to Air

**When:** Late-midgame, around 10-12 minutes, when enemy has heavy air presence including Phoenixes and Oracles.

**Mistake → correction:** Staying pure ground against heavy air. → Transition to air units like Mutalisks or Corruptors to counter enemy air. Continue expanding and teching. Maintain ground defense.

**Why:** Air units can counter enemy air and provide harassment. Mixed army with anti-air is essential.

**Read for full checks:** `N009`

## Decision Nodes

### [DEFAULT] N001 — Early Economy and Queen Defense

**Trigger situation:**  
Early game, around 3 minutes, with limited enemy information and your own economy expanding.

**Direction:**  
Continue expanding and increasing economy while maintaining a defensive ground posture. Keep producing Queens for defense and creep spread.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Mid Transition to Ground Army

**Trigger situation:**  
Early-midgame, around 4-5 minutes, with enemy showing Zealots and Stalkers, indicating a ground-based army.

**Direction:**  
Strengthen your ground army by adding more Zerglings and possibly Roaches. Continue expanding and increasing production. Maintain defense while scouting for tech switches.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Army and Tech

**Trigger situation:**  
Midgame, around 9 minutes, with enemy having a heavy ground army including Sentries and Observers.

**Direction:**  
Continue strengthening your ground army and tech. Consider adding Roaches or Hydralisks for anti-armor. Maintain map control and prepare for a decisive battle.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early-Mid Expansion and Army

**Trigger situation:**  
Early-midgame, around 5-6 minutes, with enemy showing a ground army and you are expanding.

**Direction:**  
Continue expanding and increasing production. Strengthen your ground army with more Zerglings and possibly Roaches. Maintain scouting to detect any tech switches.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Ground Army Consolidation

**Trigger situation:**  
Midgame, around 7-8 minutes, with enemy having a ground army including Sentries.

**Direction:**  
Consolidate your ground army and tech. Consider adding Roaches or Hydralisks for durability. Maintain defense and continue expanding.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early-Mid Defensive Tech

**Trigger situation:**  
Early-midgame, around 5 minutes, with enemy hidden and you are focusing on economy.

**Direction:**  
Continue expanding and increasing production. Invest in defensive tech such as Lair for Overseers and possibly Roach Warren. Maintain scouting to detect enemy intentions.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early-Mid Air Defense

**Trigger situation:**  
Early-midgame, around 6 minutes, with enemy showing Phoenixes and Oracles, indicating an air commitment.

**Direction:**  
Maintain your ground army while preparing anti-air. Consider adding Hydralisks or Spore Crawlers for defense. Continue expanding and teching.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Late-Mid Ground Army and Tech

**Trigger situation:**  
Late-midgame, around 10-12 minutes, with enemy having a heavy ground army including Observers.

**Direction:**  
Continue strengthening your ground army and tech. Consider adding Roaches or Hydralisks for anti-armor. Maintain map control and prepare for a decisive battle.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Late-Mid Air Transition

**Trigger situation:**  
Late-midgame, around 10-12 minutes, with enemy having a heavy air presence including Phoenixes and Oracles.

**Direction:**  
Consider transitioning to air units like Mutalisks or Corruptors to counter the enemy's air. Continue expanding and teching. Maintain ground defense as well.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Early-Mid Air Defense and Economy

**Trigger situation:**  
Early-midgame, around 6 minutes, with enemy showing Phoenixes and Oracles, and you have a strong economy.

**Direction:**  
Maintain your ground army while preparing anti-air. Consider adding Hydralisks or Spore Crawlers for defense. Continue expanding and teching.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Midgame Air Transition

**Trigger situation:**  
Midgame, around 8-9 minutes, with enemy having a ground army and you are transitioning to air.

**Direction:**  
Continue building Mutalisks and upgrading them. Use them for harassment and to control the map. Maintain a ground army for defense.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Late-Mid Air Harassment

**Trigger situation:**  
Late-midgame, around 10-12 minutes, with enemy having a ground army and you have a strong air force.

**Direction:**  
Continue using Mutalisks to harass expansions and force the enemy to react. Maintain a strong ground army for defense. Consider adding Corruptors if the enemy transitions to air.

**Read for details:** `N012`

---
