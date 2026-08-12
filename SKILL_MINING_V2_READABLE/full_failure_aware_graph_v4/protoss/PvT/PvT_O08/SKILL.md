# PvT_O08 Technology / Economy / Production

## Skill Identity

- Skill ID: PvT_O08
- Matchup: Protoss vs Terran
- Opening Family: technology / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Protoss opening that emphasizes heavy technology and economy while maintaining a moderate production base, aiming for a flexible ground-oriented midgame.

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

### R01 — Production Tempo and Bank Conversion

**When:** At any time, if bank is above 800 minerals and 400 gas, or if active production structures are fewer than 3 by 5 minutes, or fewer than 4 by 6 minutes.

**Correction:** Prioritize adding Gateways (or Robo/Stargate if tech prerequisites are met) to reach at least 3 production structures by 5 minutes and 4 by 6 minutes. Queue units from existing structures before adding new ones. Convert excess bank into army and production, not expansions, unless army supply is at least 15 and no severe disadvantage.

**Recheck:** Recheck at next decision cycle.

### R02 — Enemy Composition Response

**When:** If enemy intelligence shows a ground-heavy composition with Marines and Marauders, or Siege Tanks and Marines, and own army lacks adequate splash or anti-armor.

**Correction:** Strengthen ground army by adding Immortals for anti-armor and Sentries for force fields. If enemy shows potential air transition, add Phoenixes for map control and air defense. Continue increasing production and tech to support these units.

**Recheck:** Recheck at next decision cycle.

### R03 — Recovery from Low Army and High Bank

**When:** If army supply is below 15 and bank is above 1000 minerals, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately convert bank into army by queuing units from all available production structures. If production is insufficient, add Gateways (or tech structures if prerequisites are met) to increase output. Do not expand or tech greedily until army supply is at least 15 and the disadvantage is mitigated.

**Recheck:** Recheck at next decision cycle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Air Transition

**When:** Late midgame (~10 min) with own ground army including Zealots, Stalkers, Sentries, and Immortals; opponent shows ground posture with Siege Tanks, Marines, Reapers, Hellions, heavy production and tech.

**Mistake → correction:** Being too passive and neglecting air defense if opponent transitions to air. → Maintain and strengthen your ground army, continue increasing production and tech. Consider adding Phoenixes for map control and to handle any air transitions.

**Why:** Immortals counter Siege Tanks, Sentries provide shields, and Phoenixes offer mobility and scouting. This composition is robust against ground pushes.

**Read for full checks:** `N003`

### L02 — Splash vs Marine-heavy

**When:** Midgame (~9 min) with own ground army including Zealots, Stalkers, Sentries, and Immortals; opponent shows ground posture with Marines and Marauders, heavy production and tech.

**Mistake → correction:** Being caught without splash against Marine-heavy armies and neglecting scouting for tech switches. → Continue strengthening your ground army, increase production and tech. Use Sentries for force fields and Immortals for tanky units. Maintain economy and expansion.

**Why:** Marauders are strong against armored, but Immortals and Stalkers can handle them. Sentries provide utility.

**Read for full checks:** `N004`

### L03 — Economy vs Defense

**When:** Early-midgame (~5-6 min) with own ground army including Zealots and Stalkers, heavy production and tech; opponent shows ground posture with Siege Tanks and Marines, heavy economy and production.

**Mistake → correction:** Over-extending your economy without proper defense, as Reaper harassment can punish that. → Continue strengthening your ground army and increasing production and tech. Maintain economy growth and keep defense up. Consider adding Sentries or Immortals for utility.

**Why:** Siege Tanks require careful engagement; a mix of Stalkers for mobility and Zealots for tanking, plus Sentry shields, can handle ground pushes.

**Read for full checks:** `N002`

## Decision Nodes

### [DEFAULT] N001 — Early Game Tech/Economy Foundation

**Trigger situation:**  
Early game (~3 min) with own ground-oriented macro posture, moderate production, heavy tech; opponent shows ground posture with heavy production and economy, possible pressure.

**Direction:**  
Continue developing your technology and economy while strengthening your ground army. Increase production and tech, maintain defense, and keep expansion options open.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Midgame Ground Reinforcement

**Trigger situation:**  
Early-midgame (~5-6 min) with own ground army including Zealots and Stalkers, heavy production and tech; opponent shows ground posture with Siege Tanks and Marines, heavy economy and production.

**Direction:**  
Continue strengthening your ground army and increasing production and tech. Maintain economy growth and keep defense up. Consider adding Sentries or Immortals for utility.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Late-Midgame Ground Army Consolidation

**Trigger situation:**  
Late-midgame (~10 min) with own ground army including Zealots, Stalkers, Sentries, and Immortals; opponent shows ground posture with Siege Tanks, Marines, Reapers, Hellions, heavy production and tech.

**Direction:**  
Maintain and strengthen your ground army, continue increasing production and tech. Consider adding Phoenixes for map control and to handle any air transitions.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground Army with Immortals

**Trigger situation:**  
Midgame (~9 min) with own ground army including Zealots, Stalkers, Sentries, and Immortals; opponent shows ground posture with Marines and Marauders, heavy production and tech.

**Direction:**  
Continue strengthening your ground army, increase production and tech. Use Sentries for force fields and Immortals for tanky units. Maintain economy and expansion.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game Tech Focus with Unknown Opponent

**Trigger situation:**  
Early game (~3 min) with own ground-oriented posture, moderate production, heavy tech; opponent posture is unknown but shows Marines, heavy economy, moderate production, heavy tech.

**Direction:**  
Continue developing your tech and economy while maintaining a flexible ground army. Increase production and tech, and keep scouting to clarify opponent's intentions.

**Read for details:** `N005`

---
