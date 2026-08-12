# TvT_O05 Technology / Economy / Production

## Skill Identity

- Skill ID: TvT_O05
- Matchup: Terran vs Terran
- Opening Family: technology / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Terran mirror opening that prioritizes heavy economy and technology investment while maintaining a flexible ground-oriented posture. Production is moderate early, scaling to heavy as the game progresses.

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

**When:** At any time, if bank exceeds 800 minerals and 400 gas, or if active production structures are fewer than 2 by 5:00 or fewer than 3 by 6:00, or if any production structure is idle with bank above 300 minerals.

**Correction:** Queue units from all idle production structures, prioritizing Marines and Marauders. If bank remains above 1000 minerals and 500 gas after queuing, add a Barracks (or Factory if tech lab available) to increase production. Continue adding production until bank is below 600 minerals and 300 gas. Do not expand until army supply is at least 15 and production is active.

**Recheck:** Recheck at next decision cycle: verify bank is below 600 minerals and 300 gas, and all production structures have active queues.

### R02 — Enemy Composition Response

**When:** If enemy intelligence reveals any of: Battlecruisers, Banshees, or Medivacs with Hellions (drop threat), or if enemy has more than 2 air units and your anti-air supply is below 4.

**Correction:** If enemy has Battlecruisers or Banshees, build a Tech Lab on a Starport and produce Vikings (or Ravens if detection needed). If enemy has Medivacs with Hellions, add a Missile Turret at each mineral line and produce at least 2 Vikings or Medivacs for defense. Continue ground production and tech upgrades. Maintain economy and expand only if army supply is above 15 and production is active.

**Recheck:** Recheck at next decision cycle: verify anti-air supply is at least 4 and defensive structures are in place.

### R03 — Recovery from Low Army or High Bank

**When:** If army supply is below 15 and bank is above 1000 minerals, or if predicted advantage is OverwhelmingDisadvantage, or if any owned base is threatened.

**Correction:** Immediately queue units from all production structures, prioritizing combat units (Marines, Marauders, Siege Tanks). If production is insufficient (fewer than 3 Barracks or equivalent), add a Barracks or Factory. Convert all available resources into army, not expansions or tech. If threatened, produce defensive units and consider building a Bunker at the threatened base. Do not expand until army supply is above 15 and threat is cleared.

**Recheck:** Recheck at next decision cycle: verify army supply is above 15 and bank is below 500 minerals, or threat is resolved.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground Macro vs. Air Overcommit

**When:** Early-midgame, both sides have a ground-oriented macro posture with heavy economy and technology. Opponent shows light air presence and possible pressure.

**Mistake → correction:** Overcommitting to air or neglecting defense while focusing solely on ground strength. → Strengthen ground forces while increasing economy and maintaining production. Continue technology development.

**Why:** A heavy economy and tech base supports a strong ground army. Maintaining production and tech keeps you competitive while you expand your lead.

**Read for full checks:** `N001`

### L02 — Ground Strength with Air Contingency

**When:** Midgame, both sides have heavy ground macro with heavy production and tech. Opponent shows a mix of Siege Tanks, Marines, Marauders, and possibly Battlecruisers.

**Mistake → correction:** Overcommitting to ground without preparing for a potential air transition to Battlecruisers. → Maintain ground strength, increase economy, and continue technology. Consider adding air units or upgrades to counter potential Battlecruisers.

**Why:** The opponent may be transitioning to Battlecruisers, so preparing some air defense or Viking support is wise. Maintaining a strong economy allows flexibility.

**Read for full checks:** `N003`

### L03 — Defending Drops While Strengthening Ground

**When:** Late-midgame, opponent shows moderate air presence with Hellions and Medivacs, indicating a possible drop play. Your own posture is ground with moderate air.

**Mistake → correction:** Neglecting ground defense while focusing on air or expansion, leaving you vulnerable to the opponent's ground army. → Increase air presence and continue strengthening ground forces. Maintain economy and expand further. Continue technology and upgrades.

