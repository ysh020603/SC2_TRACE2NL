# ZvT_O04 Economy / Upgrade / Expansion

## Skill Identity

- Skill ID: ZvT_O04
- Matchup: Zerg vs Terran
- Opening Family: economy / upgrade / expansion opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg opening focused on heavy economy, upgrades, and expansion while maintaining a ground-oriented army. The strategy emphasizes macro development with safety checks, adapting to Terran ground compositions.

Develop a strong economy and tech base while expanding, keeping flexibility to respond to Terran pressure or transitions.

This is a strategic template, not a fixed build order. Adapt based on live observations.

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

### R01 — Maintain production tempo and convert bank into army

**When:** At any time, if bank is above 800 minerals and 400 gas, or if army supply is below 15 and production is idle or insufficient, or if supply is not blocked and there are fewer than 2 hatcheries with active larvae or fewer than 2 completed production structures.

**Correction:** Queue units from all hatcheries and production structures, prioritizing Zerglings and Queens for ground defense. If bank remains high after queuing, add a spawning pool or baneling nest if prerequisites are met, or start an evolution chamber for upgrades. Do not expand until army supply is at least 15 and production is saturated.

**Recheck:** Next decision cycle: verify bank is below 800 minerals and 400 gas, army supply is at least 15, and all production structures have active queues.

### R02 — Counter Terran ground composition with tech and units

**When:** If enemy intelligence reveals a ground composition including Marines, Reapers, Hellions, or Siege Tanks, and own army lacks sufficient anti-ground or anti-armor units, or if own tech is insufficient to handle the composition.

**Correction:** If enemy has Marines/Reapers/Hellions, prioritize Zerglings and Banelings, and start a Baneling Nest if not already present. If enemy has Siege Tanks, add Roaches or Mutalisks for mobility, and start a Roach Warren or Spire if prerequisites are met. Continue economy and upgrades, but ensure at least one evolution chamber is upgrading melee or ranged attacks.

**Recheck:** Next decision cycle: verify that the appropriate tech structure is completed or in progress, and that unit composition includes the required counters.

### R03 — Recover from low army and high bank with defensive production

**When:** If army supply is below 15 and bank is above 1000 minerals and 500 gas, or if predicted advantage is OverwhelmingDisadvantage, or if any owned base is threatened.

**Correction:** Immediately queue defensive units from all hatcheries and production structures, prioritizing Zerglings and Queens. If supply is not blocked, add a spawning pool or evolution chamber if needed. Do not expand or tech further until army supply is at least 15 and bank is below 800 minerals. If threatened, also build spine crawlers at vulnerable bases if available.

**Recheck:** Next decision cycle: verify army supply is at least 15, bank is below 800 minerals, and no owned base is under threat.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Balance economy and safety in early game

**When:** Early game, opponent posture unknown, own ground-oriented with Queens.

**Mistake → correction:** Overcommitting to army before economy is stable. → Maintain economy and expansion, strengthen ground, continue tech, develop with safety checks.

**Why:** Establish a solid economic and tech foundation while staying safe against early pressure.

**Read for full checks:** `N001`

### L02 — Tech up to counter Terran ground threats

**When:** Early-midgame, opponent ground with Marines, Reapers, Hellions, own ground with Zerglings, Queens, moderate tech.

**Mistake → correction:** Falling behind in army strength while teching. → Continue economy, increase tech, strengthen ground.

**Why:** Tech up to handle Terran ground threats.

**Read for full checks:** `N008`

### L03 — Use Mutalisks for harassment and map control

**When:** Midgame, opponent ground with Marines, Ghosts, Hellions, Medivacs, own ground with Zerglings, Mutalisks, Queens, Overseers.

**Mistake → correction:** Overcommitting to air without ground support. → Increase air, strengthen air, continue economy, increase upgrades.

**Why:** Use Mutalisks for harassment and map control.

**Read for full checks:** `N011`

## Decision Nodes

### [DEFAULT] N001 — Early Game Development

**Trigger situation:**  
Early game, opponent posture unknown, own ground-oriented with Queens.

**Direction:**  
Maintain economy and expansion, strengthen ground, continue tech, develop with safety checks.

**Read for details:** `N001`

---

### [POSITIVE] N002 — Early-Midgame Ground Focus

**Trigger situation:**  
Early-midgame, opponent ground posture with Marines and Ghosts, own ground with Zerglings and Queens.

**Direction:**  
Strengthen ground army, maintain economy, continue tech, develop with safety checks.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early-Midgame Expansion

**Trigger situation:**  
Early-midgame, opponent ground with Marines, Reapers, Hellions, own ground with Zerglings and Queens.

**Direction:**  
Increase expansion and production, strengthen ground, continue tech.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground Macro

**Trigger situation:**  
Early-midgame to midgame, opponent ground with Marines, own ground with Zerglings and Queens.

**Direction:**  
Maintain economy and production, strengthen ground, continue tech.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Late-Midgame Ground and Air

**Trigger situation:**  
Late-midgame, opponent ground with Siege Tanks, Marines, Medivacs, own ground with Zerglings, Mutalisks, Queens.

**Direction:**  
Maintain ground strength, continue economy, increase tech, consider air.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Midgame Ground Defense

**Trigger situation:**  
Midgame, opponent ground with Siege Tanks, Marines, Medivacs, own ground with Zerglings, Queens.

**Direction:**  
Maintain ground strength, continue economy, increase tech.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early Game Ground Focus

**Trigger situation:**  
Early game, opponent ground with Marines, own ground with Zerglings and Queens.

**Direction:**  
Maintain economy, strengthen ground, continue tech.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early-Midgame Tech Transition

**Trigger situation:**  
Early-midgame, opponent ground with Marines, Reapers, Hellions, own ground with Zerglings, Queens, moderate tech.

**Direction:**  
Continue economy, increase tech, strengthen ground.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Ground and Air Mix

**Trigger situation:**  
Midgame, opponent ground with Marines, Hellions, Medivacs, own ground with Zerglings, Queens, moderate tech.

**Direction:**  
Maintain ground strength, continue economy, consider air.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Late-Midgame Heavy Ground

**Trigger situation:**  
Late-midgame, opponent ground with Siege Tanks, Marines, Thors, Ravens, own ground with Zerglings, Roaches, Queens.

**Direction:**  
Maintain ground strength, continue economy, consider tech counters.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Midgame Air Transition

**Trigger situation:**  
Midgame, opponent ground with Marines, Ghosts, Hellions, Medivacs, own ground with Zerglings, Mutalisks, Queens, Overseers.

**Direction:**  
Increase air, strengthen air, continue economy, increase upgrades.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Late-Midgame Air Focus

**Trigger situation:**  
Late-midgame, opponent ground with Siege Tanks, Marines, Marauders, Medivacs, own ground with Zerglings, Mutalisks, Queens, Overseers.

**Direction:**  
Increase air, strengthen air, continue economy, increase upgrades.

**Read for details:** `N012`

---
