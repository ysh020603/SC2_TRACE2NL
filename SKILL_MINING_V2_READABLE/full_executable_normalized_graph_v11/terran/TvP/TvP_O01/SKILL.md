# TvP_O01 Technology / Economy / Production

## Skill Identity

- Skill ID: TvP_O01
- Matchup: Terran vs Protoss
- Opening Family: technology / economy / production opening
- Method: Executable-Normalized Full V11

## Opening Strategy

A macro-oriented opening that prioritizes heavy technology and economy development while maintaining moderate production. The strategic template emphasizes flexible adaptation based on live observation rather than a fixed build order.

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

### G05 — Terran production interpretation

- Scale Barracks/Factory/Starport capacity before ordering add-ons or units that lack a completed parent structure.

## V4 Matchup-Specific Corrections

### R01 — Maintain production tempo while preserving tech/economy opening

**When:** Time >= 240 and (army_supply < 15 or production < 2) and bank > 800

**Correction:** Prioritize adding production structures (e.g., Barracks, Factory, Starport) up to at least 3 total, and queue units from existing structures to keep them active. Continue worker production toward saturation (target ~30 workers by 5 minutes). Avoid expanding until army_supply >= 15 and production is sufficient.

**Recheck:** Recheck at next decision cycle: confirm production >= 3 and army_supply >= 15, or bank < 400.

### R02 — Adapt to enemy composition with appropriate tech and units

**When:** Enemy intelligence indicates air-heavy (e.g., Void Rays, Phoenix) or Colossus-based ground composition

**Correction:** If air-heavy, add Marines and/or Thors, and ensure at least one tech lab on Barracks/Factory for upgrades. If Colossus, add Vikings or Liberators, and consider Widow Mines for defense. Maintain ground army core (Marines, Siege Tanks) while adding counters. Keep production active to support the transition.

**Recheck:** Recheck at next decision cycle: confirm counter units are in production or completed, and army composition includes required anti-air/anti-Colossus.

### R03 — Recover from low army and high bank with urgent production

**When:** army_supply < 15 and bank > 1500 and (predicted_advantage == OverwhelmingDisadvantage or threat_flags indicate imminent attack)

**Correction:** Immediately convert bank into army: queue units from all available production structures, add production structures if supply allows (up to 4 total), and prioritize combat units over economy. Do not expand or tech further until army_supply >= 30. If supply blocked, add a supply provider (but only one per decision).

**Recheck:** Recheck at next decision cycle: confirm army_supply increased by at least 10 or bank reduced below 800.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid premature army commitment

**When:** Early game, around 180 seconds, with unknown enemy posture and heavy tech investment.

**Mistake → correction:** Committing to a large army before knowing the opponent's plan, or over-expanding without defense. → Focus on developing economy and tech while maintaining production. Strengthen ground army as a baseline.

**Why:** Early game is about establishing a strong economy and tech base. A ground-oriented army provides flexibility against unknown enemy tech.

**Read for full checks:** `N002`

### L02 — Balance expansion with defense

**When:** Early-midgame, around 240 seconds, with ground-oriented posture and heavy production.

**Mistake → correction:** Neglecting defense while expanding, or committing to a single tech path without information. → Continue strengthening ground army and increase production. Maintain expansion and tech progression.

**Why:** Heavy production allows a strong ground army. Continuing to expand and tech gives a long-term advantage.

**Read for full checks:** `N003`

### L03 — Maintain defense while developing

**When:** Early-midgame, around 360 seconds, with ground-oriented posture and enemy ground cues.

**Mistake → correction:** Continuing to expand and tech without reinforcing the army, assuming the enemy is passive. → Maintain defensive posture while continuing to develop ground army. Increase economy and tech.

**Why:** Siege Tanks provide strong defensive capabilities against ground pushes. Maintaining defense while expanding gives a safe economy.

**Read for full checks:** `N005`

## Decision Nodes

### [DEFAULT] N001 — Early-Mid Ground Macro with Heavy Tech

**Trigger situation:**  
At around 240 seconds, you have a ground-oriented posture with moderate production and heavy technology investment. Enemy intelligence suggests a ground posture with Zealot/Stalker cues, heavy production, and heavy tech.