**Why:** The opponent's Medivacs and Hellions suggest drop harassment. Adding air units like Vikings or Medivacs of your own helps defend and enables counter-drops.

**Read for full checks:** `N004`

## Decision Nodes

### [DEFAULT] N001 — Early Ground Macro with Heavy Tech

**Trigger situation:**  
Early-midgame, both sides have a ground-oriented macro posture with heavy economy and technology. Opponent shows light air presence and possible pressure.

**Direction:**  
Strengthen ground forces while increasing economy and maintaining production. Continue technology development.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Developing Ground with Siege Tanks

**Trigger situation:**  
Early-midgame, opponent shows Siege Tanks and Marauders, indicating a heavy ground tech path. Your own posture is ground-oriented with heavy production and tech.

**Direction:**  
Continue strengthening ground forces, increase economy, and maintain production and technology. Consider adding Siege Tanks to your composition.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground with Mixed Tech

**Trigger situation:**  
Midgame, both sides have heavy ground macro with heavy production and tech. Opponent shows a mix of Siege Tanks, Marines, Marauders, and possibly Battlecruisers.

**Direction:**  
Maintain ground strength, increase economy, and continue technology. Consider adding air units or upgrades to counter potential Battlecruisers.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Ground with Air Transition

**Trigger situation:**  
Late-midgame, opponent shows moderate air presence with Hellions and Medivacs, indicating a possible drop play. Your own posture is ground with moderate air.

**Direction:**  
Increase air presence and continue strengthening ground forces. Maintain economy and expand further. Continue technology and upgrades.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early-Midgame Ground with Reapers

**Trigger situation:**  
Early-midgame, opponent shows Siege Tanks, Marines, and Reapers, indicating a ground tech path with harassment potential. Your own posture is ground with heavy production.

**Direction:**  
Strengthen ground forces, increase economy, and maintain production and technology. Consider adding Reapers for map control or scouting.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Midgame Ground with Defense Focus

**Trigger situation:**  
Midgame, opponent shows a mix of Marines, Reapers, Medivacs, and Banshees, indicating possible air harassment. Your own posture is ground with heavy defense.

**Direction:**  
Increase defense and economy, continue production and technology. Strengthen ground forces and consider adding anti-air units.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Midgame Air Transition

**Trigger situation:**  
Midgame, opponent shows a ground posture with Marines and Marauders. Your own posture has moderate air presence, indicating a possible air transition.

**Direction:**  
Increase air presence and strengthen air forces. Continue economy and expansion. Continue technology and upgrades.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Late-Midgame Air Transition with Thor Threat

**Trigger situation:**  
Late-midgame, opponent shows Siege Tanks, Marines, and Thors, indicating a heavy ground anti-air composition. Your own posture has moderate air presence.

**Direction:**  
Increase air presence and strengthen air forces. Continue economy and expansion. Continue technology and upgrades.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Early-Midgame Air Transition with Thor

**Trigger situation:**  
Early-midgame, opponent shows Marines, Thors, and Medivacs, indicating a ground-heavy composition with some air. Your own posture has moderate air presence.

**Direction:**  
Increase air presence and strengthen air forces. Continue economy and expansion. Continue technology and upgrades.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Early Game Ground Development

**Trigger situation:**  
Early game, opponent shows a ground posture with Marines. Your own posture is unknown but with heavy tech investment.

**Direction:**  
Strengthen ground forces, increase economy, and increase production. Continue technology development.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Midgame Ground with Battlecruiser Potential

**Trigger situation:**  
Midgame, opponent shows Siege Tanks, Marines, Marauders, and possibly Battlecruisers. Your own posture is ground with heavy production.

**Direction:**  
Maintain current army path, continue economy and production. Consider adding anti-air or Battlecruiser support.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Early Game Ground with Marauder

**Trigger situation:**  
Early game, opponent shows a Marauder, indicating a ground tech path. Your own posture is ground with heavy tech.

**Direction:**  
Strengthen ground forces, increase economy, and maintain production. Continue technology development.

**Read for details:** `N012`

---
