# TvZ_O06 Technology / Economy / Expansion

## Skill Identity

- Skill ID: TvZ_O06
- Matchup: Terran vs Zerg
- Opening Family: technology / economy / expansion opening
- Method: Branch-Faithful Full V7

## Opening Strategy

A Terran opening that prioritizes heavy technology investment and economic expansion while maintaining a ground-oriented army. The early game focuses on building a strong infrastructure and tech base, with production ramping up through the midgame. The approach is flexible, allowing adaptation based on scouting information.

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

### G05 — Terran production interpretation

- Scale Barracks/Factory/Starport capacity before ordering add-ons or units that lack a completed parent structure.

## V4 Matchup-Specific Corrections

### R01 — Maintain production tempo and tech progression

**When:** Time between 240 and 360 seconds, own army supply below 15, bank above 1000, or production structures fewer than 3.

**Correction:** Prioritize spending bank on production structures (Barracks, Factory, Starport) and tech upgrades (e.g., Stim, Combat Shields, +1 weapons) while keeping workers mining. Queue units from existing production if idle. Do not expand until army supply is at least 15 and production is active.

**Recheck:** At next decision cycle, verify army supply increased, bank reduced, and production structures are actively producing.

### R02 — Counter observed Zerg composition

**When:** Enemy intelligence reveals a composition of Roaches, Mutalisks, or heavy ground with light air.

**Correction:** Adjust unit mix to counter: add Siege Tanks and Marauders against Roaches; add Thors or Marines with upgrades against Mutalisks. Ensure at least one tech lab on a Factory or Starport for required tech. Maintain production of counter units while continuing economy.

**Recheck:** At next decision cycle, confirm counter units are being produced and tech structures are available.

### R03 — Recover from low army and high bank

**When:** Army supply below 15, bank above 2000, or predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately convert bank into army: queue units from all available production structures, add production if idle, and prioritize combat units over economy. Do not expand or invest in technology until army supply is at least 15 and bank is below 1000.

**Recheck:** At next decision cycle, verify army supply increased and bank decreased.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid overextending economy without defense

**When:** Early-midgame (around 240-300s) with own heavy production and tech, ground army. Opponent still ground macro with moderate production and light tech.

**Mistake → correction:** Overextending your economy without sufficient army to defend, or neglecting scouting for tech switches or all-ins. → Continue strengthening your ground army and expanding. Maintain production and tech progression. Consider adding Siege Tanks or other tech units to your composition.

**Why:** Your heavy production and tech give you a potential army quality advantage. Expanding further will secure your economy for the long game.

**Read for full checks:** `N002`

### L02 — Avoid falling behind in tech or upgrades

**When:** Midgame (around 420-480s) with own heavy ground army, heavy production and tech. Opponent has heavy production and tech, still ground-oriented.

**Mistake → correction:** Falling behind in tech or army upgrades, or over-committing to a single composition without scouting for tech switches. → Continue to strengthen your ground army and increase tech. Maintain production and consider adding more expansions if needed. Keep defenses strong.

**Why:** With both players having heavy economies, tech and army quality become decisive. Your Siege Tanks provide a strong defensive and offensive tool.

**Read for full checks:** `N003`

### L03 — Avoid overextending without scouting for all-ins

**When:** Early game (around 180s) with own heavy production and tech, ground army. Opponent similar to N001 but with lighter defense.

**Mistake → correction:** Overextending your economy without sufficient army to defend, or neglecting scouting for potential all-ins. → Maintain your production and tech, but consider applying light pressure to exploit the opponent's light defense. Continue expanding.

**Why:** Your heavy production can allow you to field a larger army quickly. Pressuring the opponent can disrupt their macro while you continue to develop.

**Read for full checks:** `N004`

## Decision Nodes

### [DEFAULT] N001 — Early Ground Macro with Heavy Tech

**Trigger situation:**  
Early game (around 180s) with own ground-oriented macro posture, heavy economy and tech, moderate production. Opponent appears as a ground macro Zerg with light tech and moderate production.

**Direction:**  
Continue developing your economy and tech while strengthening your ground army. Maintain defensive structures and consider expanding further.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Strength and Expansion

**Trigger situation:**  
Early-midgame (around 240-300s) with own heavy production and tech, ground army. Opponent still ground macro with moderate production and light tech.

**Direction:**  
Continue strengthening your ground army and expanding. Maintain production and tech progression. Consider adding Siege Tanks or other tech units to your composition.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Tech and Army Consolidation

**Trigger situation:**  
Midgame (around 420-480s) with own heavy ground army, heavy production and tech. Opponent has heavy production and tech, still ground-oriented.

**Direction:**  
Continue to strengthen your ground army and increase tech. Maintain production and consider adding more expansions if needed. Keep defenses strong.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early Game Heavy Production Alternative

**Trigger situation:**  
Early game (around 180s) with own heavy production and tech, ground army. Opponent similar to N001 but with lighter defense.

**Direction:**  
Maintain your production and tech, but consider applying light pressure to exploit the opponent's light defense. Continue expanding.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Air Transition and Ground Core

**Trigger situation:**  
Midgame (around 420-480s) with own ground army but moderate air presence, including Battlecruisers. Opponent heavy production and tech, ground-oriented.

**Direction:**  
Continue to strengthen your ground army while also developing your air presence. Increase production and tech, and consider expanding further.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early-Midgame Siege Tank Defense

**Trigger situation:**  
Early-midgame (around 360s) with own heavy production and tech, ground army with Siege Tanks. Opponent has moderate production and light tech, but with Roaches.

**Direction:**  
Maintain your defensive posture and continue to strengthen your ground army. Consider adding more Siege Tanks or Marauders to counter Roaches.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early Game Reaper Harass

**Trigger situation:**  
Early game (around 180s) with own moderate production and heavy tech, using Reapers. Opponent ground macro with light defense.

**Direction:**  
Use your Reaper to harass the opponent's economy and scout. Continue to develop your economy and tech, and consider expanding.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early-Midgame Marine-Reaper Composition

**Trigger situation:**  
Early-midgame (around 240s) with own heavy production and tech, using Marines and Reapers. Opponent ground macro with light defense.

**Direction:**  
Continue to strengthen your army and expand. Consider adding more production or tech units. Maintain pressure with Reapers if possible.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Late-Midgame Stabilization and Expansion

**Trigger situation:**  
Late-midgame (around 600s) with own heavy ground army, moderate air, and heavy economy. Opponent has heavy production and tech, with Mutalisks.

**Direction:**  
Stabilize your defenses against potential Mutalisk harassment. Continue to strengthen your ground army and consider adding anti-air units like Thors or Marines with upgrades.

**Read for details:** `N009`

---
