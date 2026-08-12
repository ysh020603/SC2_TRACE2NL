# ZvT_O03 Economy / Technology / Expansion

## Skill Identity

- Skill ID: ZvT_O03
- Matchup: Zerg vs Terran
- Opening Family: economy / technology / expansion opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg opening that prioritizes economy and technology while expanding, aiming for a strong midgame position. The opponent is Terran, and the opening is flexible, allowing adaptation based on scouting.

Develop a robust economy and technology base while expanding, maintaining flexibility to respond to Terran's actions.

This is a strategic template, not a fixed build order. Adapt based on live scouting and enemy intelligence.

## Strategic Characteristics

- Economy: heavy
- Production: moderate
- Technology: moderate
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

### R01 — Maintain production tempo while preserving economy/tech expansion

**When:** Game time 240-360, bank above 2000, army supply below 5, production below 3, and at least one expansion completed or pending.

**Correction:** Convert bank into additional hatcheries and keep larvae spending on workers and a small defensive ground force. Prioritize completing the planned expansion and tech structures, but do not let production idle. If supply is below 30, add one overlord now and queue another only when supply approaches the cap.

**Recheck:** Next decision cycle, verify bank is below 2000, production is at least 3, and army supply is at least 5.

### R02 — Respond to Terran ground composition with defensive tech and anti-armor

**When:** Enemy intelligence shows Terran ground units (Marines, Reapers, Hellions, Siege Tanks, or Thors) and threat flag is not None.

**Correction:** If Siege Tanks or Thors are observed, start a Roach Warren and tech to Roach Speed if not already; if Hellions or Reapers are present, add a Spine Crawler at each base and keep a few Zerglings for map vision. Maintain at least one spore crawler per base if Medivacs are seen. Do not over-expand; keep army supply above 15.

**Recheck:** Next decision cycle, confirm defensive structures are in place and army supply is above 15; adjust if enemy composition shifts.

### R03 — Recover from low army and high bank with immediate army conversion

**When:** Army supply below 10, bank above 3000, and predicted advantage is OverwhelmingDisadvantage or threat flag is high.

**Correction:** Immediately spend bank on army-producing structures and units: add at least two hatcheries if larvae are insufficient, and queue a mix of Zerglings and Roaches (or Hydralisks if tech allows). Do not expand or tech further until army supply is above 20. If supply is below 40, add one overlord now and queue another only when supply approaches the cap.

**Recheck:** Next decision cycle, verify army supply is above 20 and bank is below 2000; if not, continue army conversion.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid overextending against a heavy ground Terran

**When:** Early-midgame, around 240-360 game time, with a solid economy and expansion, and enemy intelligence indicating a Terran ground posture with heavy production and technology, possibly Marines and Reapers.

**Mistake → correction:** Tempting to strengthen your ground army and increase production, economy, and expansion aggressively, but this can lead to engaging Siege Tanks head-on without proper tech or positioning, or over-expanding without sufficient army to defend. → Continue developing your economy and technology while strengthening your ground army. Maintain your expansion and production.

**Why:** A strong economy and technology base will allow you to outproduce the Terran in the midgame. Ground army strength is important to defend against potential pressure.

**Read for full checks:** `N001`

### L02 — Avoid overcommitting to army when enemy is unknown

**When:** Early game, around 180-240 game time, with a heavy economy and expansion, and enemy intelligence uncertain with no clear combat units observed, but production and technology appear heavy.

**Mistake → correction:** Tempting to strengthen ground army and increase production, economy, and expansion, but this can overcommit to army production early, slowing your economy, and neglect scouting for early pressure or all-ins. → Focus on economy and expansion while maintaining a defensive posture. Continue developing your technology.

**Why:** A strong economy early will pay off later. Since the opponent's intentions are unclear, it's safe to focus on macro.

**Read for full checks:** `N005`

### L03 — Avoid neglecting army while teching against multi-pronged pressure

**When:** Midgame, around 420 game time, with a heavy economy and investing in technology, and enemy intelligence showing a Terran ground posture with Marines, Reapers, Hellions, and Medivacs, indicating potential multi-pronged pressure.

**Mistake → correction:** Tempting to continue investing in technology and increase economy and expansion, but this can neglect army production while teching, or over-expand if an imminent attack is sensed. → Continue investing in technology while maintaining a defensive ground army. Be prepared for drops or harassment.

**Why:** Technology will give you access to stronger units and upgrades. A defensive posture is needed to handle potential multi-pronged attacks.

**Read for full checks:** `N006`

## Decision Nodes

### [DEFAULT] N001 — Early-Midgame Ground Development

**Trigger situation:**  
At around 240-360 game time, you have a solid economy and are expanding. Enemy intelligence suggests a Terran ground posture with heavy production and technology, possibly with Marines and Reapers.

**Direction:**  
Continue developing your economy and technology while strengthening your ground army. Maintain your expansion and production.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Expansion and Production

**Trigger situation:**  
At around 300-360 game time, you have a strong economy and are expanding. Enemy intelligence shows a Terran ground posture with Siege Tanks and Marines, indicating a potential defensive or siege-oriented approach.

**Direction:**  
Increase your production and expansion to match the Terran's heavy economy. Continue strengthening your ground army.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Late-Midgame Ground Strength

**Trigger situation:**  
At around 600-720 game time, you have a heavy economy and production. Enemy intelligence shows a Terran ground posture with Siege Tanks, Marines, Reapers, and Thors, indicating a strong ground army.

**Direction:**  
Maintain your ground army strength while continuing to develop your economy and technology. Consider adding more anti-air if the opponent's air presence increases.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground Defense and Tech

**Trigger situation:**  
At around 420-540 game time, you have a heavy economy and production. Enemy intelligence shows a Terran ground posture with Marines and Hellions, indicating potential harassment or early pressure.

**Direction:**  
Maintain your ground army and continue developing your technology. Be prepared to defend against Hellion run-bys or Marine pushes.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game Economy and Expansion

**Trigger situation:**  
At around 180-240 game time, you have a heavy economy and are expanding. Enemy intelligence is uncertain, with no clear combat units observed, but production and technology appear heavy.

**Direction:**  
Focus on economy and expansion while maintaining a defensive posture. Continue developing your technology.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Midgame Tech Investment

**Trigger situation:**  
At around 420 game time, you have a heavy economy and are investing in technology. Enemy intelligence shows a Terran ground posture with Marines, Reapers, Hellions, and Medivacs, indicating potential multi-pronged pressure.

**Direction:**  
Continue investing in technology while maintaining a defensive ground army. Be prepared for drops or harassment.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Midgame Expansion and Production

**Trigger situation:**  
At around 480-540 game time, you have a heavy economy and are expanding. Enemy intelligence shows a Terran ground posture with Marines and Hellions, indicating potential harassment.

**Direction:**  
Increase your production and expansion to maintain economic dominance. Continue strengthening your ground army.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Late-Midgame Air Transition

**Trigger situation:**  
At around 600 game time, you have a heavy economy and production. Enemy intelligence shows a Terran ground posture with Siege Tanks, Marines, and Battlecruisers, indicating a potential air transition.

**Direction:**  
Increase your air presence and continue developing your technology. Maintain a strong ground army for defense.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Early Game Tech and Expansion

**Trigger situation:**  
At around 180-240 game time, you have a heavy economy and are expanding. Enemy intelligence is uncertain, with only a Reaper seen, indicating possible early harassment.

**Direction:**  
Continue developing your economy and technology while maintaining a defensive posture against potential Reaper harassment.

**Read for details:** `N009`

---
