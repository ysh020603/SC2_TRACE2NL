# ZvP_O03 Economy / Expansion / Upgrade

## Skill Identity

- Skill ID: ZvP_O03
- Matchup: Zerg vs Protoss
- Opening Family: economy / expansion / upgrade opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg opening focused on heavy economy and expansion while maintaining a ground-oriented army. The build is flexible, allowing adaptation to Protoss tech choices.

Develop a strong economy and expansion lead while preserving flexibility for live observation-driven adaptation.

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

### R01 — Maintain production tempo and convert bank into army

**When:** At any time, if bank is above 2500 minerals and 500 gas, or if active production structures are fewer than 3 and army supply is below 30, or if supply is not blocked and larvae are available.

**Correction:** Spend bank on additional Hatcheries or tech structures if prerequisites are met, and queue units from all Hatcheries. Prioritize Zerglings and Roaches to keep ground army strength. Do not expand unless army supply is at least 15 and production is sufficient.

**Recheck:** Next decision cycle, verify bank is below 1500 minerals and 300 gas, and that active production structures are at least 3 or army supply has increased by at least 10.

### R02 — Adapt to Protoss air or ground composition

**When:** If enemy intelligence reveals a significant air presence (e.g., Void Rays, Oracles, Phoenixes) or a heavy ground composition with Stalkers and Sentries, and your army lacks appropriate counters.

**Correction:** If air threat is detected, tech to Spire and start producing Mutalisks or Corruptors while maintaining ground forces. If ground heavy, ensure Roach Warren is available and produce Roaches. Continue expanding and upgrading to keep pace with enemy tech.

**Recheck:** Next decision cycle, confirm that anti-air or anti-ground units are in production or queued, and that your tech structures are progressing.

### R03 — Recover from low army and high bank

**When:** If army supply is below 15 and bank is above 2000 minerals, or if predicted advantage is OverwhelmingDisadvantage, or if any owned base is threatened.

**Correction:** Immediately spend bank on army production: queue Zerglings and Roaches from all Hatcheries, and if possible, add a Spine Crawler at threatened bases. Do not expand or tech up until army supply is at least 30 and threat is mitigated.

**Recheck:** Next decision cycle, verify army supply has increased by at least 10 and bank is below 1000 minerals, or threat flags are cleared.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Keep pace with opponent's tech while maintaining ground strength

**When:** Midgame, around 480 seconds, when you have a ground army with Zerglings and Queens, heavy production but moderate technology, and the opponent shows a ground posture with Stalkers, Sentries, and Warp Prisms.

**Mistake → correction:** Focusing solely on strengthening your ground army and continuing economy without advancing your technology, risking falling behind in tech and being vulnerable to warp prism harass. → Maintain your current production and economy, and continue developing your technology. Keep your ground army strong.

**Why:** The opponent's heavy tech and production require you to keep pace. Maintaining a solid economy and production will allow you to tech up without falling behind.

**Read for full checks:** `N004`

### L02 — Balance economy, tech, and ground strength in late midgame

**When:** Late midgame, around 600-720 seconds, when you have a ground army with Zerglings, Roaches, and Queens, heavy production and technology, and the opponent shows a ground posture with Zealots, Stalkers, and Sentries.

**Mistake → correction:** Neglecting economy or upgrades, or overcommitting to a single attack if the opponent is defending well, while only focusing on strengthening ground forces. → Increase your economy and technology, continue expanding and producing. Strengthen your ground army further.

**Why:** The opponent's composition is strong on the ground, so you need to maintain a powerful ground force and tech to counter their upgrades.

**Read for full checks:** `N005`

### L03 — Prepare anti-air while maintaining ground and economy

**When:** Midgame, around 420 seconds, when you have a ground army with Zerglings, Roaches, and Queens, moderate production but heavy technology, and the opponent shows an air posture with Void Rays and Oracles.

**Mistake → correction:** Ignoring the air threat and overcommitting to ground units without anti-air support, while focusing on strengthening ground and increasing economy. → Increase your economy and technology, continue expanding and producing. Strengthen your ground army and prepare for air threats.

**Why:** The opponent's air composition requires you to tech into anti-air units while maintaining a strong economy.

**Read for full checks:** `N010`

