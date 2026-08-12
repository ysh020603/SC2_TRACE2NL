# TvP_O06 Technology / Economy / Production

## Skill Identity

- Skill ID: TvP_O06
- Matchup: Terran vs Protoss
- Opening Family: technology / economy / production opening
- Method: Executable Full V8

## Opening Strategy

A heavy-economy, heavy-technology, heavy-production opening that builds a strong ground core while keeping options open for air transitions.

Develop a technology / economy / production posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

## Strategic Characteristics

- Economy: heavy
- Production: heavy
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

### R01 — Maintain production tempo while teching

**When:** Early game (time < 360) with heavy tech/economy opening, own production buildings idle or insufficient, army supply below 15, and bank above 500.

**Correction:** Queue units from existing production structures first, prioritizing Marines and Marauders. If production is idle, build additional Barracks (with Reactors if tech lab available) to reach at least 3 active production structures. Keep worker production continuous until 2 bases are saturated (about 32 workers). Avoid adding new tech structures until army supply is above 15 and bank is below 500.

**Recheck:** At next decision cycle, verify that no production structure is idle, army supply is above 15, and bank is below 500.

### R02 — Counter enemy composition with tech and units

**When:** Enemy Intelligence indicates a specific composition: if opponent has air units (e.g., Void Rays, Phoenix, Oracle, Tempest) or heavy ground (e.g., Immortals, Stalkers) and own army lacks appropriate counters.

**Correction:** If enemy air is detected, add Engineering Bay for turrets at bases and produce Marines with Stimpack (if available) or transition to air units like Vikings or Battlecruisers if tech allows. If enemy heavy ground is detected, produce Marauders and Siege Tanks, and consider Widow Mines. Ensure detection (e.g., Raven or Missile Turret) if cloaked units are present. Maintain ground army strength while adding necessary tech.

**Recheck:** At next decision cycle, confirm that appropriate counter units are in production or queued, and detection is available if needed.

### R03 — Recover from low army and high bank

**When:** Army supply below 15, bank above 1000, and predicted advantage is OverwhelmingDisadvantage or threat flags indicate imminent attack.

**Correction:** Immediately convert bank into army: queue units from all production structures, build additional production if needed (e.g., Barracks, Factory) to maximize output. Prioritize defensive units (e.g., Marines, Siege Tanks) and ensure supply is not blocked. Do not expand or add tech until army supply is above 15 and bank is below 500. If production is insufficient, build more production structures before spending on upgrades.

**Recheck:** At next decision cycle, verify that army supply is above 15, bank is below 500, and production structures are actively producing.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid neglecting army production while teching

**When:** Early game, own ground macro with heavy production and tech, opponent posture unknown but heavy economy and tech.

**Mistake → correction:** Focusing solely on economy and technology, neglecting army production, leaving you vulnerable to early timing attacks. → Continue heavy production and technology, strengthen ground forces, and increase economy while maintaining expansion.

**Why:** A heavy tech/economy opening benefits from uninterrupted development; maintaining a strong ground core provides safety against early pressure.

**Read for full checks:** `N001`

### L02 — Avoid overextending without scouting

**When:** Early-midgame, own ground macro with Siege Tanks and Marines, opponent ground posture with Warp Prism.

**Mistake → correction:** Over-extending your army without proper scouting, leaving you vulnerable to warp prism harass. → Continue strengthening ground forces, maintain economy and production, and keep tech development on track.

**Why:** A ground-based composition with Siege Tanks provides strong defensive and offensive capability against a ground-oriented Protoss.

**Read for full checks:** `N002`

### L03 — Avoid neglecting ground army when transitioning to air

**When:** Late-midgame, own ground macro with Siege Tanks, Marines, Reapers, and Battlecruisers, opponent ground posture with Void Rays.

**Mistake → correction:** Neglecting your ground army while focusing on air, leaving you vulnerable to remaining ground forces. → Increase air presence and technology, strengthen air forces, and continue expanding.

**Why:** Void Rays are strong against ground, so transitioning to air with Battlecruisers provides a counter.

**Read for full checks:** `N010`

## Decision Nodes

### [DEFAULT] N001 — Early Ground Macro with Heavy Tech

**Trigger situation:**  
Early game, own ground macro posture with heavy production and tech, opponent posture unknown but heavy economy and tech.

**Direction:**  
Continue heavy production and technology, strengthen ground forces, and increase economy while maintaining expansion.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Consolidation

**Trigger situation:**  
Early-midgame, own ground macro with Siege Tanks and Marines, opponent ground posture with Warp Prism.

**Direction:**  
Continue strengthening ground forces, maintain economy and production, and keep tech development on track.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Expanding Ground with Widow Mines

**Trigger situation:**  
Early-midgame, own ground macro with Marines and Widow Mines, opponent ground posture with Warp Prism.

**Direction:**  
Increase expansion and continue production, while strengthening ground forces and maintaining tech.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Tech-Heavy Ground with Siege Tanks

**Trigger situation:**  
Early-midgame, own ground macro with Siege Tanks and Reapers, opponent unknown but heavy defense and tech.

**Direction:**  
Maintain production and tech, strengthen ground forces, and increase economy.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Ground with Air Support

**Trigger situation:**  
Midgame, own ground macro with Siege Tanks, Marines, Marauders, and Hellions, opponent ground posture with Stalkers and Immortals.

**Direction:**  
Increase air presence and technology, continue strengthening ground forces, and maintain economy.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Midgame Ground with Battlecruisers

**Trigger situation:**  
Midgame, own ground macro with Siege Tanks, Marines, Reapers, and Battlecruisers, opponent ground posture with Stalkers and Immortals.

**Direction:**  
Maintain ground strength, continue production and tech, and keep air presence moderate.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Late-Midgame Ground with Medivacs

**Trigger situation:**  
Late-midgame, own ground macro with Siege Tanks, Marines, Marauders, and Medivacs, opponent ground posture with Stalkers and Immortals.

**Direction:**  
Maintain ground strength, continue production and tech, and keep economy and expansion heavy.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early Game with Zealot Scout

**Trigger situation:**  
Early game, own ground macro with Marines, opponent unknown but with Zealot scout.

**Direction:**  
Continue production and tech, strengthen ground forces, and increase economy.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Defense Against Air

**Trigger situation:**  
Midgame, own ground macro with Siege Tanks, Marines, Banshees, and Widow Mines, opponent air posture with Phoenix and Oracle.

**Direction:**  
Increase defense, continue production and tech, and maintain ground strength while adding some air.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Late-Midgame Air Transition

**Trigger situation:**  
Late-midgame, own ground macro with Siege Tanks, Marines, Reapers, and Battlecruisers, opponent ground posture with Void Rays.

**Direction:**  
Increase air presence and technology, strengthen air forces, and continue expanding.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early-Midgame Air Transition

**Trigger situation:**  
Early-midgame, own ground macro with Marines, Reapers, Hellions, and Battlecruisers, opponent air posture with Tempest.

**Direction:**  
Increase air presence and technology, strengthen air forces, and continue expanding.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Early-Midgame Ground with Marauders

**Trigger situation:**  
Early-midgame, own ground macro with Siege Tanks, Reapers, and Marauders, opponent air posture with Tempest.

**Direction:**  
Maintain ground strength, continue production and tech, and keep economy heavy.

**Read for details:** `N012`

---
