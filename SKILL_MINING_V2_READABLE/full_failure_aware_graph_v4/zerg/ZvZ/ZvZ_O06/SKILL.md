# ZvZ_O06 Expansion / Economy / Production

## Skill Identity

- Skill ID: ZvZ_O06
- Matchup: Zerg vs Zerg
- Opening Family: expansion / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg versus Zerg opening that prioritizes a heavy economy and expansion posture while maintaining moderate production and light technology investment. The early game focuses on establishing a strong economic base with Queens and Zerglings for safety, then transitions into a ground-oriented midgame with options to tech into air if the opponent commits to Mutalisks.

Develop a strong economy and production base while preserving flexibility to adapt to the opponent's tech choices. Aim to reach a heavy economy and production state by the midgame, with the option to transition into air if the opponent goes Mutalisk.

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

### R01 — Maintain production tempo and economy

**When:** At any time before 6 minutes, if army supply is below 15 and bank is above 500, or if production structures are idle or insufficient relative to income.

**Correction:** Prioritize spending bank on army production and additional production structures (e.g., Hatcheries) to convert resources into units. Keep workers flowing toward saturation (target 2 per base on minerals, 3 per gas) without letting worker queues crowd out defense. Ensure supply is added just in time to avoid blocking production.

**Recheck:** Recheck at next decision cycle: army supply should be increasing, bank reduced, and production structures active.

### R02 — Counter enemy composition

**When:** When enemy intelligence reveals a significant air presence (e.g., Mutalisks) or heavy ground (e.g., Roaches) that threatens your current army composition.

**Correction:** Adjust production and technology to counter the observed threat. If enemy has air, add Hydralisks and Spore Crawlers at bases; if enemy has heavy ground, add Roaches or Hydralisks for durability and damage. Continue developing economy and production to sustain the counter.

**Recheck:** Recheck at next decision cycle: ensure counter units are in production or queued, and tech structures are completed or underway.

### R03 — Recover from low army and high bank

**When:** When army supply is below 15, bank is above 1000, and predicted advantage is OverwhelmingDisadvantage, or when owned zones are threatened.

**Correction:** Immediately convert bank into army and production. Prioritize building units from existing structures and adding production if needed. Do not expand or tech until army supply is above 15 and bank is reduced. If threatened, reinforce defenses with static structures (e.g., Spore Crawlers) and units.

**Recheck:** Recheck at next decision cycle: army supply should be above 15, bank reduced, and threat mitigated.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Balance economy and tech with defense

**When:** Early-midgame, both players are on ground with moderate production and tech, and you have a strong economy.

**Mistake → correction:** Focusing solely on economy and neglecting army production, leaving you vulnerable to a sudden attack. → Continue developing economy and production, maintain a moderate ground army, and start teching up. Keep defense light but be ready to react to pressure.

**Why:** Teching early keeps you ahead, while a moderate army deters attacks and allows safe tech investment.

**Read for full checks:** `N002`

### L02 — Match opponent's heavy ground with tech and economy

**When:** Midgame, opponent has heavy ground (Zergling, Roach, Queen) with heavy production and tech; you have moderate ground (Zergling, Hydralisk, Queen) and moderate tech.

**Mistake → correction:** Over-investing in a single unit composition without scouting, risking a surprise switch to air or different ground. → Strengthen your ground army to match the opponent's composition, continue developing economy and production, and consider increasing technology for better units.

**Why:** A strong ground army defends and counters, while economy sustains it. Hydralisks counter Roaches, Zerglings provide mobility.

**Read for full checks:** `N003`

### L03 — Maintain ground strength and tech for efficiency

**When:** Late-midgame, both have heavy ground armies (Zergling, Roach, Queen) with heavy production and moderate tech.

**Mistake → correction:** Falling into a pure ground vs ground fight without considering composition advantage, risking inefficiency. → Continue strengthening your ground army, maintain heavy production, and consider increasing technology to get Roaches or Hydralisks. Keep defense strong.

**Why:** Adding Roaches gives durability, Hydralisks provide anti-air and damage. Heavy economy sustains a large army.

