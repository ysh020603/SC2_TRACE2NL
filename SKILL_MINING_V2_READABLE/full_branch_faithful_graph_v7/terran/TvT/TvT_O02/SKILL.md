# TvT_O02 Economy / Technology / Production

## Skill Identity

- Skill ID: TvT_O02
- Matchup: Terran vs Terran
- Opening Family: economy / technology / production opening
- Method: Branch-Faithful Full V7

## Opening Strategy

A flexible Terran opening that prioritizes economic and technological development while keeping production options open. Early game is characterized by light or uncertain information, with the potential to transition into a heavy ground-based macro posture.

Develop a robust economy and technology base while maintaining flexibility to adapt to opponent actions. Aim to reach a strong mid-game position with a solid ground army and the option to transition to air if needed.

This is a strategic template, not a fixed build order. Adapt based on live observations and opponent actions.

## Strategic Characteristics

- Economy: light_or_uncertain
- Production: light_or_uncertain
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

### G05 — Terran production interpretation

- Scale Barracks/Factory/Starport capacity before ordering add-ons or units that lack a completed parent structure.

## V4 Matchup-Specific Corrections

### R01 — Production Tempo and Bank Conversion

**When:** At any time, if bank is above 800 minerals and production structures are idle or insufficient (active queues less than 2 per structure), or if army supply is below 15 and bank is above 600.

**Correction:** Queue units from existing production structures, prioritizing Marines and Marauders. If all production structures are already queued and bank remains above 1000, add a Barracks (or Factory if tech allows) to increase production capacity. Do not expand until army supply is at least 15 and production is saturated.

**Recheck:** Recheck at next decision cycle.

### R02 — Enemy Composition Response

**When:** When enemy intelligence reveals a composition with Reapers or early aggression (e.g., Reaper seen), or a ground-heavy army with Marines, Marauders, and Siege Tanks.

**Correction:** If Reapers are present, build a Marauder or a Bunker at your natural to defend workers. If the enemy is ground-heavy with Siege Tanks, add Siege Tanks of your own or Vikings for vision and to siege their tanks. Ensure you have at least one tech lab on a Barracks or Factory to produce Marauders or Siege Tanks. Keep production active to match their army size.

**Recheck:** Recheck at next decision cycle.

### R03 — Recovery from Low Army and High Bank

**When:** When army supply is below 15 and bank is above 1000 minerals, or when predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all available production structures, prioritizing Marines and Marauders. If production is insufficient, add a Barracks (or Factory) and queue units. Do not spend on expansions or technology until army supply is at least 15 and bank is below 500. If threatened, also build a Bunker at your natural for defense.

**Recheck:** Recheck at next decision cycle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Reaper Harassment Response

**When:** Early game, when you spot a Reaper from the opponent and your own economy is moderate with technology investment.

**Mistake → correction:** Overcommitting to economy and technology while ignoring the Reaper threat, leaving your workers vulnerable to harassment. → Strengthen your ground forces and increase production. Build a defensive structure or a unit to counter Reaper harassment.

**Why:** The Reaper suggests early aggression or a tech switch; defending against it prevents economic damage and prepares you for a counter.

**Read for full checks:** `N004`

### L02 — Midgame Ground Macro Mirror

**When:** Midgame, when both you and the opponent have ground-based armies with Marines and Reapers, and heavy economies.

**Mistake → correction:** Neglecting your economy while building an army, or overcommitting to a single unit composition without adaptability. → Continue strengthening your ground forces and increasing your economy. Consider adding supporting units like Marauders or Siege Tanks.

**Why:** Both players are on a similar ground macro path; strengthening army and economy helps gain an advantage in the midgame.

**Read for full checks:** `N005`

### L03 — Catching Up Against a Strong Ground Army

**When:** Early midgame, when the opponent has a strong ground army with Marines, Reapers, and Marauders, while your own posture is underdeveloped.