## Decision Nodes

### [DEFAULT] N001 — Early-Midgame Ground Macro with Heavy Economy

**Trigger situation:**  
At around 300-360 seconds, you have a ground-oriented army with Zerglings and Queens, moderate production, and a heavy economy. The opponent shows a ground posture with Zealots and Sentries, heavy production and technology.

**Direction:**  
Strengthen your ground army while increasing your economy. Maintain your current expansion and production, and continue technology development.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Midgame Ground Macro with Unknown Opponent

**Trigger situation:**  
At around 240 seconds, you have a ground-oriented army with Zerglings and Queens, moderate production, and a heavy economy. The opponent's army is unknown, but they have a heavy economy and expansions.

**Direction:**  
Continue strengthening your ground army and maintain your economy. Keep production and technology at current levels.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Macro with Heavy Tech

**Trigger situation:**  
At around 480-540 seconds, you have a ground army with Zerglings, Roaches, and Queens, heavy production and technology. The opponent shows a ground posture with Stalkers, Sentries, and Warp Prisms.

**Direction:**  
Increase your economy and technology, continue expanding and producing. Strengthen your ground army further.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground Macro with Moderate Tech

**Trigger situation:**  
At around 480 seconds, you have a ground army with Zerglings and Queens, heavy production but moderate technology. The opponent shows a ground posture with Stalkers, Sentries, and Warp Prisms.

**Direction:**  
Maintain your current production and economy, and continue developing your technology. Keep your ground army strong.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Late-Midgame Ground Macro with Heavy Tech

**Trigger situation:**  
At around 600-720 seconds, you have a ground army with Zerglings, Roaches, and Queens, heavy production and technology. The opponent shows a ground posture with Zealots, Stalkers, and Sentries.

**Direction:**  
Increase your economy and technology, continue expanding and producing. Strengthen your ground army further.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early Game Ground Macro with Heavy Economy

**Trigger situation:**  
At around 180 seconds, you have a ground-oriented army with Zerglings and Queens, moderate production, and a heavy economy. The opponent's army is unknown, but they have a heavy economy and moderate expansions.

**Direction:**  
Increase your economy and expansions, and continue developing your ground army and technology.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Late-Midgame Ground Macro with Moderate Tech

**Trigger situation:**  
At around 600 seconds, you have a ground army with Zerglings, Roaches, and Queens, heavy production but moderate technology. The opponent shows a ground posture with Zealots and Carriers.

**Direction:**  
Maintain your current production and economy, and continue developing your technology. Keep your ground army strong.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early-Midgame Ground Macro with Heavy Economy

**Trigger situation:**  
At around 240 seconds, you have a ground-oriented army with Zerglings and Queens, moderate production, and a heavy economy. The opponent's army is unknown, but they have a heavy economy and expansions.

**Direction:**  
Increase your economy and expansions, and continue developing your ground army and technology. Increase production.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Ground Macro with Moderate Tech

**Trigger situation:**  
At around 420 seconds, you have a ground army with Zerglings and Queens, moderate production and technology. The opponent shows a ground posture with Stalkers and Sentries.

**Direction:**  
Increase your economy and expansions, and continue developing your ground army and technology. Increase production.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Midgame Ground Macro vs Air Posture

**Trigger situation:**  
At around 420 seconds, you have a ground army with Zerglings, Roaches, and Queens, moderate production but heavy technology. The opponent shows an air posture with Void Rays and Oracles.

**Direction:**  
Increase your economy and technology, continue expanding and producing. Strengthen your ground army and prepare for air threats.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early-Midgame Ground Macro with Moderate Tech

**Trigger situation:**  
At around 360 seconds, you have a ground army with Zerglings and Queens, moderate production and technology. The opponent shows a ground posture with Zealots and Sentries.

**Direction:**  
Increase your economy and expansions, and continue developing your ground army and technology. Increase production.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Early-Midgame Ground Macro vs Air Posture

**Trigger situation:**  
At around 300 seconds, you have a ground army with Zerglings and Queens, moderate production, and a heavy economy. The opponent shows an air posture with Oracles.

**Direction:**  
Maintain your current production and economy, and continue developing your ground army. Keep your technology at current levels.

**Read for details:** `N012`

---
