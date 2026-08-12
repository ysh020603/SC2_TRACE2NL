# ZvT_O02 Economy / Expansion / Ground

## Skill Identity

- Skill ID: ZvT_O02
- Matchup: Zerg vs Terran
- Opening Family: economy / expansion / ground opening
- Method: Failure-Aware Full V4

## Opening Strategy

This opening focuses on developing a strong economy and expanding while maintaining a ground-oriented army. Early information about the opponent is limited, so the plan emphasizes flexibility and safety checks.

Develop a economy / expansion / ground posture while preserving flexibility for live observation-driven adaptation.

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

### G05 — Zerg production interpretation

- Treat Hatchery/Lair/Hive count, larvae, Overlords, and worker/army larva competition as the production-capacity check.

## V4 Matchup-Specific Corrections

### R01 — Maintain production tempo while preserving economy/expansion opening

**When:** At any time before 6 minutes, if army supply is below 15 and bank is above 1500, or if active production structures are fewer than 2 and bank is above 1000.

**Correction:** Queue 2-3 Zerglings or Roaches from each available Hatchery, prioritizing units that counter the enemy's known composition. If a Spawning Pool is missing, build it first. If bank remains above 2000 after queuing, add a second Hatchery or an Evolution Chamber if tech is needed. Do not expand unless army supply is at least 15 and production is active.

**Recheck:** Recheck at next decision cycle: confirm army supply increased and bank decreased; if not, repeat queue.

### R02 — Respond to Terran ground composition with tech and counters

**When:** If enemy intelligence shows heavy Marine production (e.g., multiple Barracks with tech labs) or Siege Tanks, and your army supply is below 30.

**Correction:** Queue Roaches or Banelings if a Roach Warren or Baneling Nest is available; otherwise, build the required structure first. If enemy has Siege Tanks, prioritize speed and flanking units like Banelings or Mutalisks if tech is available. Continue expanding only if army supply is above 15 and production is not idle.

**Recheck:** Recheck at next decision cycle: verify army composition counters enemy units and production is active.

### R03 — Recover from low army and high bank by converting resources into defense

**When:** If army supply is below 10 and bank is above 2000, or if predicted advantage is OverwhelmingDisadvantage and bank is above 1500.

**Correction:** Immediately queue 4-6 Zerglings or Roaches from all Hatcheries, prioritizing units that counter the enemy's known composition. If a Spawning Pool is missing, build it first. If bank remains above 3000 after queuing, add a Spine Crawler at each base. Do not expand or tech until army supply is at least 15 and bank is below 1000.

**Recheck:** Recheck at next decision cycle: confirm army supply increased and bank decreased; if not, repeat queue and consider additional defensive structures.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid head-on engagement with Siege Tanks

**When:** Early-midgame, opponent shows heavy ground production (e.g., Marines) and you have moderate ground forces.

**Mistake → correction:** Committing to a head-on fight against Siege Tanks without proper tech or positioning, or over-expanding without sufficient army to defend. → Strengthen your ground army, increase economy and expansion, and continue technology development.

**Why:** The opponent is investing heavily in ground forces, so matching their strength while growing your economy is prudent.

**Read for full checks:** `N007`

### L02 — Balance tech and army production

**When:** Midgame, opponent has heavy ground production (e.g., Marines) and you have a strong economy but moderate production.

**Mistake → correction:** Neglecting army production while teching, or over-expanding if an attack is imminent. → Strengthen your ground army, increase economy and expansion, and continue technology development.

**Why:** The opponent is investing heavily in ground forces, so you need a strong army to defend while maintaining your economy.

**Read for full checks:** `N008`

### L03 — Develop economy before committing

**When:** Early game, opponent's posture is unknown and your own economy is still developing.

**Mistake → correction:** Overcommitting to army before your economy is stable. → Maintain current development path with safety checks. Focus on economy and expansion while keeping options open.

**Why:** With limited information, it is efficient to build a solid economic foundation before committing to a specific strategy.

**Read for full checks:** `N001`

## Decision Nodes

### [DEFAULT] N001 — Early Game Development

**Trigger situation:**  
At the start of the game, both sides have limited information. The opponent's posture is unknown, and your own economy and production are still developing.

**Direction:**  
Maintain current development path with safety checks. Focus on economy and expansion while keeping options open.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Midgame Development

**Trigger situation:**  
As the game progresses into the early-midgame, the opponent's posture remains unknown, but your own economy and production are still light or uncertain.

**Direction:**  
Maintain current development path with safety checks. Continue focusing on economy and expansion.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Development

**Trigger situation:**  
In the midgame, the opponent's posture is still unknown, and your own economy and production remain light or uncertain.

**Direction:**  
Maintain current development path with safety checks. Continue focusing on economy and expansion.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Development

**Trigger situation:**  
In the late-midgame, the opponent's posture is still unknown, and your own economy and production remain light or uncertain.

**Direction:**  
Maintain current development path with safety checks. Continue focusing on economy and expansion.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early-Midgame Ground Response

**Trigger situation:**  
In the early-midgame, the opponent reveals a ground posture with heavy production and economy. Your own posture is still unknown.

**Direction:**  
Maintain current development path with safety checks. Consider strengthening your ground army to respond to the opponent's ground posture.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Midgame Ground Response

**Trigger situation:**  
In the midgame, the opponent reveals a ground posture with heavy production and economy. Your own posture is still unknown.

**Direction:**  
Maintain current development path with safety checks. Consider strengthening your ground army to respond to the opponent's ground posture.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early-Midgame Ground Macro

**Trigger situation:**  
In the early-midgame, the opponent reveals a ground posture with heavy production and economy. Your own posture is ground-oriented with moderate production.

**Direction:**  
Strengthen your ground army, increase economy and expansion, and continue technology development.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Ground Macro

**Trigger situation:**  
In the midgame, the opponent reveals a ground posture with heavy production and economy. Your own posture is ground-oriented with heavy economy and expansion.

**Direction:**  
Strengthen your ground army, increase economy and expansion, and continue technology development.

**Read for details:** `N008`

---
