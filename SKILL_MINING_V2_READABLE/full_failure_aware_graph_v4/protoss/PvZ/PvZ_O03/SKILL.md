# PvZ_O03 Technology / Economy / Expansion

## Skill Identity

- Skill ID: PvZ_O03
- Matchup: Protoss vs Zerg
- Opening Family: technology / economy / expansion opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Protoss opening that emphasizes heavy technology investment and economic expansion while keeping production moderate. The early game is flexible, with the option to transition into either a ground-oriented or air-oriented army based on scouting and opponent behavior.

Develop a technology / economy / expansion posture while preserving flexibility for live observation-driven adaptation.

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

### G05 — Protoss production interpretation

- Scale Gateways or other unit-producing tech only after power, prerequisites, and production capacity are executable.

## V4 Matchup-Specific Corrections

### R01 — Maintain tech-economy tempo with production scaling

**When:** Early to mid game, own economy and tech heavy, production moderate, army supply below 15, bank above 800,.

**Correction:** Prioritize adding production structures (Gateways, Stargates) up to 4-6 total by 6 minutes, while continuing worker production toward 30-40. Keep tech buildings (Twilight Council, Robotics Facility) progressing. If bank exceeds 1000, add production before expanding. Do not commit to a single army composition; keep ground and air options open.

**Recheck:** At next decision cycle, verify production count and worker count meet thresholds; if bank still high, add more production.

### R02 — Adapt army composition to enemy tech

**When:** Enemy intelligence shows a ground-based Zerg with light air, but own army is air-oriented with Oracles or Phoenix, or ground-oriented with Zealots and Void Rays.

**Correction:** If opponent has Corruptors or Mutalisks, maintain a mix of ground (Zealots, Stalkers) and air (Void Rays, Phoenix) to counter. If opponent is heavy on Roaches and Hydralisks, add Immortals or Colossi. Ensure detection (Observer) if Darkspawn or burrowed units are seen. Keep production balanced between Gateway and Stargate/Robotics.

**Recheck:** At next decision cycle, reassess enemy composition and adjust production queues accordingly.

### R03 — Recover from low army and high bank

**When:** Army supply below 15, bank above 1500, production idle or insufficient, or predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately convert bank into army: queue units from all available production structures, prioritize combat units over workers. If supply blocked, add a single supply provider (Pylon) if needed. Do not expand or invest in tech until army supply is above 20 and production is active. If threatened, warp in defensive units at home.

**Recheck:** At next decision cycle, verify army supply increased and bank reduced; if still low, continue unit production.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid early army commitment

**When:** Early game, own economy and tech heavy, production moderate, opponent ground-based with light air.

**Mistake → correction:** Committing to a specific army composition before scouting the opponent's tech path, or neglecting defense while focusing on economy. → Continue developing economy and technology while maintaining flexibility. Strengthen ground forces as a baseline, but keep options open for air transition.

**Why:** Early game is about establishing a strong economic and technological foundation. Committing too early to a specific army composition can be punished by scouting and adaptation.

**Read for full checks:** `N001`

### L02 — Balance air commitment with ground defense

**When:** Early-midgame, own army air-oriented with Oracles, heavy production and tech, opponent ground-based with light air.

**Mistake → correction:** Over-committing to air while neglecting ground defense, or failing to adapt if the opponent shows anti-air. → Increase air presence and strengthen air forces. Continue developing technology and economy, but ensure ground defense is not neglected.

**Why:** Oracles provide harassment and scouting, and can transition into Phoenix or Void Ray compositions. Air can be strong against ground-based Zerg, but ground defense remains essential.

**Read for full checks:** `N007`

### L03 — Maintain balanced ground and air forces

**When:** Midgame, own army ground-oriented with Zealots and Void Rays, opponent ground-based with Zerglings, Mutalisks, Corruptors, and Queens.

**Mistake → correction:** Over-committing to Void Rays if the opponent has many Corruptors, or neglecting ground defense. → Strengthen ground forces and maintain Void Rays for anti-air. Continue developing technology and economy.

