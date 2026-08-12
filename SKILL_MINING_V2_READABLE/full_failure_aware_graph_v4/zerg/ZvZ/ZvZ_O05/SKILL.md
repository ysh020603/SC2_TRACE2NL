# ZvZ_O05 Economy / Ground / Upgrade

## Skill Identity

- Skill ID: ZvZ_O05
- Matchup: Zerg vs Zerg
- Opening Family: economy / ground / upgrade opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg versus Zerg opening that prioritizes a strong economy and ground-based army development, with an emphasis on upgrades and technological progression. The opening is flexible, allowing for adaptation based on scouting information.

Develop a robust economy and a versatile ground army while maintaining the option to transition into air or tech-based compositions as the game evolves.

This is a strategic template, not a fixed build order. Adapt your decisions based on live scouting and enemy intelligence.

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

### R01 — Maintain production tempo and economy focus

**When:** Early game (before 5 minutes) with moderate economy and light tech, both players ground-oriented. If workers below 30 by 4 minutes or bank above 1500 with production idle, prioritize drones and ensure hatcheries are producing.

**Correction:** If bank exceeds 1500 and production is idle, queue drones to reach 30-35 workers by 5 minutes. If workers are below 30 at 4 minutes, prioritize drone production over army units unless threat is imminent. Keep at least one hatchery on drone production and maintain 2-3 supply providers to avoid supply blocks.

**Recheck:** Recheck at next decision cycle: workers count, bank, production status, and supply availability.

### R02 — Adapt ground composition to enemy tech

**When:** Midgame (5-9 minutes) when enemy intelligence shows heavy production and moderate-to-heavy tech. If enemy has air units (Mutalisks, Corruptors) or tech to air, adjust ground army accordingly.

**Correction:** If enemy has air presence, add Spore Crawlers at bases and produce Queens for anti-air. If enemy remains ground-heavy, continue Roach production and upgrade ground weapons/armor. Ensure at least one Evolution Chamber is upgrading when bank allows.

**Recheck:** Recheck at next decision cycle: enemy composition, own army composition, and upgrade status.

### R03 — Recover from low army and high bank

**When:** Any time when army supply is below 15 and bank exceeds 2000, or predicted advantage is OverwhelmingDisadvantage. Prioritize army production over economy.

**Correction:** Immediately queue army units (Zerglings/Roaches) from all hatcheries. If bank exceeds 2000, add extra hatcheries for production if prerequisites are met. Do not expand until army supply is above 15 and production is active. If threatened, use defensive structures and static defense.

**Recheck:** Recheck at next decision cycle: army supply, bank, production status, and threat level.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid premature aggression in a macro mirror

**When:** Early-midgame, both players ground-oriented with light tech and moderate production, strong economy and expansion.

**Mistake → correction:** Launching an unnecessary attack that sacrifices drones or disrupts your economy, or neglecting scouting for tech switches or all-ins. → Continue developing your ground army and economy. Maintain current production and technology levels while keeping an eye on potential threats.

**Why:** Both players are in a similar macro state; continuing to develop economy and ground forces keeps you competitive and ready to respond.

**Read for full checks:** `N001`

### L02 — Match heavy production with robust ground forces

**When:** Midgame, enemy ground posture with heavy production and moderate tech, your army includes Roaches.

**Mistake → correction:** Over-investing in Roaches if the opponent is teching to air, or neglecting expansion and economy. → Strengthen your ground army by adding more Roaches and possibly tech upgrades. Continue to expand your economy and production.

**Why:** Enemy's heavy production suggests a large army; matching production and strengthening ground forces helps defend or counter-attack.

**Read for full checks:** `N002`

### L03 — Prioritize economy over unnecessary units in early game

**When:** Early game, both ground-oriented with moderate production and light tech, your economy moderate and expansion developing.

**Mistake → correction:** Falling behind in economy by making unnecessary units that could be drones. → Focus on expanding your economy and establishing a solid foundation. Continue producing Zerglings and Queens for defense.