**Direction:**  
Continue developing your ground army while increasing economy and expansions. Maintain defense and tech progression.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early Game Tech/Economy Development

**Trigger situation:**  
At around 180 seconds, both sides are in early game with unknown army compositions. You have heavy economy and tech investment, moderate production, and are expanding.

**Direction:**  
Focus on developing your economy and tech while maintaining production. Strengthen your ground army as a baseline.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early-Mid Ground Push with Heavy Production

**Trigger situation:**  
At around 240 seconds, you have a ground-oriented posture with heavy production and heavy tech. Enemy is unknown but has heavy economy and tech, with moderate production.

**Direction:**  
Continue strengthening your ground army and increase production. Maintain expansion and tech progression.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Mid Ground vs Ground with Air Support

**Trigger situation:**  
At around 600 seconds, you have a ground-oriented posture with heavy production and tech, and moderate air presence. Enemy is ground-oriented with Zealot/Stalker/Sentry/Immortal cues.

**Direction:**  
Increase your air presence while continuing to strengthen your ground army. Maintain defense and tech progression.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early-Mid Ground Defense with Siege Tanks

**Trigger situation:**  
At around 360 seconds, you have a ground-oriented posture with heavy production and tech, including Siege Tanks and Marines. Enemy is ground-oriented with Zealot/Stalker/Observer cues.

**Direction:**  
Maintain your defensive posture while continuing to develop your ground army. Increase economy and tech.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Midgame Ground vs Colossus Composition

**Trigger situation:**  
At around 480 seconds, you have a ground-oriented posture with heavy production and tech. Enemy has a ground posture with Colossus, Zealot, Stalker, and Observer cues.

**Direction:**  
Increase your defensive capabilities and continue developing your ground army. Consider tech that counters Colossus, such as Vikings or Liberators.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Midgame Ground with Widow Mines

**Trigger situation:**  
At around 480 seconds, you have a ground-oriented posture with heavy production and tech, including Widow Mines. Enemy has a ground posture with Colossus, Zealot, Stalker, and Observer cues.

**Direction:**  
Maintain your ground army and continue developing. Consider adding anti-Colossus units while keeping your Widow Mines for defense.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Ground vs Air (Void Ray)

**Trigger situation:**  
At around 540 seconds, you have a ground-oriented posture with heavy production and tech, including Siege Tanks, Marines, and Widow Mines. Enemy has an air posture with Stalker and Void Ray cues.

**Direction:**  
Increase your defensive capabilities against air, such as adding Marines or Thors. Continue developing your ground army.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Early-Mid Ground vs Air (Void Ray)

**Trigger situation:**  
At around 360 seconds, you have a ground-oriented posture with heavy production and tech, including Siege Tanks and Marines. Enemy has an air posture with Stalker and Void Ray cues.

**Direction:**  
Increase your defensive capabilities against air, such as adding Marines or Thors. Continue developing your ground army.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Midgame Ground vs Air (Void Ray) - Maintain

**Trigger situation:**  
At around 540 seconds, you have a ground-oriented posture with heavy production and tech, including Siege Tanks and Marines. Enemy has an air posture with Stalker and Void Ray cues.

**Direction:**  
Maintain your ground army and continue developing. Ensure you have sufficient anti-air to defend against Void Rays.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Late-Mid Ground vs Air (Void Ray) - Defensive

**Trigger situation:**  
At around 600 seconds, you have a ground-oriented posture with heavy production and tech, including Marines. Enemy has an air posture with Stalker, Sentry, and Void Ray cues.

**Direction:**  
Increase your defensive capabilities against air, such as adding Thors or Marines. Continue developing your ground army.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Early-Mid Ground vs Air (Void Ray) - Maintain

**Trigger situation:**  
At around 300 seconds, you have a ground-oriented posture with heavy production and tech, including Siege Tanks and Marines. Enemy has an air posture with Stalker and Void Ray cues.

**Direction:**  
Maintain your ground army and continue developing. Ensure you have sufficient anti-air to defend against Void Rays.

**Read for details:** `N012`

---
