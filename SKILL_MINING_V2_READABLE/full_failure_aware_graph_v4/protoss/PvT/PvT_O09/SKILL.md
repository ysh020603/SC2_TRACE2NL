# PvT_O09 Technology / Economy / Production

## Skill Identity

- Skill ID: PvT_O09
- Matchup: Protoss vs Terran
- Opening Family: technology / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Protoss opening that emphasizes heavy technology and economy while maintaining moderate production, aiming for a flexible midgame with a ground-leaning army.

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

**When:** At any time, if bank (minerals+gas) exceeds 800 and active production structures (gateways, stargates, robotics facilities) are fewer than 3, or if any production structure is idle with no queued units.

**Correction:** Queue units from existing production structures, prioritizing gateway units (Zealots, Stalkers, or Adepts) to maintain a ground-leaning army. If prerequisites allow, add one production structure (e.g., Gateway) to increase output. Do not expand or add tech structures until bank is below 400 and production is active.

**Recheck:** Recheck at next decision cycle: confirm bank is below 400 and all production structures have at least one queued unit.

### R02 — Enemy Composition Response

**When:** If Enemy Intelligence reveals a Terran ground-heavy composition with heavy tech (e.g., Siege Tanks, Marauders, or Thors) and moderate air presence (e.g., Vikings or Medivacs), and your army supply is below 30.

**Correction:** Prioritize producing Immortals and Stalkers to counter armored ground units, and add a few Phoenixes or Void Rays if air threats are confirmed. Ensure a Robotics Facility is available or under construction; if not, build one. Maintain current expansion count and do not over-extend economy.

**Recheck:** Recheck at next decision cycle: confirm army supply is above 30 and composition includes at least 2 Immortals or 4 Stalkers, with detection if needed.

### R03 — Recovery from Low Army and High Bank

**When:** If army supply is below 15 and bank exceeds 1000, or if predicted advantage is OverwhelmingDisadvantage, or if any owned base is threatened.

**Correction:** Immediately convert bank into army by queueing units from all available production structures, prioritizing Zealots and Stalkers for ground defense. If production is insufficient, build additional Gateways (up to 4 total) and warp in units. Do not expand or add tech structures until army supply is above 25 and bank is below 500.

**Recheck:** Recheck at next decision cycle: confirm army supply is above 25 and bank is below 500, and no owned base is under threat.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid passive ground buildup

**When:** Late midgame, heavy economy and production, facing Terran ground with heavy tech and moderate air.

**Mistake → correction:** Passively strengthening ground and tech without pushing or scouting, allowing the enemy to amass a large force. → Continue strengthening ground army and tech, but maintain defense and consider adding tech units to prepare for a decisive engagement.

**Why:** Your heavy economy supports both army and tech, giving you an advantage if you stay active and ready.

**Read for full checks:** `N003`

### L02 — Avoid over-committing to tech without scouting

**When:** Early game, heavy economy, moderate production, facing Terran with unknown posture but heavy tech.

**Mistake → correction:** Over-committing to a specific tech path without scouting, risking vulnerability to early pressure or wrong composition. → Focus on increasing economy and production while developing technology, and maintain current expansion to prepare for midgame.

**Why:** A strong economy and tech foundation early pays off, and the Terran's heavy tech suggests strong units you need to match.

**Read for full checks:** `N004`

### L03 — Avoid over-extending economy without defense

**When:** Early midgame, heavy economy and production, facing Terran ground with heavy tech.

**Mistake → correction:** Over-extending economy without proper defense, leaving you vulnerable to harassment like Reapers. → Increase economy and production, continue strengthening ground army, and consider expanding while maintaining current defense.

**Why:** Investing in tech and economy now gives a strong midgame, and you need to match the Terran's heavy tech.

**Read for full checks:** `N002`

## Decision Nodes

### [DEFAULT] N001 — Midgame Ground Macro Development

**Trigger situation:**  
Reaching the midgame with a heavy economy and production, facing a Terran ground posture with heavy tech.

**Direction:**  
Continue developing your ground army and technology, while increasing production and economy. Maintain your current expansion count and keep a watchful eye on defense.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Midgame Ground Tech Investment

**Trigger situation:**  
In the early-midgame, with a heavy economy and production, facing a Terran ground posture with heavy tech.

**Direction:**  
Increase your economy and production, continue strengthening your ground army, and consider expanding to secure more resources. Maintain your current defense.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Late-Midgame Ground Army Reinforcement

**Trigger situation:**  
In the late-midgame, with a heavy economy and production, facing a Terran ground posture with heavy tech and moderate air presence.

**Direction:**  
Continue strengthening your ground army and technology, while maintaining your economy and production. Keep your defense solid and consider adding more tech units.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early Game Tech and Economy Foundation

**Trigger situation:**  
In the early game, with a heavy economy and moderate production, facing a Terran with unknown posture but heavy tech.

**Direction:**  
Focus on increasing your economy and production, while continuing to develop your technology. Maintain your current expansion and prepare for the midgame.

**Read for details:** `N004`

---
