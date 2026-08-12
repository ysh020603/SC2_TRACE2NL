# PvT_O03 Technology / Economy / Production

## Skill Identity

- Skill ID: PvT_O03
- Matchup: Protoss vs Terran
- Opening Family: technology / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Protoss opening that emphasizes heavy technology and economy while maintaining moderate production, aiming to reach a strong midgame army composition.

Develop a technology / economy / production posture while preserving flexibility for live observation-driven adaptation.

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

### R01 — Maintain production tempo and convert bank into army

**When:** At any time, if bank is above 400 minerals and 200 gas, or if active production queues are empty while army supply is below 40, or if supply is not blocked and production capacity is idle.

**Correction:** Prioritize adding production structures (Gateways, Robotics Facilities, or Stargates) up to a reasonable count for your economy, then queue units from existing structures. If army supply is below 15, do not expand; instead, spend bank on units and production. Ensure prerequisites for tech structures are met before building them.

**Recheck:** Recheck at next decision cycle: verify bank is below 300 minerals and 150 gas, and that all production structures have at least one unit queued.

### R02 — Counter enemy composition with tech and units

**When:** When enemy intelligence reveals a composition: if Terran has heavy bio with Medivacs, or Siege Tanks, or air units like Banshees or Liberators, and your army lacks appropriate counters.

**Correction:** If enemy has Siege Tanks, build Immortals and use Stalkers for mobility. If enemy has heavy bio, add Colossi or High Templar with Psionic Storm. If enemy has air, add Stalkers and Phoenixes or Archons. Ensure required tech structures (Robotics Bay, Templar Archives, Stargate) are built and queued. Maintain a mix of Zealots and Stalkers for a solid ground core.

**Recheck:** Recheck at next decision cycle: confirm you have at least one counter unit type for the observed enemy composition, and that tech structures are either completed or under construction.

### R03 — Recover from low army and high bank

**When:** When army supply is below 15 and bank is above 500 minerals and 300 gas, or when predicted advantage is OverwhelmingDisadvantage, or when an owned base is threatened.

**Correction:** Immediately convert bank into army by queuing units from all available production structures. If production is insufficient, build additional Gateways or other production structures first, then queue units. Prioritize defensive units like Zealots and Stalkers. Do not expand or tech further until army supply is above 30 and bank is below 300 minerals.

**Recheck:** Recheck at next decision cycle: verify army supply is above 30 and bank is below 300 minerals, or that the threat has passed.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid overextending economy without defense

**When:** Early-midgame, around 300 seconds, with heavy economy and production, opponent ground posture with possible Reaper harassment.

**Mistake → correction:** Continuing to expand and tech aggressively without ensuring defensive capability, leaving yourself vulnerable to early pressure like Reaper harassment. → Continue developing economy and technology, but strengthen your ground army and maintain a defensive posture while scouting for pressure.

**Why:** Your heavy investment will pay off midgame, but you need to survive early pressure. A solid ground core with Zealots and Stalkers provides flexibility.

**Read for full checks:** `N001`

### L02 — Avoid assuming enemy build without scouting

**When:** Early game, around 180 seconds, with heavy economy and tech, opponent posture unknown.

**Mistake → correction:** Making assumptions about the enemy's build without scouting, potentially neglecting defense while teching. → Continue developing economy and technology, while scouting to determine opponent's intentions. Build a solid foundation for midgame.

**Why:** Early game is about setting up economy and tech; scouting allows adaptation to opponent's strategy.

**Read for full checks:** `N003`

### L03 — Avoid neglecting upgrades and positioning

**When:** Late-midgame, around 600 seconds, opponent has heavy ground army with Siege Tanks and Medivacs, you have strong economy but need to solidify army.

**Mistake → correction:** Neglecting upgrades and being caught out of position, as opponent may have high attack/defense upgrades and attempt a timing attack. → Continue to strengthen ground army with tech units like Immortals and Colossi, while maintaining economy and expansion lead.

**Why:** Opponent's army is strong; Immortals counter tanks, Colossi handle bio, and upgrades are crucial.

**Read for full checks:** `N004`

## Decision Nodes

### [DEFAULT] N001 — Early-Midgame Ground Development

**Trigger situation:**  
At around 300 seconds, both sides have a heavy economy and production, with the opponent showing a ground posture and possible pressure.

**Direction:**  
Continue developing your economy and technology, strengthen your ground army, and maintain a defensive posture while scouting for pressure.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Army Strengthening

**Trigger situation:**  
At around 480-540 seconds, the opponent has a heavy ground army with Medivacs, and you have a solid economy but need to strengthen your army.

**Direction:**  
Increase your production and technology to strengthen your ground army, while maintaining your economy and expansion lead.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Game Tech and Economy Focus

**Trigger situation:**  
At around 180 seconds, both sides are in the early game with heavy economy and technology, but the opponent's posture is unknown.

**Direction:**  
Continue to develop your economy and technology, while scouting to determine the opponent's intentions. Build a solid foundation for your midgame.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Ground Army with Tech

**Trigger situation:**  
At around 600 seconds, the opponent has a heavy ground army with Siege Tanks and Medivacs, and you have a strong economy but need to solidify your army.

**Direction:**  
Continue to strengthen your ground army with tech units like Immortals and Colossi, while maintaining your economy and expansion lead.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game Ground Army Development

**Trigger situation:**  
At around 180 seconds, the opponent shows a ground posture with Marines and Marauders, and you have a Stalker but need to build your army.

**Direction:**  
Continue to develop your economy and technology, while building a ground army to defend against potential pressure.

**Read for details:** `N005`

---
