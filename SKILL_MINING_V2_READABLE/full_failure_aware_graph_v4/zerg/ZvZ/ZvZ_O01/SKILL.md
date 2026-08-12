# ZvZ_O01 Economy / Expansion / Ground

## Skill Identity

- Skill ID: ZvZ_O01
- Matchup: Zerg vs Zerg
- Opening Family: economy / expansion / ground opening
- Method: Failure-Aware Full V4

## Opening Strategy

This opening focuses on a heavy economy and expansion posture with a ground-oriented army. Production is moderate early, with technology investment light or uncertain. The goal is to develop a strong macro foundation while maintaining flexibility to adapt to opponent actions.

Develop a economy / expansion / ground posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

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

### R01 — Maintain Ground Production Tempo

**When:** Early-midgame with heavy economy and moderate production; Zergling and Queen cues visible; bank above 1500 minerals or 300 gas; army supply below 20.

**Correction:** Queue Zerglings and Queens from existing hatcheries, prioritizing larvae for army over drones if army supply is below 15. If production is idle and bank is high, add a hatchery at a natural expansion only if army supply is at least 15 and no severe disadvantage is predicted. Keep tech light; do not start a Spire or Infestation Pit unless enemy air is confirmed.

**Recheck:** At next decision cycle, verify that army supply increased by at least 5 and bank decreased by at least 500 minerals or 100 gas.

### R02 — Counter Enemy Air or Ground Composition

**When:** Enemy Intelligence shows Mutalisks or other air units; or enemy ground composition is Roach-heavy with light air; midgame with moderate to heavy production.

**Correction:** If enemy air is present, build Spore Crawlers at each base and queue Hydralisks or Corruptors once a Hydralisk Den or Spire is completed. If enemy is ground-heavy with Roaches, prioritize Roaches and Zerglings, and add a Roach Warren if not already present. Maintain economy and production; do not over-expand while army supply is below 15.

**Recheck:** At next decision cycle, confirm that anti-air or anti-ground units are being produced and that each base has at least one Spore Crawler if enemy air was detected.

### R03 — Recover from Low Army and High Bank

**When:** Army supply below 10, bank above 2000 minerals or 400 gas, or predicted advantage is OverwhelmingDisadvantage; production is idle or insufficient.

**Correction:** Immediately queue combat units (Zerglings, Roaches, or Hydralisks) from all hatcheries, prioritizing army over workers. If supply is blocked, build a single Overlord or spawning pool as needed. Do not expand or tech until army supply is at least 15 and bank is below 1000 minerals. If enemy threat is imminent, use all larvae for army and consider spine crawlers at natural.

**Recheck:** At next decision cycle, verify that army supply is at least 15 and bank is below 1000 minerals; if not, continue the recovery queue.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid Premature Tech

**When:** Early-midgame, both sides ground, heavy economy, moderate production, light tech. Zergling and Queen cues visible.

**Mistake → correction:** Investing in unnecessary technology that delays army production. → Continue strengthening ground, maintain economy, production, tech, and expansion.

**Why:** Maintaining a balanced ground macro approach keeps you competitive while allowing adaptation to opponent's tech or army choices.

**Read for full checks:** `N002`

### L02 — Don't Ignore Air Threat

**When:** Midgame, opponent ground with heavy air presence, heavy economy, heavy production, moderate tech. Zergling, Mutalisk, Queen, Overseer cues.

**Mistake → correction:** Staying purely ground when opponent has a significant air force. → Increase defense, economy, continue production and tech, strengthen ground.

**Why:** With opponent having air presence, you need to bolster defenses and possibly tech to anti-air while maintaining economy.

**Read for full checks:** `N008`

### L03 — Don't Neglect Ground Defense

**When:** Midgame, opponent ground with light air, heavy economy, heavy production, heavy tech. Zergling, Roach, Queen cues.

**Mistake → correction:** Neglecting ground defense while teching to air. → Increase air, economy, continue tech, maintain production, strengthen air.

**Why:** If you have air presence and opponent is ground-heavy, transitioning to air can give you a strategic advantage.

**Read for full checks:** `N009`

## Decision Nodes

### [POSITIVE] N001 — Early Ground Macro with Economy Focus

**Trigger situation:**  
Early game, both sides ground-oriented, heavy economy, moderate production, light tech. Opponent shows Queen cues, pressure possible.

**Direction:**  
Strengthen ground army, increase economy, continue tech, maintain defense and expansion.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Mid Ground Development

**Trigger situation:**  
Early-midgame, both sides ground, heavy economy, moderate production, light tech. Zergling and Queen cues visible.

**Direction:**  
Continue strengthening ground, maintain economy, production, tech, and expansion.

**Read for details:** `N002`

---

### [POSITIVE] N003 — Aggressive Economy and Expansion

**Trigger situation:**  
Early game, ground posture, heavy economy, moderate production, light tech. Opponent Queen cues, pressure possible.

**Direction:**  
Increase economy, expansion, and production, continue tech, strengthen ground.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground Macro

**Trigger situation:**  
Midgame, both sides ground, heavy economy, heavy production, moderate tech. Zergling and Queen cues.

**Direction:**  
Maintain ground strength, economy, production, tech, and expansion.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Defensive Early Game

**Trigger situation:**  
Early game, ground posture, heavy economy, moderate production, light tech. Opponent Queen cues, pressure possible.

**Direction:**  
Increase defense, economy, continue production and tech, strengthen ground.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Expansion and Production Push

**Trigger situation:**  
Early-midgame, ground posture, heavy economy, moderate production, light tech. Zergling and Queen cues.

**Direction:**  
Increase economy, expansion, production, continue tech, strengthen ground.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Late-Midgame Ground Defense

**Trigger situation:**  
Late-midgame, opponent ground with heavy air presence, heavy economy, heavy production, heavy tech. Zergling, Mutalisk, Roach, Queen cues.

**Direction:**  
Increase defense, economy, continue production and tech, strengthen ground.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Ground with Air Threat

**Trigger situation:**  
Midgame, opponent ground with heavy air presence, heavy economy, heavy production, moderate tech. Zergling, Mutalisk, Queen, Overseer cues.

**Direction:**  
Increase defense, economy, continue production and tech, strengthen ground.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Air Transition

**Trigger situation:**  
Midgame, opponent ground with light air, heavy economy, heavy production, heavy tech. Zergling, Roach, Queen cues.

**Direction:**  
Increase air, economy, continue tech, maintain production, strengthen air.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Late-Midgame Air Transition

**Trigger situation:**  
Late-midgame, opponent ground with light air, heavy economy, heavy production, moderate tech. Zergling, Queen cues.

**Direction:**  
Increase air, economy, continue tech, maintain production, strengthen air.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early Game Stabilization

**Trigger situation:**  
Early game, ground posture, heavy economy, moderate production, light tech. Zergling and Queen cues.

**Direction:**  
Increase economy, production, continue tech, strengthen ground, maintain defense.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Early-Mid Defensive Stance

**Trigger situation:**  
Early-midgame, ground posture, heavy economy, moderate production, light tech. Zergling and Queen cues.

**Direction:**  
Increase defense, economy, continue production and tech, strengthen ground.

**Read for details:** `N012`

---
