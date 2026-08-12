# ZvT_O01 Economy / Expansion / Ground

## Skill Identity

- Skill ID: ZvT_O01
- Matchup: Zerg vs Terran
- Opening Family: economy / expansion / ground opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg opening focused on heavy economy and expansion while maintaining a ground-oriented army. The opponent is Terran, and early intelligence suggests a ground posture with possible early pressure. The strategy emphasizes macro development with safety checks.

Develop a strong economy and expand while building a ground-based army, maintaining flexibility to adapt to opponent's tech or air transitions.

This is a strategic template, not a fixed build order. Adapt based on live scouting and opponent actions.

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

### R01 — Maintain Zergling production tempo while expanding

**When:** Early game (before 6:00) with Zergling/Queen army, ground-oriented opening, and at least one expansion completed or under construction.

**Correction:** If army supply is below 15 and bank is above 600, queue Zerglings from all Hatcheries with available larvae, prioritizing army over additional workers. If no larvae, inject with Queens. If supply blocked, add one Overlord (only if no supply provider is already queued or completed). Continue expanding only if army supply is at least 15 and production is active.

**Recheck:** At next decision cycle, verify army supply is at least 15 and bank is below 600, or production is actively queued.

### R02 — Counter Terran ground composition with tech and units

**When:** Enemy intelligence shows a ground posture with Marines, Reapers, Hellions, or Siege Tanks, and own army is primarily Zergling/Queen.

**Correction:** If enemy has Siege Tanks or Hellions, prioritize teching to Lair and spawning a Roach Warren, then queue Roaches. If enemy has Marines/Reapers, ensure Baneling Nest is started and morph Banelings from Zerglings. Maintain at least 2 bases and keep worker count near saturation (about 3 per mineral line). If bank exceeds 1000, add production structures (e.g., additional Hatcheries) before expanding further.

**Recheck:** At next decision cycle, confirm that required tech structures are completed or under construction, and army composition includes appropriate counters.

### R03 — Recover from low army and high bank

**When:** Army supply is below 15, bank is above 1000, or predicted advantage is OverwhelmingDisadvantage, and production is idle or insufficient.

**Correction:** Immediately convert bank into army: queue Zerglings and/or Roaches from all Hatcheries, using all available larvae. If larvae are insufficient, inject with Queens. If supply is blocked, add one Overlord (only if no supply provider is pending). Do not expand or tech until army supply is at least 15 and production is active. If enemy threat is imminent, prioritize defensive units (e.g., Spine Crawlers) only if army is still low after production.

**Recheck:** At next decision cycle, verify army supply is at least 15 and bank is below 1000, or production is actively queued.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Balanced Macro with Ground Focus

**When:** Early game, opponent ground posture (Marine/Reaper), own Zergling/Queen, moderate production and light tech.

**Mistake → correction:** Being too passive and letting the Terran dictate the pace, neglecting army production while expanding. → Strengthen ground army, increase economy, maintain expansions and production, continue tech.

**Why:** Maintaining a balanced macro approach supports a strong midgame.

**Read for full checks:** `N002`

### L02 — Late Midgame Preparation

**When:** Late midgame, opponent ground posture (SiegeTank/Marine/Reaper/Hellion), own Zergling/Queen, heavy production and tech.

**Mistake → correction:** Being passive and letting the Terran dictate the pace, neglecting upgrades. → Strengthen ground army, increase economy, continue expansions and production, increase tech.

**Why:** In late midgame, you need to prepare for large engagements; maintaining economy while teching is crucial.

**Read for full checks:** `N005`

### L03 — Transition to Midgame

**When:** Early midgame, opponent ground posture (Marine/Reaper/Hellion), own Zergling/Queen, moderate tech.

**Mistake → correction:** Over-investing in tech at the expense of army size, neglecting scouting to anticipate the attack. → Strengthen ground, increase economy, continue expansions and production, increase tech.

**Why:** As you transition to midgame, you need to start teching to counter opponent's composition; maintaining economy is key.

**Read for full checks:** `N007`

## Decision Nodes

### [POSITIVE] N001 — Early Ground Macro with Expansion

**Trigger situation:**  
Early game, both sides have heavy economy and expansion. Opponent shows ground posture with possible Marine/Reaper cues. Own army is Zergling/Queen.

**Direction:**  
Strengthen ground army, increase economy and expansions, continue technology, maintain defense.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Standard Ground Macro

**Trigger situation:**  
Early game, similar to N001 but with slightly different expansion timing. Opponent ground posture, own Zergling/Queen.

**Direction:**  
Strengthen ground, increase economy, maintain expansions and production, continue tech.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Push Preparation

**Trigger situation:**  
Early-midgame, opponent ground posture with heavy production, own army has Queens. Economy and expansions heavy.

**Direction:**  
Strengthen ground army, increase economy and expansions, continue tech, maintain defense.

**Read for details:** `N003`

---

### [POSITIVE] N004 — Early Macro with Unknown Opponent

**Trigger situation:**  
Early game, opponent posture unknown (no reliable combat-unit cue), but economy heavy. Own Zergling/Queen.

**Direction:**  
Strengthen ground, increase economy and expansions, continue tech, maintain defense.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Late Midgame Ground vs Ground

**Trigger situation:**  
Late midgame, opponent ground posture with SiegeTank/Marine/Reaper/Hellion, own Zergling/Queen. Both heavy economy and tech.

**Direction:**  
Strengthen ground army, increase economy, continue expansions and production, increase tech.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Midgame Ground vs Ground with Hydralisks

**Trigger situation:**  
Midgame, opponent ground posture with SiegeTank/Marine/Reaper/Marauder, own Zergling/Hydralisk/Queen/Overseer.

**Direction:**  
Strengthen ground army, increase economy, continue expansions and production, increase tech.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early Midgame Tech Transition

**Trigger situation:**  
Early midgame, opponent ground posture with Marine/Reaper/Hellion, own Zergling/Queen. Own tech moderate.

**Direction:**  
Strengthen ground, increase economy, continue expansions and production, increase tech.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early Midgame Expansion Focus

**Trigger situation:**  
Early midgame, opponent ground posture with Marine/Reaper, own Zergling/Queen. Own tech light.

**Direction:**  
Strengthen ground, increase economy and expansions, increase production, continue tech.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Late Midgame Ground Defense

**Trigger situation:**  
Late midgame, opponent ground posture with Marine, own Zergling/Queen. Both heavy economy and tech.

**Direction:**  
Strengthen ground, increase economy, maintain expansions and production, continue tech.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Midgame Ground vs Ground with Medivac

**Trigger situation:**  
Midgame, opponent ground posture with SiegeTank/Marine/Reaper/Medivac, own Zergling/Queen. Own tech moderate.

**Direction:**  
Strengthen ground, increase economy, maintain expansions and production, continue tech.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Late Midgame Air Transition

**Trigger situation:**  
Late midgame, opponent ground posture with Marine, own Zergling/Mutalisk/Queen. Own air presence heavy.

**Direction:**  
Increase air presence, strengthen air army, continue economy and expansions, increase upgrades.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Midgame Air Transition

**Trigger situation:**  
Midgame, opponent ground posture with Marine/Reaper, own Hydralisk/Mutalisk/Queen/Overseer. Own air moderate.

**Direction:**  
Increase air presence, strengthen air army, continue economy and expansions, increase upgrades.

**Read for details:** `N012`

---
