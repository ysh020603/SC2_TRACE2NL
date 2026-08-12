# PvP_O04 Technology / Economy / Upgrade

## Skill Identity

- Skill ID: PvP_O04
- Matchup: Protoss vs Protoss
- Opening Family: technology / economy / upgrade opening
- Method: Executable-Normalized Full V11

## Opening Strategy

A Protoss mirror opening that prioritizes heavy technology and economy development while keeping production moderate. The early game is flexible, with the option to transition into ground, air, or mixed compositions based on scouting and opponent posture.

Develop a technology / economy / upgrade posture while preserving flexibility for live observation-driven adaptation.

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

### R01 — Maintain Tech/Economy Tempo with Production Scaling

**When:** Game time is between 4 and 6 minutes, bank is above 800 minerals, and active production structures are fewer than 3, or all production structures are idle.

**Correction:** Prioritize adding a Gateway or Warp Gate if prerequisites are met, and queue at least 2 units per production structure. If Robotics Facility or Stargate is available, queue a unit from it. Keep worker production continuous until saturation (around 2 per base). Avoid spending on technology or expansions until production is active and bank is below 500 minerals.

**Recheck:** At the next decision cycle, verify that production structures are active (queues non-empty) and bank is below 500 minerals. If not, repeat the correction.

### R02 — Counter Enemy Ground Composition with Tech and Army Mix

**When:** Enemy Intelligence shows a ground-heavy composition (e.g., Zealots, Stalkers, Sentries, Immortals) and your army supply is above 15.

**Correction:** Ensure your army includes a mix of ground units (Zealots, Stalkers) and add air support (e.g., Oracles, Phoenixes) if tech allows. Prioritize building a Robotics Facility or Stargate if not already present, and queue units that counter the enemy composition. Maintain economy and technology development to support the transition.

**Recheck:** At the next decision cycle, confirm that your army composition includes both ground and air units, and that production structures are active. If not, adjust production queues accordingly.

### R03 — Recover from Low Army and High Bank

**When:** Army supply is below 15, bank is above 1000 minerals, and predicted advantage is not OverwhelmingAdvantage.

**Correction:** Immediately convert bank into army by queuing units from all available production structures. If production is insufficient, add a Gateway or Warp Gate (if prerequisites met) and queue units. Prioritize defensive units (e.g., Stalkers, Zealots) to protect bases. Do not expand or invest in technology until army supply is above 15 and bank is below 500 minerals.

**Recheck:** At the next decision cycle, verify that army supply has increased and bank is reduced. If not, continue producing units and consider adding production structures.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground Commitment vs. Balanced Expansion

**When:** Early-midgame (around 4 minutes) when both players have heavy economy and tech, and the opponent shows a ground posture with Stalkers.

**Mistake → correction:** Over-committing to a single ground tech path without scouting, potentially neglecting defense against possible pressure. → Strengthen ground forces while increasing economy and expansion. Maintain defense and continue production.

**Why:** The opponent is ground-focused, so reinforcing your ground army and expanding your economy will set up a strong midgame. Heavy technology investment supports future transitions.

**Read for full checks:** `N001`

### L02 — Matching Ground Strength

**When:** Midgame (around 8 minutes) when both players have heavy economies and tech, and the opponent shows a ground posture with Zealots, Stalkers, Sentries, and Immortals.

**Mistake → correction:** Over-committing to a single tech path without scouting, or neglecting defense against possible pressure. → Continue strengthening ground forces and maintain economy and expansion. Keep technology development ongoing.

**Why:** The opponent's ground composition is strong, so matching with a robust ground army and maintaining tech advantages will keep you competitive.

**Read for full checks:** `N002`

### L03 — Air Harassment Against Ground

**When:** Early-midgame (around 5 minutes) when the opponent shows a ground posture with Stalkers, but you have a mixed army with Oracles and a heavy economy.

**Mistake → correction:** Over-committing to air without sufficient ground support, or neglecting economy. → Increase air presence and strengthen air forces while continuing economy and technology development.

**Why:** The opponent is ground-focused, so adding air units like Oracles can provide harassment and scouting advantages while you build a mixed composition.

**Read for full checks:** `N004`

## Decision Nodes

### [DEFAULT] N001 — Early-Mid Ground Development

**Trigger situation:**  
At around 4 minutes, both players are in early-midgame with heavy economy and technology, and the opponent shows a ground posture with Stalker cues.

**Direction:**  
Strengthen ground forces while increasing economy and expansion. Maintain defense and continue production.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Consolidation

**Trigger situation:**  
At around 8 minutes, both players have heavy economies and technology, with the opponent showing a ground posture including Zealots, Stalkers, Sentries, and Immortals.

**Direction:**  
Continue strengthening ground forces and maintain economy and expansion. Keep technology development ongoing.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Late-Mid Ground Stability

**Trigger situation:**  
At around 10 minutes, the opponent remains ground-focused with a moderate defense, and you have a heavy economy and expansion.

**Direction:**  
Maintain ground strength and economy, with a focus on defense and continued technology development.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early-Mid Mixed Transition

**Trigger situation:**  
At around 5 minutes, the opponent shows a ground posture with Stalkers, but you have a mixed army with Oracles and a heavy economy.

**Direction:**  
Increase air presence and strengthen air forces while continuing economy and technology development.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game Ground Foundation

**Trigger situation:**  
At around 3 minutes, both players are in early game with unknown army postures, but you have Zealots and Stalkers.

**Direction:**  
Strengthen ground forces while increasing economy and technology. Maintain defense and continue production.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early-Mid Air Mirror

**Trigger situation:**  
At around 6 minutes, both players have air-oriented armies with Phoenixes and Oracles, and heavy economies.

**Direction:**  
Maintain air presence and strengthen ground forces as a complement. Continue economy and technology development.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early Game Defensive Development

**Trigger situation:**  
At around 3 minutes, the opponent has a heavy defense posture and moderate economy, while you have a Stalker and heavy economy.

**Direction:**  
Stabilize your economy and defense while increasing production and technology. Maintain ground strength.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Ground vs Air

**Trigger situation:**  
At around 9 minutes, the opponent has a heavy air army with Carriers and Void Rays, while you have a ground army with Zealots, Stalkers, Sentries, and Warp Prisms.

**Direction:**  
Strengthen ground forces and consider adding anti-air capabilities. Maintain economy and expansion.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Air Transition

**Trigger situation:**  
At around 9 minutes, the opponent has a ground army with Stalkers, Sentries, Observers, and Oracles, while you have an air army with Phoenixes.

**Direction:**  
Increase air presence and strengthen air forces. Continue economy and technology development.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Late-Mid Ground Defense vs Air

**Trigger situation:**  
At around 10 minutes, the opponent has a heavy air army with Carriers and Void Rays, while you have a ground army with Stalkers, Sentries, Void Rays, and Observers.

**Direction:**  
Increase defense and strengthen ground forces while adding anti-air. Continue economy and technology development.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early-Mid Ground Development (Unknown Opponent)

**Trigger situation:**  
At around 5 minutes, the opponent's posture is unknown, but you have a ground army with Stalkers and a heavy economy.

**Direction:**  
Strengthen ground forces while increasing economy and technology. Maintain defense and continue production.

**Read for details:** `N011`

---
