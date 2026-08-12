# ZvP_O07 Economy / Production / Expansion

## Skill Identity

- Skill ID: ZvP_O07
- Matchup: Zerg vs Protoss
- Opening Family: economy / production / expansion opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg opening that prioritizes economy, production, and expansion while maintaining a ground-oriented army. The strategy is flexible and adapts to opponent observations.

Develop a strong economy and production base while preserving flexibility to respond to Protoss tech choices.

This is a strategic template, not a fixed build order.

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

### R01 — Production Tempo with Economy Focus

**When:** Time between 240 and 360 seconds, workers below 35, army supply below 5, bank above 2000, and production structures fewer than 3.

**Correction:** Prioritize building additional production structures (e.g., Hatcheries) up to at least 3, while continuing to produce workers. If bank remains high after reaching 3 production structures, spend excess on additional Queens or Zerglings to convert resources into army. Do not expand further until production is sufficient and army supply is at least 15.

**Recheck:** At next decision cycle, verify production structures count is at least 3, workers are above 35, and bank is below 2000. If not, repeat the correction.

### R02 — Anti-Air Response to Protoss Air Composition

**When:** Enemy Intelligence indicates air units (e.g., Void Rays, Phoenixes, Oracles) and current anti-air capability is insufficient (e.g., no Hydralisks or Spore Crawlers).

**Correction:** Add anti-air units and structures: build a Spire if not already present, then produce Mutalisks or Corruptors; also consider Spore Crawlers at bases. Ensure at least 2 Spore Crawlers per base if air threat is severe. Maintain ground army production to avoid overcommitting to air.

**Recheck:** At next decision cycle, verify anti-air units or structures are present and sufficient to counter the observed air composition. If not, continue producing anti-air.

### R03 — Recovery from Low Army and High Bank

**When:** Army supply below 15, bank above 3000, and predicted advantage is OverwhelmingDisadvantage or threat flags indicate imminent attack.

**Correction:** Immediately convert bank into army: produce combat units from all available production structures, prioritizing Zerglings and Roaches for ground defense. If production structures are insufficient, build additional Hatcheries. Do not expand or tech until army supply is at least 15 and bank is below 2000. Use larva efficiently to maximize unit production.

**Recheck:** At next decision cycle, verify army supply is at least 15 and bank is below 2000. If not, continue producing army and building production structures.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid over-expanding without army support

**When:** Early game, around 180 seconds, when you have a heavy economy and expansion but light production and tech, and opponent's posture is unknown.

**Mistake → correction:** Continuing to expand and strengthen ground army without first building up production and scouting, leaving you vulnerable to early aggression. → Focus on economy and expansion, but start building up production and army. Maintain a defensive posture.

**Why:** Your economy is strong, so you can afford to expand and tech. The opponent's unknown posture means you should be cautious.

**Read for full checks:** `N002`

### L02 — Avoid blind teching without scouting

**When:** Early midgame, around 240 seconds, when you have a heavy economy and expansion but light production and tech, and opponent's posture is unknown.

**Mistake → correction:** Increasing economy and tech without scouting, potentially leaving you unprepared for the opponent's strategy and neglecting army production. → Increase your economy and tech, while maintaining your production and expansion. Keep a defensive posture.

**Why:** Your economy is strong, so you can invest in tech. The opponent's unknown posture means you should be cautious.

**Read for full checks:** `N004`

### L03 — Avoid neglecting ground defense against air-heavy opponent

**When:** Midgame, around 540 seconds, when you have a heavy economy, production, expansion, and tech, and opponent has an air posture with heavy production and tech.

**Mistake → correction:** Continuing to strengthen ground army and expand without adding anti-air, leaving you vulnerable to the opponent's air units. → Increase your economy, production, and expansion, while continuing to develop your ground army. Consider adding anti-air.

**Why:** The opponent's air threat requires a response, so you need to prepare anti-air while maintaining your economy.

**Read for full checks:** `N008`

## Decision Nodes

### [DEFAULT] N001 — Early-Midgame Ground Development

**Trigger situation:**  
At around 300 seconds, you have a heavy economy and expansion, with moderate production and light tech. The opponent shows a ground posture with heavy production and tech.

**Direction:**  
Continue developing your economy and production, strengthen your ground army, and maintain your expansion. Keep an eye on potential pressure.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early Game Economy Focus

**Trigger situation:**  
At around 180 seconds, you have a heavy economy and expansion, but your production and tech are light. The opponent's posture is unknown, but they have heavy defense and tech.

**Direction:**  
Focus on economy and expansion, while starting to build up your production and army. Maintain a defensive posture.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Army Strengthening

**Trigger situation:**  
At around 480 seconds, you have a heavy economy, production, and expansion, with moderate tech. The opponent has a ground posture with heavy production and tech.

**Direction:**  
Strengthen your ground army and continue to develop your economy and tech. Maintain your defense.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early-Midgame Economy and Tech Expansion

**Trigger situation:**  
At around 240 seconds, you have a heavy economy and expansion, but light production and tech. The opponent's posture is unknown, but they have heavy economy and tech.

**Direction:**  
Increase your economy and tech, while maintaining your production and expansion. Keep a defensive posture.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Tech and Army Investment

**Trigger situation:**  
At around 480 seconds, you have a heavy economy, production, and expansion, with heavy tech. The opponent has a ground posture with heavy production and tech.

**Direction:**  
Increase your economy, production, and tech, while continuing to expand. Strengthen your ground army.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Late-Midgame Ground Army Consolidation

**Trigger situation:**  
At around 600 seconds, you have a heavy economy, production, and expansion, with heavy tech. The opponent has a ground posture with heavy production and tech.

**Direction:**  
Maintain your economy, production, and tech, while continuing to strengthen your ground army. Keep your defense.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Midgame Air Threat Response

**Trigger situation:**  
At around 420 seconds, you have a heavy economy and production, with moderate tech. The opponent has an air posture with heavy production and tech.

**Direction:**  
Increase your defense and economy, while continuing to develop your ground army. Consider adding anti-air units.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Air Pressure and Expansion

**Trigger situation:**  
At around 540 seconds, you have a heavy economy, production, and expansion, with heavy tech. The opponent has an air posture with heavy production and tech.

**Direction:**  
Increase your economy, production, and expansion, while continuing to develop your ground army. Consider adding anti-air.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Ground Army Development

**Trigger situation:**  
At around 420 seconds, you have a heavy economy, production, and expansion, with heavy tech. The opponent has a ground posture with heavy production and tech.

**Direction:**  
Increase your economy, production, and expansion, while continuing to develop your ground army. Keep your defense.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Midgame Air Transition

**Trigger situation:**  
At around 540 seconds, you have a heavy economy, production, and expansion, with moderate tech. The opponent has a ground posture with heavy production and tech.

**Direction:**  
Increase your air presence and tech, while continuing to develop your economy and expansion. Strengthen your air army.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early-Midgame Tech Investment

**Trigger situation:**  
At around 360 seconds, you have a heavy economy and expansion, with moderate production and heavy tech. The opponent has a ground posture with heavy production and tech.

**Direction:**  
Increase your economy and tech, while continuing to develop your production and expansion. Strengthen your ground army.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Early-Midgame Air Threat Response

**Trigger situation:**  
At around 360 seconds, you have a heavy economy and expansion, with heavy production and moderate tech. The opponent has an air posture with heavy production and tech.

**Direction:**  
Increase your economy, production, and expansion, while continuing to develop your ground army. Consider adding anti-air.

**Read for details:** `N012`

---
