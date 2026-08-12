# ZvZ_O03 Economy / Technology / Expansion

## Skill Identity

- Skill ID: ZvZ_O03
- Matchup: Zerg vs Zerg
- Opening Family: economy / technology / expansion opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg versus Zerg opening that prioritizes a heavy economy, technology, and expansion posture while maintaining a ground-oriented army. The approach is flexible, with a focus on developing infrastructure and tech before committing to aggressive actions.

Develop a strong economy and technology base while expanding, keeping ground army strength sufficient to deter or respond to pressure, and preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order. Adapt based on live scouting and enemy intelligence.

## Strategic Characteristics

- Economy: heavy
- Production: moderate
- Technology: moderate
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

### R01 — Production Tempo with Economy Focus

**When:** At any time before 360 seconds, if bank is above 2000 minerals and army supply is below 8, or if active production structures are fewer than 2 and bank is above 1500.

**Correction:** Prioritize converting bank into production and army: queue units from existing hatcheries, add a spawning pool if missing, and start a roach warren if tech is available. Maintain worker production to reach saturation, but do not let worker queues exceed 2 per hatchery. Avoid expanding until army supply is at least 15 and production is active.

**Recheck:** Recheck at next decision cycle: ensure bank is below 1500, army supply is at least 8, and production structures are active.

### R02 — Enemy Composition Response

**When:** When enemy intelligence shows Zergling and Queen cues, and your army lacks sufficient anti-light units or is below 10 supply.

**Correction:** Add a roach warren and produce roaches to counter light ground units. Maintain at least 2 queens for defense and creep spread. If enemy shows Roach cues, transition to roach production and consider a baneling nest for light units. Keep army supply above 15 to deter aggression.

**Recheck:** Recheck at next decision cycle: confirm roach warren is active, army supply is above 15, and production is not idle.

### R03 — Recovery from Low Army and High Bank

**When:** When army supply is below 15, bank is above 3000 minerals, or predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately convert bank into army: queue zerglings and roaches from all hatcheries, add spawning pools if needed, and ensure at least 3 hatcheries are producing. Do not expand or invest in technology until army supply is above 20. If threatened, prioritize defensive units and static defense.

**Recheck:** Recheck at next decision cycle: army supply should be above 20, bank below 2000, and production active.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Early Economy vs. Defense

**When:** Early game, around 180 seconds, with both sides expanding and minimal army (Queen only), opponent shows Zergling and Queen.

**Mistake → correction:** Over-committing to economy and tech while neglecting defense, assuming the opponent is passive. → Focus on economy and tech development while preparing to defend. Maintain production and expansion, but be ready to build defensive units if pressure comes.

**Why:** Early game is about establishing a strong economy and tech lead. Investing now will pay off, but you must be prepared to defend against early Zergling pressure.

**Read for full checks:** `N003`

### L02 — Balanced Macro in Early-Midgame

**When:** Early-midgame, around 300 seconds, with both sides in a ground-oriented macro posture, heavy economy and expansion, moderate production/tech, enemy shows Zergling and Queen.

**Mistake → correction:** Neglecting army production entirely, leaving yourself vulnerable to a sudden attack. → Continue developing your economy and tech while strengthening your ground army. Maintain current production and expansion pace, but keep safety checks in mind.

**Why:** The situation is symmetric and stable; investing in economy and tech now will pay off later. Maintaining a ground army deters potential aggression without overcommitting.

**Read for full checks:** `N001`

### L03 — Scaling with Upgrades in Late-Midgame

**When:** Late-midgame, around 600-720 seconds, with both sides having heavy economy, defense, production, and tech. Your army is ground-based with Zergling and Queen, opponent shows Zergling, Roach, Queen.

**Mistake → correction:** Over-investing in technology without sufficient army, and neglecting scouting for tech switches. → Increase your economy and tech further, and consider upgrades. Maintain your ground army and production, but be ready to adapt if the opponent tech switches.

**Why:** With a heavy economy and tech, you can afford to invest in upgrades and a larger army. Maintaining a strong ground presence keeps you safe while you scale.

**Read for full checks:** `N004`

## Decision Nodes

### [DEFAULT] N001 — Early-Midgame Ground Macro Development

**Trigger situation:**  
At around 300 seconds, both players are in early-midgame with a ground-oriented macro posture, heavy economy and expansion, and moderate production/tech. Enemy intelligence shows Zergling and Queen cues, with possible pressure.

**Direction:**  
Continue developing your economy and tech while strengthening your ground army. Maintain current production and expansion pace, but keep safety checks in mind.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Army Strengthening

**Trigger situation:**  
At around 420-480 seconds, the game enters midgame. Both sides have moderate defense, heavy economy, and moderate production/tech. Your army now includes Roach cues alongside Zergling and Queen.

**Direction:**  
Continue strengthening your ground army, adding Roaches for durability. Maintain economy and tech development, and keep defense at a moderate level.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Game Economy and Tech Focus

**Trigger situation:**  
At around 180 seconds, the game is in early game. Both sides have heavy economy and expansion, but defense is light or uncertain. Your army is minimal (Queen only), while the opponent shows Zergling and Queen.

**Direction:**  
Focus on economy and tech development while preparing to defend. Maintain production and expansion, but be ready to build defensive units if pressure comes.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Heavy Macro and Tech

**Trigger situation:**  
At around 600-720 seconds, the game reaches late-midgame. Both sides have heavy economy, defense, production, and tech. Your army is ground-based with Zergling and Queen, while the opponent shows Zergling, Roach, Queen.

**Direction:**  
Increase your economy and tech further, and consider upgrades. Maintain your ground army and production, but be ready to adapt if the opponent tech switches.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Stabilize and Develop

**Trigger situation:**  
At around 540 seconds, the game is midgame. You have heavy defense, economy, production, and tech, while the opponent has moderate defense, heavy economy, and heavy production with Roach and Queen cues.

**Direction:**  
Stabilize your position by increasing defense and economy, while continuing production and tech. Maintain your ground army and be ready to respond to pressure.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early Game Defensive Development

**Trigger situation:**  
At around 180 seconds, the game is early game. You have heavy defense and economy, while the opponent has light defense and heavy economy, with Zergling and Queen cues.

**Direction:**  
Continue developing your economy and tech while maintaining a strong defense. Increase production and expansion as you feel safe.

**Read for details:** `N006`

---