**Why:** Void Rays provide anti-air and can be effective against Corruptors. A balanced army can handle mixed compositions.

**Read for full checks:** `N010`

## Decision Nodes

### [DEFAULT] N001 — Early Game Tech/Eco Development

**Trigger situation:**  
Early game, own army composition unknown, economy heavy, technology heavy, production moderate. Opponent shows ground posture with light air presence, moderate production, light tech.

**Direction:**  
Continue developing economy and technology while maintaining flexibility. Strengthen ground forces as a baseline, but keep options open for air transition.

**Read for details:** `N001`

---

### [POSITIVE] N002 — Ground Army Stabilization

**Trigger situation:**  
Early-midgame, own army is ground-oriented with Stalkers, heavy production and tech. Opponent remains ground-based with light air, moderate production.

**Direction:**  
Stabilize your ground army and continue increasing production and technology. Maintain economy and expansion.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Ground Army Development with Safety Checks

**Trigger situation:**  
Early-midgame, own army ground-oriented with Stalkers, heavy production and tech. Opponent ground-based, light air, moderate production.

**Direction:**  
Continue developing ground forces and technology while maintaining safety checks. Increase production and economy.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground Army Expansion

**Trigger situation:**  
Midgame, own army ground-oriented with Stalkers, Sentries, and Warp Prisms. Opponent ground-based with Zerglings, Roaches, and Queens, heavy production and tech.

**Direction:**  
Continue strengthening your ground army and maintain economy. Consider adding tech units like Immortals or Colossi.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game Expansion Focus

**Trigger situation:**  
Early game, own army unknown, economy heavy, expansion light_or_uncertain. Opponent ground-based with light air, moderate production.

**Direction:**  
Increase expansion and continue developing technology. Strengthen ground forces as a baseline.

**Read for details:** `N005`

---

### [POSITIVE] N006 — Midgame Tech Advantage

**Trigger situation:**  
Midgame, own army ground-oriented with Stalkers, Warp Prisms, Observers, and Immortals. Opponent ground-based with Zerglings and Queens, moderate production and tech.

**Direction:**  
Leverage your tech advantage to pressure the opponent or expand further. Continue increasing technology.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Air Transition with Oracles

**Trigger situation:**  
Early-midgame, own army air-oriented with Oracles, heavy production and tech. Opponent ground-based with light air, moderate production.

**Direction:**  
Increase air presence and strengthen air forces. Continue developing technology and economy.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Late-Midgame Ground Tech

**Trigger situation:**  
Late-midgame, own army ground-oriented with Stalkers and Dark Templar, heavy production and tech. Opponent ground-based with Zerglings, Hydralisks, Roaches, and Queens.

**Direction:**  
Continue strengthening your ground army and consider adding Colossi or High Templar. Maintain economy and expansion.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Air Army with Phoenix

**Trigger situation:**  
Midgame, own army air-oriented with Zealots, Stalkers, and Oracles. Opponent ground-based with Zerglings, Mutalisks, Corruptors, and Queens.

**Direction:**  
Increase air presence and strengthen air forces. Consider adding Phoenix to counter Mutalisks.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Midgame Ground with Void Rays

**Trigger situation:**  
Midgame, own army ground-oriented with Zealots and Void Rays. Opponent ground-based with Zerglings, Mutalisks, Corruptors, and Queens.

**Direction:**  
Strengthen ground forces and maintain Void Rays for anti-air. Continue developing technology and economy.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Late-Midgame Air Army with Phoenix

**Trigger situation:**  
Late-midgame, own army air-oriented with Zealots, Stalkers, Phoenix, and Oracles. Opponent ground-based with Zerglings, Mutalisks, Roaches, and Queens.

**Direction:**  
Continue strengthening air forces and consider adding Carriers or Void Rays. Maintain economy and expansion.

**Read for details:** `N011`

---
