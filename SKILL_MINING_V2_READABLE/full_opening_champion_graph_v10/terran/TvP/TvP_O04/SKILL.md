# TvP_O04 Expansion / Economy / Technology

## Skill Identity

- Skill ID: TvP_O04
- Matchup: Terran vs Protoss
- Opening Family: expansion / economy / technology opening
- Method: Opening-Champion Full V10

## Opening Strategy

A Terran opening that prioritizes a heavy economy and technology investment while maintaining a flexible, ground-leaning army posture. The early game focuses on establishing a strong economic base and teching up, with production ramping up as the game progresses. The approach is adaptable, allowing for adjustments based on scouting information about the Protoss opponent's composition and strategy.

Develop a expansion / economy / technology posture while preserving flexibility for live observation-driven adaptation.

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

### R01 — Production Tempo with Economy Focus

**When:** Time >= 240 and (army_supply < 8 or production < 2) and bank > 800

**Correction:** Prioritize building additional production structures (Barracks, Factory, Starport) up to at least 3 total, and queue units from existing structures to keep them active. Maintain worker production toward saturation (target 30+ workers by 5 minutes). Avoid expanding until army supply >= 15 and production is active.

**Recheck:** Next decision cycle: verify army_supply >= 8, production >= 3, and worker count >= 30.

### R02 — Enemy Composition Response

**When:** Enemy Intelligence indicates air-heavy composition (e.g., Phoenixes, Oracles, Void Rays) and army lacks sufficient anti-air (e.g., Marines, Thors, Vikings)

**Correction:** Add anti-air units to your composition: produce Marines from Barracks, or add a Starport for Vikings. Ensure at least 4 anti-air units or 2 Thors/Vikings. Maintain ground army and continue economy/tech development.

**Recheck:** Next decision cycle: confirm anti-air unit count >= 4 or presence of Thors/Vikings.

### R03 — Recovery from Low Army and High Bank

**When:** army_supply < 15 and bank > 1500 and (predicted_advantage == OverwhelmingDisadvantage or threat_flags indicate imminent attack)

**Correction:** Immediately convert bank into army: queue units from all production structures, prioritize combat units over workers. If production is insufficient, build additional production structures. Do not expand or tech until army_supply >= 15 and production is active.

**Recheck:** Next decision cycle: verify army_supply >= 15 and bank < 1000.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Don't Overextend Economy

**When:** Early-midgame, both sides ground-oriented with heavy production and tech, around 300 seconds.

**Mistake → correction:** Continuing to expand and tech without reinforcing your army, assuming the enemy is passive. → Strengthen your ground army and increase technology investment. Consider adding air units for flexibility. Maintain expansion and production.

**Why:** The opponent is ground-oriented, so a strong ground army is essential. Air units provide flexibility against potential air transitions.

**Read for full checks:** `N002`

### L02 — Early Game: Don't Overcommit to Tech

**When:** Early game, both sides unknown compositions, heavy economy and tech investment, around 180 seconds.

**Mistake → correction:** Over-committing to tech at the expense of army production and neglecting scouting. → Focus on developing economy and technology while maintaining a light defensive posture. Use your Reaper for scouting to gather information.

**Why:** This sets up a strong midgame, and scouting helps you adapt to the opponent's choices.

**Read for full checks:** `N003`

### L03 — Ground vs Air: Don't Ignore Anti-Air

**When:** Early-midgame, opponent air-oriented with Phoenixes and Oracles, you have ground army with Siege Tanks and Marines, around 360 seconds.

**Mistake → correction:** Neglecting your ground army entirely or over-investing in anti-air without a clear threat. → Add anti-air units such as Marines, Thors, or Vikings to counter the opponent's air presence. Maintain your ground army and continue expanding.

**Why:** The opponent's air units can be a threat, so you need a response. Adding anti-air units helps defend against harass and potential air attacks.

**Read for full checks:** `N006`

## Decision Nodes

### [DEFAULT] N001 — Early Midgame Ground Development

**Trigger situation:**  
At around 240 seconds, you have a ground-oriented army with heavy production and technology, while the opponent is still unknown but likely teching heavily.

**Direction:**  
Continue developing your economy and technology while strengthening your ground army. Maintain your current defensive posture and keep expanding.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Army Strengthening

**Trigger situation:**  
At around 300 seconds, you have a ground army with Marines and Reapers, and the opponent is also ground-oriented with Stalkers. Both have heavy economies and technology.

**Direction:**  
Continue strengthening your ground army and increase your technology investment. Consider adding air units to complement your ground forces. Maintain your expansion and production.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Game Tech and Economy Focus

**Trigger situation:**  
At around 180 seconds, both you and the opponent have unknown army compositions, but both are investing heavily in economy and technology.

**Direction:**  
Focus on developing your economy and technology while maintaining a light defensive posture. Use your Reaper for scouting to gather information about the opponent's strategy.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground Army with Air Support

**Trigger situation:**  
At around 420 seconds, you have a ground army with Marines and Medivacs, while the opponent has a ground army with Stalkers and Warp Prisms. Both have heavy economies and technology.

**Direction:**  
Continue strengthening your ground army and increase your technology and upgrades. Maintain your air presence and consider adding more Medivacs for mobility and healing. Keep expanding.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Late Midgame Ground Army with Siege Tanks

**Trigger situation:**  
At around 600 seconds, you have a ground army with Siege Tanks, Marines, and Marauders, while the opponent has a ground army with Zealots, High Templars, Sentries, and Warp Prisms.

**Direction:**  
Continue strengthening your ground army and increase your technology and upgrades. Consider adding more Siege Tanks for defensive strength and Marauders for tanking. Maintain your expansion.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early Midgame Air Transition

**Trigger situation:**  
At around 360 seconds, the opponent has an air-oriented army with Phoenixes and Oracles, while you have a ground army with Siege Tanks and Marines.

**Direction:**  
Consider adding anti-air units such as Marines, Thors, or Vikings to counter the opponent's air presence. Maintain your ground army and continue expanding.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Midgame Air Defense

**Trigger situation:**  
At around 540 seconds, the opponent has a heavy air presence with Phoenixes and Immortals, while you have a ground army with Marines and Marauders.

**Direction:**  
Increase your air presence and add anti-air units such as Vikings or Thors. Continue strengthening your ground army and maintain your defensive posture.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Late Midgame Air and Ground Balance

**Trigger situation:**  
At around 600 seconds, the opponent has a heavy air presence with Phoenixes and Sentries, while you have a ground army with Marines, Reapers, Medivacs, and Widow Mines.

**Direction:**  
Increase your air presence and add anti-air units such as Vikings or Thors. Continue strengthening your ground army and maintain your defensive posture.

**Read for details:** `N008`

---