**Read for full checks:** `N004`

## Decision Nodes

### [DEFAULT] N001 — Early Game Economy and Safety

**Trigger situation:**  
At the start of the game, both players are in a ground macro posture with heavy economy and expansion, light technology, and moderate production. The opponent is likely to have Zerglings and Queens, with possible early pressure.

**Direction:**  
Maintain your economy and expansion while strengthening your ground army. Keep your defense light but be ready to react to early pressure. Continue producing Queens and Zerglings to maintain safety.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Midgame Development

**Trigger situation:**  
In the early-midgame, both players are still in a ground macro posture with heavy economy and expansion, but technology is starting to increase. The opponent may have Zerglings and Queens, with possible pressure.

**Direction:**  
Continue developing your economy and production. Maintain your ground army and consider increasing your technology. Keep your defense light but be ready to react to pressure.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Army Strengthening

**Trigger situation:**  
In the midgame, the opponent has a heavy ground army with Zerglings, Roaches, and Queens, and heavy production and technology. You have a moderate ground army with Zerglings, Hydralisks, and Queens, and moderate technology.

**Direction:**  
Strengthen your ground army to match the opponent's composition. Continue developing your economy and production. Maintain your defense and consider increasing your technology to get better units.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Ground Dominance

**Trigger situation:**  
In the late-midgame, the opponent has a heavy ground army with Zerglings, Roaches, and Queens, and heavy production and moderate technology. You have a heavy ground army with Zerglings and Queens, and heavy production and moderate technology.

**Direction:**  
Continue strengthening your ground army and maintain your heavy production. Consider increasing your technology to get better units like Roaches or Hydralisks. Keep your defense strong.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early-Midgame Tech and Expansion

**Trigger situation:**  
In the early-midgame, the opponent has a light ground posture with only Queens, and moderate production and light technology. You have a moderate ground posture with Queens and Overseers, and moderate technology.

**Direction:**  
Increase your technology and continue expanding. Maintain your ground army and consider adding more production. Keep your defense strong.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early-Midgame Aggressive Expansion

**Trigger situation:**  
In the early-midgame, the opponent has a ground posture with Zerglings and Queens, and moderate production and light technology. You have a light ground posture with Queens, and moderate production and light technology.

**Direction:**  
Increase your expansion and production to get ahead economically. Continue developing your ground army and technology. Keep your defense light but be ready to react.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Midgame Defensive Stance

**Trigger situation:**  
In the midgame, the opponent has a heavy ground army with Zerglings, Roaches, and Queens, and heavy production and technology. You have a moderate ground army with Roaches and Queens, and moderate production and technology.

**Direction:**  
Increase your defense and continue developing your economy and production. Strengthen your ground army to match the opponent's. Consider increasing your technology to get better units.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Air Transition

**Trigger situation:**  
In the midgame, the opponent has a heavy ground army with Zerglings, Roaches, and Queens, and heavy production and technology. You have a heavy air presence with Mutalisks, Zerglings, Queens, and Overseers, and heavy production and moderate technology.

**Direction:**  
Increase your air army and continue developing your economy. Maintain your ground army for defense. Consider increasing your technology to get better air units.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Late-Midgame Defensive Tech

**Trigger situation:**  
In the late-midgame, the opponent has a heavy air presence with Mutalisks, Zerglings, and Queens, and heavy production and technology. You have a heavy ground army with Roaches and Queens, and heavy production and technology.

**Direction:**  
Increase your defense and continue developing your economy and production. Consider adding anti-air units like Hydralisks or Spore Crawlers. Maintain your ground army.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Late-Midgame Air Harassment

**Trigger situation:**  
In the late-midgame, the opponent has a heavy ground army with Zerglings, Roaches, and Queens, and heavy production and technology. You have a heavy air presence with Mutalisks, Zerglings, Queens, and Overseers, and heavy production and moderate technology.

**Direction:**  
Increase your air army and continue harassing the opponent. Maintain your ground army for defense. Consider increasing your technology to get better air units.

**Read for details:** `N010`

---
