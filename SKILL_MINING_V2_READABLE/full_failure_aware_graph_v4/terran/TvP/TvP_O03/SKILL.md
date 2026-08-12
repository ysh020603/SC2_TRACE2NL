# TvP_O03 Technology / Economy / Production

## Skill Identity

- Skill ID: TvP_O03
- Matchup: Terran vs Protoss
- Opening Family: technology / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Terran opening that emphasizes heavy economy and technology investment while keeping production moderate, aiming for a flexible transition into either a ground or air-oriented midgame based on scouting.

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

### R01 — Production Tempo and Bank Conversion

**When:** At any point before 6 minutes, if average bank exceeds 1500 minerals and production is below 3 active structures, or if army supply is below 15 and bank exceeds 1000.

**Correction:** Prioritize converting bank into production: add Barracks or Factory if prerequisites are met, and queue units from existing structures. Ensure worker production continues toward saturation (target 2 per base) without letting worker queues delay army production. Recheck at next decision cycle.

**Recheck:** Bank > 1500 and production < 3, or army supply < 15 and bank > 1000.

### R02 — Enemy Composition Response

**When:** When enemy intelligence reveals a significant air threat (e.g., Carriers, Void Rays, Phoenix) or heavy ground splash (e.g., Colossus, High Templar) and current army lacks appropriate counters.

**Correction:** Adjust production and technology to counter the observed composition: if air threat, add Marines and Vikings, and ensure Starport with tech lab is available; if ground splash, add Siege Tanks and consider Ghosts for EMP. Maintain economy and production while transitioning. Recheck at next decision cycle.

**Recheck:** Enemy composition includes air or splash units and current army lacks counters.

### R03 — Recovery from Low Army and High Bank

**When:** When army supply is below 15, bank exceeds 2000, and predicted advantage is OverwhelmingDisadvantage or threat flags indicate imminent attack.

**Correction:** Immediately convert bank into army: queue units from all available production structures, add supply providers if needed (but only one at a time), and prioritize defensive structures if threatened. Do not expand or tech switch until army supply is above 15 and bank is reduced. Recheck at next decision cycle.

**Recheck:** Army supply < 15 and bank > 2000 and (predicted advantage is OverwhelmingDisadvantage or threat flags active).

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid overcommitting to a single attack

**When:** Midgame with a ground-oriented army, heavy production and technology, and moderate defense.

**Mistake → correction:** Committing to a single attack without sufficient army strength, risking a counterattack while the opponent is also building up. → Continue strengthening your ground army and maintain economy and production. Consider adding more Siege Tanks or transitioning to air if the opponent goes for Colossus or air units.

**Why:** Siege Tanks provide strong defensive and offensive capabilities against ground armies. Maintaining a heavy economy allows you to tech switch if needed.

**Read for full checks:** `N003`

### L02 — Avoid engaging without proper positioning

**When:** Midgame with a ground-oriented army, heavy production and technology, and moderate defense.

**Mistake → correction:** Engaging in a straight-up fight without proper positioning, as the opponent's army is powerful. → Continue strengthening your ground army and maintain economy and production. Consider adding more Siege Tanks or transitioning to air if the opponent goes for Colossus or air units.

**Why:** Siege Tanks provide strong defensive and offensive capabilities against ground armies. Maintaining a heavy economy allows you to tech switch if needed.

**Read for full checks:** `N005`

### L03 — Avoid neglecting ground defense during air transition

**When:** Midgame with a ground-oriented army transitioning to air, with moderate air presence and Banshees.

**Mistake → correction:** Neglecting ground defense while focusing on air, as the opponent could still push with a strong ground army. → Increase your air presence and strengthen your air army. Continue developing your economy and technology to support the transition.

**Why:** Transitioning to air can give you an advantage if the opponent is heavily ground-based. Banshees can harass and provide mobility.

**Read for full checks:** `N006`

## Decision Nodes

### [DEFAULT] N001 — Early Game Tech/Eco Development

**Trigger situation:**  
At the start of the game, both sides are in early game with unknown army compositions. You have a heavy economy and technology focus, with moderate production and a light defense posture.

**Direction:**  
Continue developing your economy and technology while maintaining a light defense. Increase your expansion and production to support a strong midgame.

