# ZvZ_O02 Economy / Ground / Expansion

## Skill Identity

- Skill ID: ZvZ_O02
- Matchup: Zerg vs Zerg
- Opening Family: economy / ground / expansion opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg versus Zerg opening that emphasizes economy and expansion while keeping ground forces as the primary defensive and offensive arm. The early game is characterized by uncertainty about the opponent's intentions, so the strategy is to develop a solid economic base and a flexible ground army, ready to adapt based on scouting information.

Develop a robust economy and a ground-oriented army while maintaining flexibility to respond to opponent actions. Prioritize expansion and worker production to secure a long-term advantage, but keep enough defensive units to deter early aggression.

This is a strategic template, not a fixed build order. Adapt your actions based on live scouting and opponent behavior.

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

### R01 — Maintain production tempo while preserving economy

**When:** At any time before 6 minutes, if army supply is below 10 and bank is above 800, or if production structures are fewer than 3 and bank is above 1000.

**Correction:** Queue 2-3 Zerglings or 1-2 Roaches from existing hatcheries if larvae are available; otherwise, spawn larvae. If bank remains above 1000 after queuing, add one extra hatchery (if supply is at least 15 and no severe disadvantage). Do not build tech structures until army supply is at least 10.

**Recheck:** Recheck at next decision cycle.

### R02 — Counter enemy ground composition with roaches and lings

**When:** If enemy intelligence shows a ground-based posture with Zerglings or Queens, and your army supply is below 20.

**Correction:** Prioritize producing Roaches and Zerglings from existing hatcheries. If enemy has Roaches, add a Roach Warren if not already present. If enemy has Mutalisks, add a Spore Crawler at each base and produce Hydralisks if tech is available. Maintain worker production toward saturation.

**Recheck:** Recheck at next decision cycle.

### R03 — Recover from low army and high bank

**When:** If army supply is below 15 and bank is above 1500, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all hatcheries, prioritizing combat units over workers. If production is insufficient, add hatcheries (up to 3 total) if supply is at least 15. Do not expand or tech until army supply is above 20 and bank is below 1000.

**Recheck:** Recheck at next decision cycle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid premature tech investment

**When:** Early-mid game, opponent has ground posture with Zerglings, heavy economy, and you have moderate production and light tech.

**Mistake → correction:** Investing in unnecessary technology that delays army production. → Continue strengthening your ground army and maintain economy. Consider expanding further to secure long-term advantage.

**Why:** Both sides focus on economy and ground forces; the better economy and army composition will prevail.

**Read for full checks:** `N007`

### L02 — Avoid falling behind in economy

**When:** Early game, opponent has ground posture with Queen, your economy is moderate, and you have light tech.

**Mistake → correction:** Making unnecessary units that could be drones, falling behind economically. → Maintain a balanced approach: develop economy while strengthening ground army. Focus on scouting to gain information.

**Why:** Opponent focuses on economy; you need to keep up economically while building a defensive army to deter attacks. Balanced approach adapts to opponent's actions.

**Read for full checks:** `N006`

### L03 — Avoid unnecessary aggression

**When:** Early-mid game, opponent has ground posture with Zerglings, heavy economy, and you have moderate production and light tech.

**Mistake → correction:** Engaging in unnecessary aggression that costs drones, neglecting scouting for tech switches or all-ins. → Continue strengthening ground army and maintain economy. Consider expanding further to secure long-term advantage.

**Why:** Both sides focus on economy and ground forces; the better economy and army composition will prevail.

**Read for full checks:** `N007`

## Decision Nodes

### [DEFAULT] N001 — Early Game Uncertainty

**Trigger situation:**  
At the start of the game, both players have limited information. The opponent's posture is unknown, and your own forces are still developing.

**Direction:**  
Maintain a balanced development path, focusing on economy and scouting. Avoid overcommitting to any single strategy until you have more information.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Mid Game Development

**Trigger situation:**  
As the game progresses into the early-mid game, you still have limited information about the opponent, but your own economy and production are starting to take shape.

**Direction:**  
Continue to develop your economy and production while keeping your army composition flexible. Focus on scouting to gain information about the opponent's plans.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Consolidation

**Trigger situation:**  
In the midgame, you have established a solid economic base, but the opponent's strategy is still unclear. You need to consolidate your position and prepare for potential conflicts.

**Direction:**  
Maintain your current development path while increasing your scouting efforts. Consider building a defensive army to protect your expansions and prepare for potential attacks.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late Midgame Preparation

**Trigger situation:**  
In the late midgame, you have a stable economy, but the opponent's strategy is still unknown. You need to prepare for the late game while maintaining flexibility.

**Direction:**  
Continue to develop your economy and production while increasing your army size. Focus on scouting to gain information about the opponent's plans.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Ground-Oriented Development

**Trigger situation:**  
You have scouted the opponent and detected a ground-based posture, with cues such as Queens. The opponent appears to be focusing on economy and expansion.

**Direction:**  
Strengthen your ground army and increase your defenses. Continue expanding your economy to match the opponent's growth.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Balanced Ground Development

**Trigger situation:**  
You have scouted the opponent and detected a ground-based posture, but your own economy is moderate. You need to balance army and economy development.

**Direction:**  
Maintain a balanced approach, developing your economy while also strengthening your ground army. Focus on scouting to gain information about the opponent's plans.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Midgame Ground Confrontation

**Trigger situation:**  
In the early-mid game, you have scouted the opponent and detected a ground-based posture with Zerglings. The opponent's economy and expansion are heavy, indicating a macro-oriented strategy.

**Direction:**  
Continue to strengthen your ground army and maintain your economy. Consider expanding further to secure a long-term advantage.

**Read for details:** `N007`

---
