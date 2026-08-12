# TvZ_O02 Technology / Economy / Production

## Skill Identity

- Skill ID: TvZ_O02
- Matchup: Terran vs Zerg
- Opening Family: technology / economy / production opening
- Method: Executable-Normalized Full V11

## Opening Strategy

This opening emphasizes developing a technology and economy foundation while keeping production flexible. Early game is characterized by uncertainty in both own and opponent postures, with a focus on safe development and scouting. As the game progresses, the path can branch into a heavier ground-oriented composition if the opponent shows a ground macro posture.

Develop a technology / economy / production posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

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

### G05 — Terran production interpretation

- Scale Barracks/Factory/Starport capacity before ordering add-ons or units that lack a completed parent structure.

## V4 Matchup-Specific Corrections

### R01 — Production Tempo and Bank Conversion

**When:** At any time, if bank is above 800 minerals and production is below 3 active structures, or if army supply is below 15 and bank is above 1000.

**Correction:** Queue units from existing production structures, prioritizing Marines and Marauders. If no production structures exist, build a Barracks with a Reactor if prerequisites allow. If supply is not blocked and bank remains high, add a second Barracks or Factory. Do not expand until army supply is at least 15 and production is active.

**Recheck:** Recheck at next decision cycle.

### R02 — Counter Zerg Ground Composition

**When:** Enemy Intelligence shows Zergling, Roach, or Hydralisk, and own army lacks sufficient anti-ground or anti-armor units.

**Correction:** If Roaches or Hydralisks are present, add Marauders and Siege Tanks. If Zerglings are the main threat, ensure Hellions or Widow Mines are available. Continue producing Marines as core. If Factory is not built, construct one with a Tech Lab for Siege Tanks. Maintain at least 2 production structures per base.

**Recheck:** Recheck at next decision cycle.

### R03 — Recovery from Low Army and High Bank

**When:** Army supply is below 15, bank is above 1500, or predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all available production structures, prioritizing combat units. If production is insufficient, build additional Barracks or Factories. Do not spend on expansions or technology until army supply is at least 20 and bank is below 500. If supply is blocked, add a supply depot.

**Recheck:** Recheck at next decision cycle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Defend and Expand

**When:** Late midgame, both sides have heavy ground-oriented postures. Opponent shows Zergling, Roach, Queen. Own army includes Siege Tank, Marine, Reaper, Marauder.

**Mistake → correction:** Overextending with ground forces without proper support, neglecting upgrades or production. → Strengthen ground army, increase defense, economy, and expansion. Continue production and technology.

**Why:** With both sides committed to ground, maintaining a strong defensive position while expanding economy supports a larger army. Siege tanks and marines provide a solid core.

**Read for full checks:** `N006`

### L02 — Early Ground Threat: Flexible Response

**When:** Early game, opponent shows a ground posture with Zergling. Own economy is moderate with heavy expansion.

**Mistake → correction:** Over-teching without sufficient army production, allowing opponent's Zerglings to punish greed. → Strengthen ground army, increase economy, increase expansion, continue production and technology.

**Why:** The opponent's ground posture suggests a potential ground-based army. Maintaining flexible development allows you to respond appropriately without overcommitting.

**Read for full checks:** `N010`

### L03 — Midgame Ground Clash: Solid Core

**When:** Midgame, both sides have heavy ground-oriented postures. Opponent shows Zergling, Hydralisk, Roach, Queen. Own army includes Marine.

**Mistake → correction:** Overextending without proper support, neglecting upgrades or production. → Strengthen ground army, increase economy, continue production and technology.

**Why:** With both sides committed to ground, maintaining a strong army composition is important. Marines provide a solid core, but consider adding supporting units like Marauders or Siege Tanks.

**Read for full checks:** `N012`

## Decision Nodes

### [DEFAULT] N001 — Early Game Development with Safety Checks

**Trigger situation:**  
Early game, both sides have limited information. Opponent posture is unknown, own posture is also uncertain. Focus on establishing a solid foundation.

**Direction:**  
Maintain current development path with safety checks. Keep production, economy, technology, and expansion directions steady.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Late Midgame Development with Safety Checks

**Trigger situation:**  
Late midgame, still limited information. Both sides maintain unknown postures. Continue safe development.

**Direction:**  
Maintain current development path with safety checks. Keep production, economy, technology, and expansion directions steady.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Development with Safety Checks

**Trigger situation:**  
Midgame, still limited information. Both sides maintain unknown postures. Continue safe development.

**Direction:**  
Maintain current development path with safety checks. Keep production, economy, technology, and expansion directions steady.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early Midgame Development with Safety Checks

**Trigger situation:**  
Early midgame, still limited information. Both sides maintain unknown postures. Continue safe development.

**Direction:**  
Maintain current development path with safety checks. Keep production, economy, technology, and expansion directions steady.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Midgame Ground Posture Recognition

**Trigger situation:**  
Early midgame, opponent shows a ground macro posture with Zergling and Queen cues. Own posture still unknown. This is a signal to start leaning towards a ground-oriented response.

**Direction:**  
Maintain current development path with safety checks. Keep production, economy, technology, and expansion directions steady.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Late Midgame Ground vs Ground Confrontation

**Trigger situation:**  
Late midgame, both sides have heavy ground-oriented postures. Opponent shows Zergling, Roach, Queen. Own army includes Siege Tank, Marine, Reaper, Marauder. This is a direct confrontation scenario.

**Direction:**  
Strengthen ground army, increase defense, economy, and expansion. Continue production and technology.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early Midgame Ground Posture with Heavy Economy

**Trigger situation:**  
Early midgame, opponent shows a ground posture with Zergling. Own economy is moderate with heavy expansion. This is a signal to start leaning towards a ground-oriented response.

**Direction:**  
Strengthen ground army, increase economy, continue production and technology.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early Midgame Ground Posture with Moderate Economy

**Trigger situation:**  
Early midgame, opponent shows a ground posture with Zergling. Own posture is ground-oriented with Marine. This is a signal to start leaning towards a ground-oriented response.

**Direction:**  
Strengthen ground army, increase economy, continue technology.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Early Game Ground Posture with Heavy Economy

**Trigger situation:**  
Early game, opponent shows a ground posture with Zergling. Own economy is moderate with light expansion. This is a signal to start leaning towards a ground-oriented response.

**Direction:**  
Strengthen ground army, increase economy, increase production, continue technology.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Early Game Ground Posture with Heavy Expansion

**Trigger situation:**  
Early game, opponent shows a ground posture with Zergling. Own economy is moderate with heavy expansion. This is a signal to start leaning towards a ground-oriented response.

**Direction:**  
Strengthen ground army, increase economy, increase expansion, continue production and technology.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early Midgame Ground Posture with Heavy Defense

**Trigger situation:**  
Early midgame, opponent shows a ground posture with Zergling and Queen. Own posture is ground-oriented with heavy defense. This is a signal to start leaning towards a ground-oriented response.

**Direction:**  
Strengthen ground army, increase economy, increase production, continue technology.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Midgame Ground vs Ground Confrontation

**Trigger situation:**  
Midgame, both sides have heavy ground-oriented postures. Opponent shows Zergling, Hydralisk, Roach, Queen. Own army includes Marine. This is a direct confrontation scenario.

**Direction:**  
Strengthen ground army, increase economy, continue production and technology.

**Read for details:** `N012`

---
