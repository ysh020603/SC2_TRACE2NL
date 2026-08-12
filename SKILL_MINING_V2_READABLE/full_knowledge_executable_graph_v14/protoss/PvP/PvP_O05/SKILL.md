# PvP_O05 Technology / Economy / Expansion

## Skill Identity

- Skill ID: PvP_O05
- Matchup: Protoss vs Protoss
- Opening Family: technology / economy / expansion opening
- Method: Knowledge-Constrained Executable Full V14

## Opening Strategy

A Protoss versus Protoss opening that emphasizes heavy technology investment, a strong economy, and expansion while keeping production moderate early. The strategic template is flexible, allowing adaptation to either a ground or air transition based on live observations.

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

**When:** Early to midgame, both players have heavy economy and tech, own army composition unclear, no reliable enemy combat-unit cues, and production is below 3 active warpgates or robotics facilities.

**Correction:** Prioritize completing tech structures (Twilight Council, Robotics Facility, or Stargate) and keep probes producing toward saturation. Add one production structure if bank exceeds 400 minerals and 200 gas, and ensure warpgate cooldowns are used by warping in a round of gateway units. Do not expand beyond your natural until army supply is at least 15 and production is active.

**Recheck:** At next decision cycle, verify that production count has increased if bank was high, and that worker count is progressing toward 2 per mineral line and 3 per gas geyser.

### R02 — Counter enemy composition with tech-appropriate units

**When:** Enemy intelligence reveals a clear composition: if opponent shows Zealot-heavy ground, or Stalker/Sentry with Warp Prism and Observer, or air units like Oracle/Void Ray/Carrier, and own army lacks appropriate counters or detection.

**Correction:** If opponent is Zealot-heavy, add Immortals and keep Stalkers for support. If opponent shows Stalker/Sentry with Warp Prism and Observer, ensure you have Observers for detection and add Immortals. If opponent has air units, produce Stalkers or Phoenixes for anti-air, and consider a Stargate if not already present. Maintain economy and production while adapting.

**Recheck:** At next decision cycle, confirm that your army composition includes the required counter units and that detection is available if the opponent has cloaked or invisible units.

### R03 — Recover from low army and high bank with immediate production

**When:** Army supply is below 15, bank exceeds 1000 minerals and 500 gas, or predicted advantage is OverwhelmingDisadvantage, and production is idle or insufficient.

**Correction:** Immediately convert bank into army by warping in units from all available gateways and queuing production from robotics or stargate. If production is insufficient, add one production structure (gateway or robotics facility) without expanding. Prioritize units that counter the enemy's known composition. Do not spend on technology or expansions until army supply is above 15 and production is active.

**Recheck:** At next decision cycle, verify that army supply has increased, bank is reduced, and production is no longer idle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid neglecting detection or anti-air when both sides are heavy ground

**When:** Midgame, both sides have heavy ground armies and heavy tech. Own army includes Stalkers and Immortals, opponent shows Zealot cues.

**Mistake → correction:** Continuing to strengthen ground and expand without ensuring detection or anti-air, risking a surprise transition to air units like Oracles or Void Rays. → Continue strengthening your ground army, adding more Immortals and supporting units. Keep expanding and increasing your economy.

**Why:** Immortals are strong against Zealot-heavy ground compositions common in PvP. Maintaining a heavy economy allows you to outproduce the opponent.

**Read for full checks:** `N002`

### L02 — Avoid over-investing in army early when opponent is unknown

**When:** Early game, both sides have heavy economy and technology, but no clear army composition yet. No reliable combat-unit cues from the opponent.

**Mistake → correction:** Making a large army investment too early, which may delay your tech and economy. → Focus on developing your economy and technology while maintaining a flexible army composition. Continue expanding and increasing production.

**Why:** In the early game, investing in tech and economy sets up a strong midgame. Keeping options open allows you to react to the opponent's first moves.

**Read for full checks:** `N003`

### L03 — Avoid being too passive when opponent has heavy ground and detection

**When:** Late-midgame, both sides have heavy ground armies and heavy tech. Own army includes Stalkers, Observers, and Immortals, opponent shows Stalker, Sentry, WarpPrism, Observer cues.

