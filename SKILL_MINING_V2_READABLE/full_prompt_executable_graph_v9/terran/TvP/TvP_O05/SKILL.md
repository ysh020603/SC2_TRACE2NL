# TvP_O05 Technology / Economy / Upgrade

## Skill Identity

- Skill ID: TvP_O05
- Matchup: Terran vs Protoss
- Opening Family: technology / economy / upgrade opening
- Method: Prompt-Executable Full V9

## Opening Strategy

A Terran opening that emphasizes heavy technology and economy development while maintaining a flexible ground-oriented posture. The opening is designed to support a strong mid-game transition with upgrades and production, while keeping options open for adaptation based on scouting.

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

### G05 — Terran production interpretation

- Scale Barracks/Factory/Starport capacity before ordering add-ons or units that lack a completed parent structure.

## V4 Matchup-Specific Corrections

### R01 — Maintain production tempo and worker saturation

**When:** Time >= 240 and (workers < 28 or production < 2 or bank > 1500)

**Correction:** Queue workers from all Command Centers until saturation (target 28+ workers by 4:00, 32+ by 5:00). If production is below 2, add a Barracks or Factory (prerequisite: supply available). If bank exceeds 1500, add production structures (Barracks/Factory) or start an upgrade (e.g., +1 infantry weapons) if prerequisites are met. Keep army supply above 15 before considering an expansion.

**Recheck:** Recheck at next decision cycle.

### R02 — Adapt to enemy air composition

**When:** Enemy Intelligence indicates air units (e.g., Oracles, Phoenixes, Void Rays) and your army lacks anti-air (e.g., no Marines, no Missile Turrets, no Cyclones)

**Correction:** Add anti-air capability: produce Marines from Barracks, add a Missile Turret at each mineral line, or build a Cyclone from a Factory (prerequisite: Factory with tech lab). Maintain ground army production and continue economy/technology development.

**Recheck:** Recheck at next decision cycle.

### R03 — Recover from low army and high bank

**When:** Army supply < 15 and bank > 2000 and (predicted advantage is OverwhelmingDisadvantage or threat flags indicate imminent attack)

**Correction:** Immediately convert bank into army: queue units from all production structures (Barracks, Factory, Starport) and add production if idle. Prioritize combat units over workers. Do not expand or start new upgrades until army supply is above 15 and bank is below 1000.

**Recheck:** Recheck at next decision cycle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid over-committing to a single attack without scouting

**When:** Early-midgame, around 4 minutes, both sides have heavy economy and production, opponent likely ground with Zealots/Stalkers, you have Marines/Marauders.

**Mistake → correction:** Over-committing to a single attack without scouting, neglecting anti-air, or over-investing in ground without flexibility. → Continue strengthening your ground army while increasing economy and expansions. Maintain current defense and technology development.

**Why:** Both sides are in a macro-oriented phase. Maintaining a strong economy and production allows you to out-scale the opponent if they commit to a ground composition.

**Read for full checks:** `N001`

### L02 — Avoid over-extending economy without sufficient army

**When:** Early game, around 3 minutes, you have ground army of Marines/Marauders, heavy economy, opponent posture unknown but heavy economy.

**Mistake → correction:** Over-extending your economy without sufficient army, or neglecting scouting to identify opponent's tech path. → Increase your production and continue developing your ground army. Maintain your economy and technology development.

**Why:** With a ground army already established, it is efficient to continue producing units and expanding your economy to support a strong mid-game.

**Read for full checks:** `N004`

### L03 — Avoid neglecting anti-air against air transition

**When:** Early-midgame, around 5 minutes, opponent has transitioned to air with Oracles/Zealots, you have ground army with Marines/Marauders.

**Mistake → correction:** Neglecting your ground army in favor of anti-air, or being caught off guard by Oracle harassment. → Maintain your ground army while considering adding anti-air capabilities. Continue developing your economy and technology.

**Why:** The opponent's air presence requires you to prepare for potential Oracle harassment or a transition to a more air-heavy composition.

