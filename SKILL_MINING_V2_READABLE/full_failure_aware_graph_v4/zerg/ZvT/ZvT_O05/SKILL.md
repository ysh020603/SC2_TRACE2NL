# ZvT_O05 Expansion / Economy / Production

## Skill Identity

- Skill ID: ZvT_O05
- Matchup: Zerg vs Terran
- Opening Family: expansion / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg opening that prioritizes economy and expansion while maintaining a flexible ground-oriented posture. Early game focuses on queens and zerglings, with technology investment ramping up through the midgame. The opponent is expected to follow a ground-heavy Terran composition, but the plan remains adaptable to observed enemy tech choices.

Develop a strong economy and production base while preserving flexibility to respond to the opponent's tech and army composition. Aim to reach a midgame with a solid ground army and the option to transition into air if needed.

This is a strategic template, not a fixed build order. Adapt based on live scouting and enemy intelligence.

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

### R01 — Maintain production tempo and worker saturation

**When:** At any time before 6 minutes, if workers below 30 or production structures below 3, or if bank exceeds 1000 minerals and 200 gas while army supply is below 15.

**Correction:** Queue workers from all hatcheries until saturation (target 60+ workers). Build additional hatcheries if production structures are below 3 and bank is high. If army supply is below 15, prioritize producing zerglings or roaches to defend. Avoid expanding until production is sufficient and army is above 15 supply.

**Recheck:** Recheck at next decision cycle: workers >= 60, production structures >= 3, bank < 1000 minerals, army supply >= 15.

### R02 — Counter enemy composition with tech and units

**When:** If enemy intelligence reveals a ground-heavy Terran composition (e.g., marines, marauders, tanks) and you have not yet invested in roaches or hydralisks, or if enemy has air units (e.g., banshees, battlecruisers) and you lack anti-air.

**Correction:** If ground-heavy, add roaches or hydralisks to your army and start upgrades (e.g., missile attacks, carapace). If air-heavy, build spore crawlers at bases and produce hydralisks or corruptors. Ensure you have the necessary tech structures (e.g., roach warren, hydralisk den, spire) and queue units accordingly.

**Recheck:** Recheck at next decision cycle: army composition includes appropriate counters, tech structures completed, and anti-air defense in place if needed.

### R03 — Recover from low army and high bank

**When:** If army supply is below 15 and bank exceeds 2000 minerals and 500 gas, or if predicted advantage is OverwhelmingDisadvantage, or if any owned base is threatened.

**Correction:** Immediately convert bank into army: queue zerglings, roaches, or hydralisks from all hatcheries. If production structures are insufficient, build additional hatcheries. Prioritize defending threatened bases with static defense (spore crawlers, spine crawlers) if needed. Do not expand or tech until army supply is above 15 and bank is reduced.

**Recheck:** Recheck at next decision cycle: army supply >= 15, bank < 1000 minerals, and no owned base under threat.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid over-expanding without defense

**When:** Early-midgame, when you have a ground-oriented posture with moderate production and light tech, and the opponent is also ground-oriented with heavy production and tech.

**Mistake → correction:** Focusing solely on expanding and teching up while neglecting army production and defense, leaving you vulnerable to enemy aggression. → Increase your expansion and production while investing in technology, but ensure you maintain a defensive force to protect your bases.

**Why:** A strong economy and tech base will allow you to transition into a powerful midgame army, but only if you survive the early-midgame pressure.

**Read for full checks:** `N011`

### L02 — Avoid passivity in early game

**When:** Early game, when you have a ground-oriented posture with moderate production and light tech, and the opponent is ground-oriented with moderate production and heavy tech.

**Mistake → correction:** Being too passive and focusing only on economy and expansion, allowing the Terran to dictate the pace and apply pressure without resistance. → Maintain your economy and expansion rate while producing queens for defense. Continue teching towards a midgame composition.

**Why:** A strong economy allows you to outproduce the opponent in the midgame. Queens provide cost-effective defense against early pressure and creep spread.

**Read for full checks:** `N001`

### L03 — Avoid over-investing in tech at the expense of army

**When:** Early-midgame, when you have a ground-oriented posture with moderate production and heavy tech, and the opponent is ground-oriented with heavy production and tech.

**Mistake → correction:** Over-investing in technology and upgrades while neglecting army size and scouting, leaving you unprepared for an enemy attack. → Increase your technology and production to match the opponent. Continue expanding and strengthening your ground army.

**Why:** Investing in technology now allows you to unlock key units like Hydralisks or Roaches, which are essential against a Terran ground army, but you must also maintain a sufficient army to defend.

**Read for full checks:** `N003`

## Decision Nodes

### [DEFAULT] N001 — Early Game Foundation

**Trigger situation:**  
At the start of the game, focus on establishing a solid economy and early defense.

**Direction:**  
Maintain your economy and expansion rate while producing queens for defense. Continue teching towards a midgame composition.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Midgame Expansion

**Trigger situation:**  
As the game progresses into the early-midgame, continue expanding and increasing production.

**Direction:**  
Continue to strengthen your ground army and increase production. Maintain your expansion rate and start investing more in technology.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Tech Investment

**Trigger situation:**  
Entering the midgame, focus on increasing technology and production to match the opponent's heavy investment.

**Direction:**  
Increase your technology and production to match the opponent. Continue expanding and strengthening your ground army.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Army Strengthening

**Trigger situation:**  
In the late-midgame, focus on strengthening your army and maintaining your economy.

**Direction:**  
Continue to strengthen your ground army and increase technology. Maintain your expansion and production.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Army Composition

**Trigger situation:**  
In the midgame, focus on building a balanced army composition to counter the opponent's ground forces.

**Direction:**  
Strengthen your ground army and consider adding units like Hydralisks or Roaches to counter the opponent's composition.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Midgame Tech Transition

**Trigger situation:**  
In the midgame, consider transitioning to a more advanced army composition based on the opponent's tech.

**Direction:**  
Continue to strengthen your ground army and consider adding air units if the opponent transitions to Battlecruisers.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Late-Midgame Hydralisk Composition

**Trigger situation:**  
In the late-midgame, focus on a Hydralisk-based army to counter the opponent's ground forces.

**Direction:**  
Continue to strengthen your Hydralisk-based army and consider upgrades to increase their effectiveness.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Zergling Pressure

**Trigger situation:**  
In the midgame, use zerglings to apply pressure while maintaining your economy.

**Direction:**  
Use zerglings for harassment and map control while teching up to a stronger army.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Air Transition

**Trigger situation:**  
In the midgame, consider transitioning to a Mutalisk-based army to harass and control the map.

**Direction:**  
Increase your air presence and use Mutalisks for harassment and map control.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Late-Midgame Air Harassment

**Trigger situation:**  
In the late-midgame, continue to use Mutalisks for harassment and map control.

**Direction:**  
Continue to strengthen your air army and use Mutalisks to harass expansions and force the opponent to react.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early-Midgame Tech Expansion

**Trigger situation:**  
In the early-midgame, focus on expanding and teching up to prepare for the midgame.

**Direction:**  
Increase your expansion and production while investing in technology.

**Read for details:** `N011`

---
