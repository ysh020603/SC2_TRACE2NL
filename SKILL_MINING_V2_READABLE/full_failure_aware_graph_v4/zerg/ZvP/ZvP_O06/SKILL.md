# ZvP_O06 Economy / Expansion / Ground

## Skill Identity

- Skill ID: ZvP_O06
- Matchup: Zerg vs Protoss
- Opening Family: economy / expansion / ground opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg opening that prioritizes economy and expansion while building a ground-oriented army. The strategy focuses on developing a strong economy and tech base, with moderate production and a flexible transition path.

Develop a strong economy and expansion lead while maintaining a ground army core, then adapt to the opponent's tech or air transitions.

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

### R01 — Maintain production tempo and convert bank into army

**When:** At 4-6 minutes, if army supply is below 15 and bank is above 1500 minerals, or if active production structures are fewer than 3 and bank is above 1000 minerals.

**Correction:** Queue 2-3 units from each available hatchery or spawning pool, prioritizing Roaches or Hydralisks. If larvae are insufficient, build an extra hatchery or use injects. Ensure supply is available; if not, add one overlord. Recheck at next decision cycle.

**Recheck:** Army supply >= 15 or bank < 500 minerals, and production structures >= 3.

### R02 — Counter enemy composition with appropriate tech and units

**When:** If enemy intelligence reveals a ground army with Immortals, or an air transition with Phoenixes/Warp Prisms, or Carriers.

**Correction:** For Immortals: add Roaches or Hydralisks and continue teching. For air: build Hydralisks or Mutalisks, and add Spore Crawlers at bases. For Carriers: add Corruptors or Hydralisks and Spore Crawlers. Ensure tech structures are built and units queued.

**Recheck:** Army composition includes counters and anti-air defense is in place.

### R03 — Recover from low army and high bank

**When:** If army supply is below 15 and bank is above 2000 minerals, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately convert bank into army: queue units from all hatcheries, build additional hatcheries if larvae are insufficient, and ensure supply is available. Prioritize units that counter the enemy composition. Do not expand or tech until army supply is above 15 and bank is below 1000.

**Recheck:** Army supply >= 15 and bank < 1000 minerals.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Counter Immortal-heavy ground armies

**When:** Midgame, around 7 minutes, when opponent has a ground army with Immortals and you have heavy defense and tech investment.

**Mistake → correction:** Staying on a small ground army and continuing to tech without increasing production, leaving you vulnerable to being overwhelmed. → Continue teching and increase army production. Add units that counter Immortals, such as Roaches or Hydralisks.

**Why:** Immortals are strong against armored units, so you need a mix of units. Your tech investment will provide upgrades to help in the fight.

**Read for full checks:** `N005`

### L02 — Transition to anti-air against Phoenix/Warp Prism

**When:** Midgame, around 8 minutes, when opponent transitions to an air-based army with Phoenixes and Warp Prisms, and you have a heavy ground defense.

**Mistake → correction:** Staying on a ground-only army and continuing to strengthen ground forces, leaving you vulnerable to air harassment. → Add anti-air units such as Hydralisks or Mutalisks. Consider building Spore Crawlers for defense.

**Why:** The opponent's air army requires anti-air capabilities. Your strong economy can support a tech switch to counter.

**Read for full checks:** `N007`

### L03 — Maintain flexibility against unknown tech

**When:** Early game, around 3 minutes, with a heavy economy and expansion, while opponent's tech is unknown but heavy.

**Mistake → correction:** Overcommitting to a specific tech path before knowing the opponent's plan, risking a poor matchup. → Continue expanding and teching. Maintain a ground army for safety and scout for tech choices.

**Why:** A strong economy and tech lead will give you an advantage in the mid-game. Ground army provides defense against early pressure.

**Read for full checks:** `N008`

## Decision Nodes

### [DEFAULT] N001 — Early Economy and Expansion Focus

**Trigger situation:**  
Early game, around 3-4 minutes, with a heavy economy and expansion posture. Opponent is unknown or light, with heavy tech investment.

**Direction:**  
Continue developing your economy and expansion. Maintain a ground army core and keep scouting to detect tech or air transitions.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Mid-Game Ground Army Strengthening

**Trigger situation:**  
Around 5 minutes, opponent shows a ground-based army with Zealots and Stalkers. Your economy is strong, and you are expanding.

**Direction:**  
Increase your ground army production and continue teching. Consider adding Roaches or Hydralisks to counter the ground composition.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Tech Investment and Defense

**Trigger situation:**  
Around 6 minutes, opponent still has a heavy ground army. You have a moderate defense and are investing in technology.

**Direction:**  
Continue teching while maintaining a defensive posture. Consider adding units that counter the opponent's composition, such as Roaches or Banelings.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Maintain and Adapt

**Trigger situation:**  
Around 6 minutes, opponent has a ground army. Your economy is strong, but your tech is light.

**Direction:**  
Maintain your current production and defense. Consider adding a few tech structures to prepare for the mid-game.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Mid-Game Tech and Army Expansion

**Trigger situation:**  
Around 7 minutes, opponent has a ground army with Immortals. You have a heavy defense and are investing in tech.

**Direction:**  
Continue teching and increase your army production. Consider adding units that counter Immortals, such as Roaches or Hydralisks.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Mid-Game Army Consolidation

**Trigger situation:**  
Around 8 minutes, opponent has a ground army with Observers and Immortals. You have a heavy defense and are producing heavily.

**Direction:**  
Consolidate your army and continue producing. Consider adding Hydralisks or Lurkers for anti-ground damage.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Air Transition Defense

**Trigger situation:**  
Around 8 minutes, opponent transitions to an air-based army with Phoenixes and Warp Prisms. You have a heavy ground defense.

**Direction:**  
Add anti-air units such as Hydralisks or Mutalisks. Consider building Spore Crawlers for defense.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early Game Expansion and Tech

**Trigger situation:**  
Early game, around 3 minutes, with a heavy economy and expansion. Opponent is unknown, but tech-heavy.

**Direction:**  
Continue expanding and teching. Maintain a ground army for safety and scout for tech choices.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Late Mid-Game Ground Army

**Trigger situation:**  
Around 10 minutes, opponent has a ground army with Observers and Immortals. You have a heavy defense and production.

**Direction:**  
Maintain your army and continue producing. Consider adding upgrades and tech units like Lurkers or Brood Lords.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Late Game Carrier Transition

**Trigger situation:**  
Around 10 minutes, opponent transitions to Carriers. You have a heavy ground defense and production.

**Direction:**  
Add anti-air units such as Hydralisks, Corruptors, or Mutalisks. Consider building Spore Crawlers for defense.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early Air Harass Defense

**Trigger situation:**  
Around 5 minutes, opponent has Phoenixes and Oracles. You have a moderate defense and are teching.

**Direction:**  
Add anti-air units such as Hydralisks or Queens. Consider building Spore Crawlers for defense.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Early Expansion and Army

**Trigger situation:**  
Around 4 minutes, opponent is unknown but tech-heavy. You have a heavy defense and are expanding.

**Direction:**  
Continue expanding and teching. Maintain a ground army for safety and scout for tech choices.

**Read for details:** `N012`

---