**Mistake → correction:** Engaging the opponent's army without a plan, or neglecting your economy while trying to catch up. → Maintain your current development path, but be aware that the opponent is ahead. Consider building a defensive structure or a unit to counter the opponent's composition.

**Why:** The opponent has a strong ground army, so you need to catch up. Maintaining development while preparing a defense is the safest option.

**Read for full checks:** `N007`

## Decision Nodes

### [DEFAULT] N001 — Early Game Development

**Trigger situation:**  
At the start of the game, both players have limited information. The opponent's posture is unknown, and your own production and technology are light or uncertain.

**Direction:**  
Maintain current development path, focusing on economy and technology. Avoid unnecessary risks.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Midgame Development

**Trigger situation:**  
As the game progresses into the early-midgame, the opponent's posture remains unknown, but you have had time to develop your economy and technology.

**Direction:**  
Continue maintaining your current development path, focusing on economy and technology. Keep your options open.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Development

**Trigger situation:**  
In the midgame, the opponent's posture is still unknown, but you have had time to build up your economy and technology.

**Direction:**  
Continue maintaining your current development path, focusing on economy and technology. Keep your options open.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early Game with Reaper Cue

**Trigger situation:**  
Early game, you spot a Reaper from the opponent, indicating a possible aggressive or tech-oriented opening. Your own economy is moderate, and you have invested in technology.

**Direction:**  
Strengthen your ground forces and increase production. Consider building a defensive structure or a unit to counter Reaper harassment.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Ground Macro

**Trigger situation:**  
Midgame, the opponent has a ground-based army with Marines and Reapers, and a heavy economy. You have a similar ground composition.

**Direction:**  
Continue strengthening your ground forces and increasing your economy. Consider adding supporting units like Marauders or Siege Tanks.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Late Midgame Ground Macro

**Trigger situation:**  
Late midgame, the opponent has a strong ground army with Siege Tanks, Marines, Reapers, and Medivacs. Your own posture is unknown and underdeveloped.

**Direction:**  
Maintain your current development path, but be aware that you are behind. Consider building a defensive structure or a unit to counter the opponent's composition.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early Midgame Ground Macro

**Trigger situation:**  
Early midgame, the opponent has a ground army with Marines, Reapers, and Marauders. Your own posture is unknown and underdeveloped.

**Direction:**  
Maintain your current development path, but be aware that the opponent is ahead. Consider building a defensive structure or a unit to counter the opponent's composition.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Ground Macro

**Trigger situation:**  
Midgame, the opponent has a strong ground army with Siege Tanks, Marines, Reapers, and Medivacs. Your own posture is unknown and underdeveloped.

**Direction:**  
Maintain your current development path, but be aware that you are behind. Consider building a defensive structure or a unit to counter the opponent's composition.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Early Midgame Ground Macro

**Trigger situation:**  
Early midgame, the opponent has a ground army with Reapers, and a heavy economy. You have a ground army with Marines.

**Direction:**  
Strengthen your ground forces and increase your economy. Consider adding supporting units like Marauders or Reapers.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Early Game with Reaper Cue

**Trigger situation:**  
Early game, you spot a Reaper from the opponent, indicating a possible aggressive or tech-oriented opening. Your own economy is moderate, and you have invested in technology.

**Direction:**  
Strengthen your ground forces and increase production. Consider building a defensive structure or a unit to counter Reaper harassment.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early Midgame Ground Macro

**Trigger situation:**  
Early midgame, the opponent has a ground army with Marines and Reapers, and a heavy economy. You have a similar ground composition.

**Direction:**  
Continue strengthening your ground forces and increasing your economy. Consider adding supporting units like Marauders or Siege Tanks.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Midgame Transition to Air

**Trigger situation:**  
Midgame, the opponent has a ground army with Marines and Reapers. You have a ground army with Siege Tanks, Marines, Hellions, and Medivacs, and you are considering adding air units.

**Direction:**  
Increase your air presence and strengthen your air forces. Consider adding Vikings or Banshees to gain an advantage.

**Read for details:** `N012`

---