**Mistake → correction:** Being too passive, allowing the opponent to build up for a timing attack. → Continue strengthening your ground army, adding more Immortals and ensuring you have detection. Maintain your economy and expansion.

**Why:** Observers provide detection against potential cloaked units, while Immortals are strong against armored ground units. A heavy economy allows you to sustain a large army.

**Read for full checks:** `N005`

## Decision Nodes

### [DEFAULT] N001 — Early-Mid Ground Development with Heavy Tech

**Trigger situation:**  
Early-midgame phase with both sides having heavy economy and technology, but own army composition still unclear. Opponent shows a ground posture with Stalker cues.

**Direction:**  
Strengthen your ground army while continuing to develop your economy and technology. Maintain your current expansion and production.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Macro with Immortal Support

**Trigger situation:**  
Midgame phase where both sides have heavy ground armies and heavy tech. Own army includes Stalkers and Immortals, while opponent shows Zealot cues.

**Direction:**  
Continue strengthening your ground army, adding more Immortals and supporting units. Keep expanding and increasing your economy.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Game Tech and Economy Focus

**Trigger situation:**  
Early game with both sides having heavy economy and technology, but no clear army composition yet. No reliable combat-unit cues from the opponent.

**Direction:**  
Focus on developing your economy and technology while maintaining a flexible army composition. Continue expanding and increasing production.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Air Transition with Phoenix and Oracle

**Trigger situation:**  
Midgame phase where you have transitioned to an air-oriented army with Phoenix and Oracle, while the opponent remains ground-focused with Zealots.

**Direction:**  
Increase your air presence and continue strengthening your air army. Maintain your economy and expansion, and keep up production.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Late-Mid Ground Army with Observer and Immortal

**Trigger situation:**  
Late-midgame phase with both sides having heavy ground armies and heavy tech. Own army includes Stalkers, Observers, and Immortals, while opponent shows Stalker, Sentry, WarpPrism, and Observer cues.

**Direction:**  
Continue strengthening your ground army, adding more Immortals and ensuring you have detection. Maintain your economy and expansion.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Midgame Ground Army vs Mixed Opponent

**Trigger situation:**  
Midgame phase where you have a ground army with Stalkers, while the opponent shows a mixed posture with moderate air presence.

**Direction:**  
Strengthen your ground army while considering adding some anti-air capabilities. Maintain your economy and expansion.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Late-Mid Air vs Air with Carrier Threat

**Trigger situation:**  
Late-midgame phase where both sides have heavy air armies. Own army includes Phoenix and Oracle, while opponent shows Stalker and Carrier cues.

**Direction:**  
Increase your air presence and consider adding units that can counter Carriers, such as Void Rays or more Phoenixes. Maintain your economy and expansion.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Air Army vs Mixed Opponent

**Trigger situation:**  
Midgame phase where you have an air army with Phoenix and Oracle, while the opponent shows a mixed posture with moderate air presence.

**Direction:**  
Continue strengthening your air army and consider adding some ground units for defense. Maintain your economy and expansion.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Air Transition with Oracle Support

**Trigger situation:**  
Midgame phase where you have an air army with Phoenix and Oracle, while the opponent shows an air posture with Oracle cues.

**Direction:**  
Maintain your air army and consider adding more Phoenixes or Oracles. Continue developing your economy and technology.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Early-Mid Ground Development with Zealot Cues

**Trigger situation:**  
Early-midgame phase where both sides have heavy economy and technology, but own army composition is still unclear. Opponent shows Zealot cues.

**Direction:**  
Strengthen your ground army while continuing to develop your economy and technology. Maintain your current expansion and production.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early-Mid Air Transition with Phoenix

**Trigger situation:**  
Early-midgame phase where you have transitioned to an air-oriented army with Phoenix, while the opponent shows an air posture with Oracle cues.

**Direction:**  
Increase your air presence and continue strengthening your air army. Maintain your economy and expansion, and keep up production.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Midgame Ground Army with Sentry Support

**Trigger situation:**  
Midgame phase where you have a ground army with Zealots and Sentries, while the opponent shows a ground posture with no reliable combat-unit cues.

**Direction:**  
Strengthen your ground army, adding more Sentries for force fields and other support. Continue developing your economy and technology.

**Read for details:** `N012`

---
