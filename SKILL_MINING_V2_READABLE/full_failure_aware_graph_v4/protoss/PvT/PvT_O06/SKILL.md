# PvT_O06 Technology / Economy / Production

## Skill Identity

- Skill ID: PvT_O06
- Matchup: Protoss vs Terran
- Opening Family: technology / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Protoss opening that emphasizes heavy technology and economy investment while maintaining a flexible ground-oriented posture. Early game focuses on developing infrastructure and tech, with production ramping up through the midgame. The opponent is Terran, and the opening is designed to adapt based on observed enemy posture.

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

### G05 — Protoss production interpretation

- Scale Gateways or other unit-producing tech only after power, prerequisites, and production capacity are executable.

## V4 Matchup-Specific Corrections

### R01 — Maintain tech-economy tempo with early defense

**When:** Before 5 minutes, with heavy economy/tech investment, enemy shows Reaper or Marine, and army supply is below 15.

**Correction:** Prioritize a defensive structure (e.g., Shield Battery) and produce a few Zealots or Stalkers from existing Gateways while continuing worker production. Keep tech buildings (e.g., Twilight Council) progressing. If bank exceeds 300 minerals, add a Gateway or start a Warp Gate upgrade.

**Recheck:** At next decision cycle, confirm army supply is at least 10, workers are near 22-24, and no supply block is imminent.

### R02 — Counter bio with splash and upgrades

**When:** After 6 minutes, enemy composition is primarily bio (Marines, Marauders, Medivacs) with heavy ground posture, and you have at least 2 bases and 3 production structures.

**Correction:** Add Colossi or Archons to complement High Templars. Ensure Forge and Twilight upgrades are progressing. If bank is high, add Gateways and produce Zealots/Stalkers to support the tech units.

**Recheck:** At next decision cycle, verify you have at least one Colossus or Archon, and that upgrades are not idle.

### R03 — Recover from low army and high bank

**When:** Army supply is below 15, bank exceeds 1000 minerals and 500 gas, or predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately convert bank into army: queue units from all Gateways, add Gateways if production is insufficient, and prioritize combat units over economy. Do not expand. If supply is blocked, build a Pylon. If enemy has air, add Stalkers or Phoenixes.

**Recheck:** At next decision cycle, confirm army supply is above 20 and bank is reduced by at least 50%.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid neglecting upgrades and positioning while teching up

**When:** Late midgame, around 10 minutes, with heavy ground army and High Templars/Sentries, enemy ground posture with Marines/Reapers/Marauders/Medivacs and heavy defense.

**Mistake → correction:** Focusing solely on strengthening ground forces and increasing production/economy/tech without prioritizing upgrades, and being caught out of position against a potential timing attack. → Continue increasing production and technology, and consider adding Colossi or Archons to complement High Templars. Maintain economy and expansion, but ensure upgrades are kept on par and army is well-positioned.

**Why:** High Templar tech provides strong advantage against bio with Psionic Storm; Colossi/Archons add splash and tankiness. Upgrades are critical to match enemy's high attack/defense.

**Read for full checks:** `N004`

### L02 — Avoid assuming enemy build without scouting while teching

**When:** Early game, around 3 minutes, with heavy economy and tech investment, enemy shows Reaper indicating possible early harassment.

**Mistake → correction:** Assuming the enemy's build without scouting and neglecting defense while teching, leaving yourself vulnerable to early pressure. → Focus on developing economy and technology while preparing to defend against potential early pressure. Strengthen ground forces as you transition.

**Why:** Heavy tech and economy start can yield long-term advantage, but must be safe against Reaper harassment. Solid foundation now pays off later.

**Read for full checks:** `N002`

### L03 — Avoid over-extending economy without proper defense

**When:** Early midgame, around 6 minutes, with heavy economy and production, ground units like Stalkers, enemy ground posture with Marines/Reapers and heavy tech.

**Mistake → correction:** Over-extending economy and expansion without adequate defense, allowing Reaper harassment to punish. → Continue strengthening ground army and increasing production/technology. Maintain economy and expansion pace, but keep an eye on defense.

**Why:** Heavy tech and economy advantage can be leveraged to out-produce enemy. Strengthening ground forces aligns with observed enemy ground posture, preparing for engagements.

**Read for full checks:** `N001`

## Decision Nodes

### [DEFAULT] N001 — Early-Mid Transition with Ground Tech

**Trigger situation:**  
At around 6 minutes, you have a heavy economy and production, with ground units like Stalkers. Enemy shows a ground posture with Marines and Reapers, and heavy tech investment.

**Direction:**  
Continue strengthening your ground army and increasing production and technology. Maintain your economy and expansion pace, but keep an eye on defense.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early Game Tech and Economy Focus

**Trigger situation:**  
At around 3 minutes, you are in the early game with heavy economy and tech investment, but your army composition is unclear. Enemy shows a Reaper, indicating possible early harassment.

**Direction:**  
Focus on developing your economy and technology while preparing to defend against potential early pressure. Strengthen your ground forces as you transition.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Army Consolidation

**Trigger situation:**  
At around 9 minutes, you have a heavy ground army with Zealots, Stalkers, Sentries, and Warp Prisms. Enemy shows a ground posture with Marines, Reapers, Marauders, and Medivacs, indicating a bio-based army.

**Direction:**  
Continue strengthening your ground army and increasing production. Maintain your economy and expansion, and consider adding tech units like Immortals or Colossi to counter the bio army.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Tech and Army Expansion

**Trigger situation:**  
At around 10 minutes, you have a heavy ground army with High Templars and Sentries, indicating advanced tech. Enemy shows a ground posture with Marines, Reapers, Marauders, and Medivacs, with heavy defense.

**Direction:**  
Continue increasing your production and technology, and consider adding Colossi or Archons to complement your High Templars. Maintain your economy and expansion.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game Defensive Tech

**Trigger situation:**  
At around 3 minutes, you have a heavy economy and tech, but your army is undefined. Enemy shows a Marine, indicating a possible early push.

**Direction:**  
Focus on developing your economy and technology while preparing to defend against early pressure. Build a defensive structure or units to ensure safety.

**Read for details:** `N005`

---
