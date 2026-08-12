# TvP_O07 Economy / Technology / Expansion

## Skill Identity

- Skill ID: TvP_O07
- Matchup: Terran vs Protoss
- Opening Family: economy / technology / expansion opening
- Method: Opening-Champion Full V10

## Opening Strategy

A Terran opening that prioritizes a heavy economy, heavy technology investment, and early expansion while maintaining a ground-oriented army. The build is flexible and observation-driven, aiming to develop a strong macro position before committing to a specific army composition.

Develop a robust economy and technology base while preserving flexibility to adapt to the opponent's observed posture. Aim to reach a strong midgame position with multiple bases, high worker count, and access to key tech units.

This is a strategic template, not a fixed build order. Adapt based on live scouting and enemy intelligence.

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

### G05 — Terran production interpretation

- Scale Barracks/Factory/Starport capacity before ordering add-ons or units that lack a completed parent structure.

## V4 Matchup-Specific Corrections

### R01 — Production Tempo and Bank Conversion

**When:** At any time, if bank exceeds 800 minerals and 400 gas, or if active production structures are fewer than 3 and army supply is below 30, or if supply is not blocked and workers are below 30 at 5 minutes.

**Correction:** Queue units from all available production structures, prioritizing Marines and Marauders. If no production structures are available, build a Barracks with a Reactor if prerequisites allow. If supply is not blocked and workers are below 30, queue SCVs from all Command Centers. If supply is blocked, add a Supply Depot only if no supply provider is already completed, pending, or queued.

**Recheck:** Recheck at next decision cycle.

### R02 — Anti-Air Response to Enemy Air Composition

**When:** If enemy intelligence shows any of Void Rays, Phoenixes, Oracles, or other air units, and your army composition lacks sufficient anti-air (e.g., fewer than 4 Marines per 10 army supply, or no Thors/Vikings).

**Correction:** Queue additional Marines from Barracks, and if tech lab is available, start producing Thors or Vikings from Factories or Starports. If no Starport exists, build one with a Tech Lab. Ensure at least 2 anti-air units per 10 army supply.

**Recheck:** Recheck at next decision cycle.

### R03 — Recovery from Low Army and High Bank

**When:** If army supply is below 15 and bank exceeds 1000 minerals and 500 gas, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all production structures, prioritizing combat units. If production is insufficient, build additional Barracks, Factories, or Starports as resources allow. Do not expand or tech until army supply is above 15 and production is active.

**Recheck:** Recheck at next decision cycle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Anti-Air Gap vs Void Rays

**When:** Midgame, around 420 seconds, with a heavy ground army and economy, and enemy scouting shows Zealots and Void Rays.

**Mistake → correction:** Sticking to a pure ground composition without anti-air, leaving your army vulnerable to Void Rays. → Maintain your ground army and continue expanding, but add anti-air units like Marines or Thors to counter potential Void Rays.

**Why:** Your ground army is strong, but Void Rays threaten it. Adding anti-air ensures you can handle mixed compositions.

**Read for full checks:** `N005`

### L02 — Insufficient Anti-Air vs Heavy Air

**When:** Midgame, around 480 seconds, with a heavy ground army and economy, and enemy scouting shows Zealots, Stalkers, Phoenixes, and Observers.

**Mistake → correction:** Continuing to strengthen ground forces without adding anti-air, leaving you unable to fight the enemy's air-heavy army. → Increase your anti-air capabilities by adding Thors, Vikings, or more Marines, while continuing to strengthen your ground army and maintain economy.

**Why:** The opponent's air army is strong, but your heavy economy allows a tech switch to support your ground with anti-air.

**Read for full checks:** `N008`

### L03 — Overreacting to Oracles

**When:** Early-midgame, around 300 seconds, with a heavy ground army and economy, and enemy scouting shows Zealots and Oracles.

**Mistake → correction:** Over-investing in anti-air or abandoning your ground army in response to Oracle harassment. → Maintain your ground army but start preparing anti-air by adding Marines and possibly Thors or Vikings, while continuing to expand and tech.

**Why:** Oracles can harass, but your economy is strong. Adding anti-air defends against air threats without sacrificing your ground core.

**Read for full checks:** `N006`

## Decision Nodes

### [DEFAULT] N001 — Early-Midgame Ground Macro with Heavy Tech