**Why:** A strong economy is crucial for long-term success; building a solid foundation allows you to outproduce the enemy in the midgame.

**Read for full checks:** `N003`

## Decision Nodes

### [DEFAULT] N001 — Early-Midgame Ground Macro

**Trigger situation:**  
At around 6 minutes, both players are in the early-midgame with a ground-oriented posture. Enemy intelligence suggests a ground army with Zerglings and Queens, moderate production, and light technology. Your own forces are similarly ground-based with Zerglings and Queens, and you have a strong economy and expansion.

**Direction:**  
Continue developing your ground army and economy. Maintain your current production and technology levels, while keeping an eye on potential threats.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Army Strengthening

**Trigger situation:**  
At around 7 minutes, the game has progressed to the midgame. Enemy intelligence shows a ground posture with Zerglings and Queens, but their production has increased to heavy and technology is moderate. Your own army includes Roaches, indicating a transition to a more robust ground composition.

**Direction:**  
Strengthen your ground army by adding more Roaches and possibly tech upgrades. Continue to expand your economy and production.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Game Economy Focus

**Trigger situation:**  
At around 3 minutes, the game is in the early game. Enemy intelligence shows a ground posture with Zerglings and Queens, moderate production, and light technology. Your own economy is moderate, and you are still developing your expansion.

**Direction:**  
Focus on expanding your economy and establishing a solid foundation. Continue producing Zerglings and Queens for defense.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Ground Army Consolidation

**Trigger situation:**  
At around 10 minutes, the game is in the late-midgame. Enemy intelligence shows a ground posture with Zerglings, Roaches, and Queens, heavy production, and moderate technology. Your own army is similar, with a heavy economy and production.

**Direction:**  
Consolidate your ground army and continue to upgrade. Maintain your economy and production to support a large army.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Late-Midgame Air Transition

**Trigger situation:**  
At around 10 minutes, the game is in the late-midgame. Enemy intelligence shows a ground posture with Zerglings, Roaches, and Queens, heavy production, and heavy technology. Your own army has transitioned to include Mutalisks, indicating an air component.

**Direction:**  
Increase your air presence and continue to strengthen your air army. Maintain your economy and production to support the transition.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Midgame Air Transition

**Trigger situation:**  
At around 9 minutes, the game is in the midgame. Enemy intelligence shows a ground posture with Zerglings, Roaches, and Queens, heavy production, and heavy technology. Your own army has transitioned to include Mutalisks, indicating an air component.

**Direction:**  
Increase your air presence and continue to strengthen your air army. Maintain your economy and production to support the transition.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Late-Midgame Defensive Stance

**Trigger situation:**  
At around 10 minutes, the game is in the late-midgame. Enemy intelligence shows an air presence with Zerglings, Mutalisks, Corruptors, and Queens, heavy production, and heavy technology. Your own army is ground-based with Zerglings, Roaches, Queens, and Overseers.

**Direction:**  
Increase your defensive capabilities, particularly against air. Continue to develop your economy and production, but prioritize defense.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early-Midgame Defensive Development

**Trigger situation:**  
At around 4 minutes, the game is in the early-midgame. Enemy intelligence shows a ground posture with Zerglings and Queens, moderate production, and light technology. Your own economy is heavy, but your defense is light or uncertain.

**Direction:**  
Increase your defensive capabilities while continuing to develop your economy. Build defensive structures and maintain a standing army.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Defensive Response to Air

**Trigger situation:**  
At around 9 minutes, the game is in the midgame. Enemy intelligence shows an air presence with Zerglings, Mutalisks, Corruptors, and Queens, heavy production, and heavy technology. Your own army is ground-based with Zerglings, Roaches, and Queens.

**Direction:**  
Increase your defensive capabilities, particularly against air. Continue to develop your economy and production, but prioritize defense.

**Read for details:** `N009`

---
