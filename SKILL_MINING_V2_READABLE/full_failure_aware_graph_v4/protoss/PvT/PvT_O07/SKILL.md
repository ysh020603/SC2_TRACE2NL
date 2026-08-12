# PvT_O07 Technology / Economy / Production

## Skill Identity

- Skill ID: PvT_O07
- Matchup: Protoss vs Terran
- Opening Family: technology / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Protoss opening that emphasizes heavy technology and economy investment while maintaining moderate production, aiming for a flexible mid-game transition.

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

### R01 — Maintain tech-economy tempo with production scaling

**When:** Before 360 seconds, with heavy economy and technology investment, and production below 3 active structures or army supply below 15 while bank exceeds 800.

**Correction:** Prioritize adding production structures (Gateways or Robo) up to at least 3 active production facilities, and queue units to keep them busy. Convert excess minerals into additional production or tech prerequisites, but do not delay worker saturation. If supply is below 15, build army units from existing production before expanding.

**Recheck:** At next decision cycle, verify production count is at least 3 and army supply is above 15 or bank is below 800.

### R02 — Counter Terran ground composition with tech and air support

**When:** When enemy intelligence reveals a ground-heavy composition including Marines, Marauders, Reapers, Hellions, or Siege Tanks, and you have a ground-leaning army with access to Stargate.

**Correction:** Add Void Rays from Stargate if the enemy lacks anti-air, while continuing to strengthen your ground army with Immortals or Colossus to handle armored units. Ensure detection is available if Widow Mines or Banshees are present. Keep production and technology advancing to support both ground and air units.

**Recheck:** At next decision cycle, confirm you have at least 2 Void Rays or equivalent air support, and detection if needed, while maintaining ground production.

### R03 — Recover from low army and high bank with urgent production

**When:** When army supply is below 15, bank exceeds 1500, and predicted advantage is OverwhelmingDisadvantage or threat flags are high.

**Correction:** Immediately convert bank into army by queuing units from all available production structures, prioritizing combat units over economy. If production is insufficient, add production structures first, then queue units. Do not expand or tech greedily until army supply is above 15 and bank is below 1000.

**Recheck:** At next decision cycle, verify army supply is above 15 and bank is below 1000, or production is actively building units.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid blind teching without scouting

**When:** Early game around 180 seconds, when you have heavy economy and technology investment but unknown enemy composition, with possible Reapers and Marines.

**Mistake → correction:** Assuming the enemy's build without scouting and neglecting defense while teching. → Focus on increasing production and technology while maintaining a safe economy. Scout to clarify the opponent's intentions.

**Why:** Early game is about establishing a strong foundation. Heavy technology investment can pay off later, but you need to be aware of potential early pressure.

**Read for full checks:** `N002`

### L02 — Leverage Void Rays against ground-heavy enemy

**When:** Late midgame around 600 seconds, when you have a ground-oriented army with Void Rays and the opponent shows a ground posture with Marines, Reapers, Marauders, and Hellions.

**Mistake → correction:** Neglecting ground defense and failing to exploit your air advantage. → Continue strengthening your ground army while maintaining air support from Void Rays. Increase production and technology, and consider adding more air units if the opponent lacks anti-air.

**Why:** The opponent's ground army is strong, but your Void Rays provide an advantage if they lack anti-air. You can leverage this to gain map control.

**Read for full checks:** `N004`

### L03 — Prepare for bio-based army while expanding

**When:** Early game around 180 seconds, when you have an unknown army composition, heavy economy, and are expanding, while the opponent shows a ground posture with Marines and Marauders.

**Mistake → correction:** Over-committing to defense at the expense of economy and neglecting scouting for tech switches or all-ins. → Focus on increasing production and technology while maintaining a safe economy. Scout to confirm the opponent's build.

**Why:** The opponent's ground posture with Marines and Marauders suggests a bio-based army. You need to prepare for that with appropriate units and upgrades.

**Read for full checks:** `N005`

## Decision Nodes

### [DEFAULT] N001 — Early-Mid Transition with Ground Focus

**Trigger situation:**  
At around 300 seconds, you have a ground-oriented army with Stalkers, while the opponent shows a ground posture with Marines and Widow Mines. Your economy and production are heavy, and you are expanding.

**Direction:**  
Continue strengthening your ground army while increasing production and technology. Maintain your economy and expansion pace, and keep defense at a moderate level.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early Game Tech and Economy Development

**Trigger situation:**  
At around 180 seconds, both you and the opponent have unknown army compositions, but you have a heavy economy and technology investment. The opponent shows possible Reapers and Marines.

**Direction:**  
Focus on increasing production and technology while maintaining a safe economy. Consider scouting to clarify the opponent's intentions.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Army Strengthening

**Trigger situation:**  
At around 480 seconds, you have a ground-oriented army with heavy production and technology. The opponent shows a ground posture with Siege Tanks, Marines, and Banshees.

**Direction:**  
Strengthen your ground army and consider adding units that can handle Siege Tanks, such as Immortals or Void Rays. Increase production and technology further.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late Midgame Ground and Air Flexibility

**Trigger situation:**  
At around 600 seconds, you have a ground-oriented army with Void Rays, while the opponent shows a ground posture with Marines, Reapers, Marauders, and Hellions.

**Direction:**  
Continue strengthening your ground army while maintaining air support from Void Rays. Increase production and technology, and consider adding more air units if the opponent lacks anti-air.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game Ground Posture with Heavy Economy

**Trigger situation:**  
At around 180 seconds, you have an unknown army composition, but the opponent shows a ground posture with Marines and Marauders. Your economy is heavy, and you are expanding.

**Direction:**  
Focus on increasing production and technology while maintaining a safe economy. Consider scouting to confirm the opponent's build.

**Read for details:** `N005`

---