**Read for details:** `N001`

---

### [POSITIVE] N002 — Early-Midgame Ground Macro

**Trigger situation:**  
By early-midgame, both you and the opponent have committed to a ground-oriented army with heavy production and technology. Your economy is heavy, and you have a strong expansion.

**Direction:**  
Continue strengthening your ground army and maintain your economy and production. Keep your expansion and technology development going.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Army with Siege Tanks

**Trigger situation:**  
In the midgame, you have a ground-oriented army with heavy production and technology. Your defense posture is moderate, and you have Siege Tanks and Marines as representative units.

**Direction:**  
Continue strengthening your ground army and maintain your economy and production. Consider adding more Siege Tanks or transitioning to air if the opponent goes for Colossus or air units.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground Army with Siege Tanks (Alternate)

**Trigger situation:**  
In the midgame, you have a ground-oriented army with heavy production and technology. Your defense posture is moderate, and you have Siege Tanks and Marines as representative units.

**Direction:**  
Continue strengthening your ground army and maintain your economy and production. Consider adding more Siege Tanks or transitioning to air if the opponent goes for Colossus or air units.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Ground Army with Siege Tanks and Marines

**Trigger situation:**  
In the midgame, you have a ground-oriented army with heavy production and technology. Your defense posture is moderate, and you have Siege Tanks and Marines as representative units.

**Direction:**  
Continue strengthening your ground army and maintain your economy and production. Consider adding more Siege Tanks or transitioning to air if the opponent goes for Colossus or air units.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Midgame Air Transition

**Trigger situation:**  
In the midgame, you have a ground-oriented army with heavy production and technology, but you are transitioning to an air-oriented army. Your air presence is moderate, and you have Banshees as representative units.

**Direction:**  
Increase your air presence and strengthen your air army. Continue developing your economy and technology to support the transition.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Late-Midgame Ground Army with Medivacs

**Trigger situation:**  
In the late-midgame, you have a ground-oriented army with heavy production and technology. Your defense posture is heavy, and you have Siege Tanks, Marines, and Medivacs as representative units.

**Direction:**  
Continue strengthening your ground army and maintain your economy and production. Consider adding Vikings to counter Colossus if the opponent has them.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Late-Midgame Ground Army with Reapers

**Trigger situation:**  
In the late-midgame, you have a ground-oriented army with heavy production and technology. Your defense posture is heavy, and you have Siege Tanks, Marines, Reapers, and Medivacs as representative units.

**Direction:**  
Continue strengthening your ground army and maintain your economy and production. Consider adding more Siege Tanks or transitioning to air if the opponent goes for Colossus or air units.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Late-Midgame Air Transition

**Trigger situation:**  
In the late-midgame, you have a ground-oriented army with heavy production and technology, but you are transitioning to an air-oriented army. Your air presence is moderate, and you have Banshees and Battlecruisers as representative units.

**Direction:**  
Increase your air presence and strengthen your air army. Continue developing your economy and technology to support the transition.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Early Game Tech/Eco with Reaper

**Trigger situation:**  
At the start of the game, you have a heavy economy and technology focus, with moderate production. You have a Reaper as a representative unit, indicating early harassment potential.

**Direction:**  
Use your Reaper for scouting and harassment while continuing to develop your economy and technology. Increase your production to support a strong midgame.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early-Midgame Ground Macro (Alternate)

**Trigger situation:**  
By early-midgame, you have a ground-oriented army with heavy production and technology. Your economy is heavy, and you have a strong expansion. The opponent's posture is still unknown, but they have Zealots and Stalkers.

**Direction:**  
Continue strengthening your ground army and maintain your economy and production. Keep your expansion and technology development going.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Midgame Ground Army vs Air

**Trigger situation:**  
In the midgame, you have a ground-oriented army with heavy production and technology. Your defense posture is heavy, and you have Siege Tanks, Marines, Reapers, and Medivacs as representative units. The opponent has transitioned to an air-oriented army with Carriers.

**Direction:**  
Consider transitioning to an air-oriented army to counter the opponent's Carriers. Add Vikings or other anti-air units to your composition.

**Read for details:** `N012`

---
