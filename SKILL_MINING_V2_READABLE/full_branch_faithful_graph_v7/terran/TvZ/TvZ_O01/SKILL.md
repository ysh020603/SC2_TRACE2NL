# TvZ_O01 Expansion / Economy / Technology

## Skill Identity

- Skill ID: TvZ_O01
- Matchup: Terran vs Zerg
- Opening Family: expansion / economy / technology opening
- Method: Branch-Faithful Full V7

## Opening Strategy

A Terran opening that prioritizes economic expansion and heavy technology investment while maintaining a flexible ground-oriented posture. The plan is to develop infrastructure and tech steadily, with safety checks to adapt to Zerg pressure.

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

### R01 — Production Tempo with Economy and Tech

**When:** At 4-6 minutes, if workers < 24 or production < 2 or bank > 1500, while preserving expansion/economy/tech identity.

**Correction:** Queue workers to 24+ on two bases, add a Barracks or Factory if production < 2, and spend bank on tech (e.g., Factory add-ons, Starport) or additional production, but do not expand beyond two bases until army supply >= 15 and production is active.

**Recheck:** Recheck at next decision cycle.

### R02 — Counter Zerg Ground Composition

**When:** If enemy composition shows Zergling/Queen with moderate production and light tech, or Zergling/Hydralisk with heavy tech, and your army lacks sufficient anti-ground or anti-light units.

**Correction:** Prioritize Hellions or Siege Tanks for Zergling/Queen; add Marauders or Siege Tanks for Hydralisk. Ensure at least 2 production structures on tech labs or add a Factory if needed. Maintain worker saturation and tech upgrades.

**Recheck:** Recheck at next decision cycle.

### R03 — Recovery from Low Army and High Bank

**When:** If army supply < 15 and bank > 1500, or predicted advantage is OverwhelmingDisadvantage, or owned zones threatened.

**Correction:** Immediately convert bank into army: queue Marines, Marauders, or Siege Tanks from all available production; add production structures if idle or insufficient. Do not expand or tech until army supply >= 15 and production is active. Prioritize defensive units and detection if needed.

**Recheck:** Recheck at next decision cycle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid greedy expansion without defense

**When:** Early-midgame, around 4 minutes, with heavy economy and production, ground forces (Marine, Reaper), and heavy tech. Enemy is on a ground macro posture with Zergling/Queen, moderate production, and light tech.

**Mistake → correction:** Expanding too greedily without proper defenses, or committing to an attack before your economy is stable. → Continue developing your economy and technology while strengthening your ground army. Maintain current defense and production.

**Why:** Your heavy tech and economy give you a long-term advantage. By continuing to develop, you can outscale the Zerg if they remain on a passive macro path.

**Read for full checks:** `N001`

### L02 — Avoid over-investing in air without scouting

**When:** Midgame, around 9 minutes, with heavy economy and production, Siege Tanks, Marines, and Hellions. Enemy is on a ground macro posture with Zergling/Queen, heavy production and tech.

**Mistake → correction:** Over-investing in air without proper scouting, or neglecting upgrades. → Continue strengthening your ground army and increase technology. Maintain economy and defense.

**Why:** Your Siege Tank-based army is strong against ground Zerg. Increasing tech will give you an edge in engagements.

**Read for full checks:** `N004`

### L03 — Avoid over-committing to attack without solid composition

**When:** Early-midgame, around 5-6 minutes, with heavy economy and production, Marines, Reapers, and Hellions. Enemy is on a ground macro posture with Zergling/Queen, moderate production and tech.

**Mistake → correction:** Over-committing to an attack before you have a solid army composition and upgrades, or neglecting scouting to detect tech switches. → Continue strengthening your ground army and increase technology. Maintain economy and defense.

**Why:** Hellions are effective against Zerglings and provide map control. Continuing to tech up will give you a strong midgame.

**Read for full checks:** `N007`

## Decision Nodes

### [DEFAULT] N001 — Early-Midgame Ground Macro with Heavy Tech

**Trigger situation:**  
Around 4 minutes, you have a heavy economy and production, with ground forces (Marine, Reaper) and heavy tech. Enemy is likely on a ground macro posture with Zergling/Queen, moderate production, and light tech.

**Direction:**  
Continue developing your economy and technology while strengthening your ground army. Maintain current defense and production.

**Read for details:** `N001`

---

### [POSITIVE] N002 — Late-Midgame Ground Strength with Siege Tanks

**Trigger situation:**  
Around 10 minutes, you have a strong ground army with Siege Tanks, Marines, and Hellions, heavy production and tech. Enemy is on a ground macro posture with Zergling/Queen, heavy production and tech.

**Direction:**  
Continue strengthening your ground army and increase technology investment. Maintain economy and defense.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Game Tech Development

**Trigger situation:**  
Around 3 minutes, you have a heavy economy and moderate production, with Reaper for scouting. Enemy is on a ground macro posture with Zergling/Queen, moderate production, and light tech.

**Direction:**  
Continue developing your economy and technology, and strengthen your ground army. Maintain current production.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground Macro with Siege Tanks

**Trigger situation:**  
Around 9 minutes, you have a heavy economy and production, with Siege Tanks, Marines, and Hellions. Enemy is on a ground macro posture with Zergling/Queen, heavy production and tech.

**Direction:**  
Continue strengthening your ground army and increase technology. Maintain economy and defense.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Ground Defense with Tech Advantage

**Trigger situation:**  
Around 7 minutes, you have a heavy economy and production, with Marines, Reapers, and Hellions. Enemy has a ground army with Zergling, Hydralisk, and Queen, heavy tech.

**Direction:**  
Continue strengthening your ground army and increase technology. Maintain economy and defense.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Late-Midgame Ground with Air Support

**Trigger situation:**  
Around 10 minutes, you have a heavy economy and production, with Marines, Reapers, Hellions, and Banshees. Enemy is on a ground macro posture with Zergling/Queen, heavy production and tech.

**Direction:**  
Continue strengthening your ground army and increase technology. Maintain economy and defense.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early-Midgame Ground with Hellions

**Trigger situation:**  
Around 5-6 minutes, you have a heavy economy and production, with Marines, Reapers, and Hellions. Enemy is on a ground macro posture with Zergling/Queen, moderate production and tech.

**Direction:**  
Continue strengthening your ground army and increase technology. Maintain economy and defense.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early Game Stabilization

**Trigger situation:**  
Around 3 minutes, you have a heavy economy and moderate production, with Marines and Reapers. Enemy has no reliable combat-unit cues, but is likely on a ground macro posture.

**Direction:**  
Stabilize your defense and continue developing your economy and technology. Increase production.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Stabilization with Heavy Production

**Trigger situation:**  
Around 7 minutes, you have a heavy economy and production, with Marines, Reapers, and Hellions. Enemy has a ground army with Zergling and Queen, heavy production and moderate tech.

**Direction:**  
Stabilize your defense and continue developing your economy and technology. Increase production.

**Read for details:** `N009`

---