**Read for full checks:** `N006`

## Decision Nodes

### [DEFAULT] N001 — Early-Mid Ground Macro with Heavy Economy

**Trigger situation:**  
At around 4 minutes, both sides have a heavy economy and production. The opponent is likely ground-oriented with Zealots and Stalkers, while you have Marines and Marauders.

**Direction:**  
Continue strengthening your ground army while increasing economy and expansions. Maintain your current defense and technology development.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Mid Ground Macro with Moderate Defense

**Trigger situation:**  
At around 4 minutes, you have a heavy economy and production, but your defense is moderate. The opponent is ground-oriented with Zealots and Stalkers.

**Direction:**  
Maintain your current production and economy, while slightly increasing your defense. Continue technology development.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Game Unknown Posture with Heavy Economy

**Trigger situation:**  
At around 3 minutes, the opponent's army composition is unknown, but they have a heavy economy and technology. You have a heavy economy and production.

**Direction:**  
Continue developing your economy and technology, while maintaining a flexible army composition. Strengthen your ground forces as a baseline.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early Game Ground Macro with Heavy Economy

**Trigger situation:**  
At around 3 minutes, you have a ground army of Marines and Marauders, with a heavy economy. The opponent's posture is unknown but they have a heavy economy.

**Direction:**  
Increase your production and continue developing your ground army. Maintain your economy and technology development.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Mid-Game Air Transition by Opponent

**Trigger situation:**  
At around 5 minutes, the opponent has transitioned to an air posture with Oracles and Zealots. You have a ground army with Marines and Marauders.

**Direction:**  
Maintain your ground army while considering adding anti-air capabilities. Continue developing your economy and technology.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Mid-Game Air Transition by Opponent

**Trigger situation:**  
At around 5 minutes, the opponent has transitioned to an air posture with Oracles and Zealots. You have a ground army with Marines and Marauders.

**Direction:**  
Maintain your ground army while considering adding anti-air capabilities. Continue developing your economy and technology.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Mid-Game Ground Macro with Heavy Economy

**Trigger situation:**  
At around 9 minutes, the opponent has a ground posture with Zealots, Stalkers, Sentries, and Observers. You have a ground army with Marines and Marauders.

**Direction:**  
Continue strengthening your ground army and economy. Maintain your defense and technology development.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Mid-Game Air Transition by Opponent

**Trigger situation:**  
At around 8 minutes, the opponent has a heavy air presence with Phoenixes and Oracles. You have a ground army with Marines, Marauders, and Widow Mines.

**Direction:**  
Maintain your ground army while considering adding anti-air capabilities. Continue developing your economy and technology.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Late-Mid Ground Macro with Heavy Defense

**Trigger situation:**  
At around 10 minutes, the opponent has a ground posture with Colossi, Zealots, Stalkers, and Sentries. You have a ground army with Siege Tanks, Marines, and Reapers.

**Direction:**  
Increase your defense and continue developing your ground army. Maintain your economy and technology development.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Mid-Game Ground Macro with Air Support

**Trigger situation:**  
At around 9 minutes, the opponent has a ground posture with Zealots, Stalkers, Sentries, and Observers. You have a ground army with Marines, Marauders, Medivacs, and Widow Mines.

**Direction:**  
Increase your air presence and continue developing your ground army. Maintain your economy and technology development.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early Game Unknown Posture with Heavy Economy

**Trigger situation:**  
At around 3 minutes, the opponent's army composition is unknown, but they have a heavy economy and technology. You have a heavy economy and production.

**Direction:**  
Continue developing your economy and technology, while maintaining a flexible army composition. Strengthen your ground forces as a baseline.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Early-Mid Ground Macro with Heavy Economy

**Trigger situation:**  
At around 6 minutes, the opponent has a ground posture with Stalkers. You have a ground army with Marines and Marauders.

**Direction:**  
Increase your production and continue developing your ground army. Maintain your economy and technology development.

**Read for details:** `N012`

---