**Trigger situation:**  
At around 240 seconds, you have a heavy economy, heavy production, and heavy tech investment. Your army is ground-oriented with Reapers. The opponent shows a ground posture with Stalkers, moderate production, and heavy tech.

**Direction:**  
Continue developing your economy and tech. Strengthen your ground army composition. Consider adding production structures to support a larger army. Maintain defensive positioning while scouting for tech switches.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Army with Air Transition

**Trigger situation:**  
At around 540 seconds, you have a heavy ground army with Siege Tanks, Marines, Reapers, and Hellions. Your economy and tech are heavy. The opponent has a ground army with Stalkers, Sentries, Observers, and Immortals, and heavy production.

**Direction:**  
Increase your air presence to gain mobility and support your ground army. Continue strengthening your ground composition. Consider adding Medivacs for healing and drops. Maintain economic growth.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Game Ground Defense and Economy

**Trigger situation:**  
At around 180 seconds, you have a moderate ground army with Marines, heavy economy, and heavy tech. The opponent shows a ground posture with Zealots, moderate production, and heavy tech.

**Direction:**  
Maintain your defensive posture while continuing to expand and tech. Strengthen your ground army with additional Marines and possibly Marauders. Keep scouting for tech switches.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Stabilization and Defense

**Trigger situation:**  
At around 600 seconds, you have a heavy ground army with Siege Tanks, Marines, and Medivacs. Your economy and tech are heavy. The opponent has a ground army with Stalkers, Sentries, Observers, and Immortals, and heavy production.

**Direction:**  
Focus on stabilizing your position. Increase defensive structures and maintain army strength. Continue economic growth but prioritize safety. Consider adding more Medivacs for sustain.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Ground Army with Medivac Support

**Trigger situation:**  
At around 420 seconds, you have a heavy ground army with Siege Tanks, Marines, Hellions, and Medivacs. Your economy and tech are heavy. The opponent shows a ground posture with Zealots and Void Rays, heavy production.

**Direction:**  
Maintain your ground army and continue to expand. Consider adding anti-air capabilities (e.g., Marines, Thors) to counter potential Void Rays. Keep scouting for further tech.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early-Midgame vs Air Posture

**Trigger situation:**  
At around 300 seconds, you have a heavy ground army with Marines. Your economy and tech are heavy. The opponent shows an air posture with Zealots and Oracles, heavy production.

**Direction:**  
Maintain your ground army but start preparing anti-air. Consider adding Marines and possibly Thors or Vikings. Continue expanding and teching.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early Game Unknown Posture

**Trigger situation:**  
At around 180 seconds, you have a moderate ground army with Marines, heavy economy, and heavy tech. The opponent's posture is unknown, with a Sentry seen, moderate production.

**Direction:**  
Continue developing your economy and tech. Maintain a defensive posture while scouting to determine the opponent's plan. Expand cautiously.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame vs Heavy Air

**Trigger situation:**  
At around 480 seconds, you have a heavy ground army with Siege Tanks, Marines, Reapers, and Hellions. Your economy and tech are heavy. The opponent has a heavy air posture with Zealots, Stalkers, Phoenixes, and Observers.

**Direction:**  
Increase your anti-air capabilities. Consider adding Thors, Vikings, or more Marines. Continue to strengthen your ground army and maintain economy.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame vs Air Posture

**Trigger situation:**  
At around 420 seconds, you have a heavy ground army with Marines. Your economy and tech are heavy. The opponent has an air posture with Zealots, Stalkers, Phoenixes, and Observers.

**Direction:**  
Maintain your ground army but start adding anti-air units. Consider Vikings or Thors. Continue expanding and teching.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Late-Midgame vs Heavy Air

**Trigger situation:**  
At around 600 seconds, you have a heavy ground army with Siege Tanks, Marines, Reapers, and Hellions. Your economy and tech are heavy. The opponent has a heavy air posture with Zealots, Stalkers, Phoenixes, and Observers.

**Direction:**  
Maintain your ground army and continue to expand. Consider adding more anti-air units (Thors, Vikings) to counter the air threat. Keep teching.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Midgame Ground Army with Tech Focus

**Trigger situation:**  
At around 420 seconds, you have a heavy ground army with Siege Tanks, Marines, and Reapers. Your economy and tech are heavy. The opponent shows a ground posture with Zealots and Void Rays, heavy production.

**Direction:**  
Maintain your current army path and continue to tech. Consider adding anti-air to counter Void Rays. Keep expanding.

**Read for details:** `N011`

---
