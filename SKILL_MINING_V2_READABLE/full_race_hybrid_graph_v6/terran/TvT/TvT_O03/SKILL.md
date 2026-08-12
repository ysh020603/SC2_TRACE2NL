# TvT_O03 Technology / Economy / Upgrade

## Skill Identity

- Skill ID: TvT_O03
- Matchup: Terran vs Terran
- Opening Family: technology / economy / upgrade opening
- Method: Race-Hybrid Full V6

## Opening Strategy

A Terran mirror opening that prioritizes heavy technology and economy development with moderate production, aiming for a strong midgame position.

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

### R01 — Production Tempo and Tech/Economy Balance

**When:** Time between 240 and 360, workers below 30, army supply below 10, bank above 1000, production below 3, and no active threat.

**Correction:** Prioritize worker production from all Command Centers, queue SCVs continuously until saturation. Add a Barracks or Factory if production is below 3 and prerequisites are met. If bank exceeds 1500 and production is active, start an Engineering Bay or Armory upgrade. Do not expand until army supply is at least 15 and production is not idle.

**Recheck:** Recheck at next decision cycle: workers increased, production count increased, bank reduced, and army supply improved.

### R02 — Enemy Composition Response

**When:** Enemy Intelligence indicates a heavy air composition (e.g., Banshees, Vikings, Battlecruisers) or a heavy ground composition with Siege Tanks, and own army lacks appropriate counters.

**Correction:** If enemy air is detected, add a Starport with Tech Lab and produce Vikings or Ravens, and ensure at least one Missile Turret per base. If enemy ground is heavy with Siege Tanks, add Siege Tanks or Marauders with Concussive Shells, and consider a Raven for detection. Maintain production of core ground units (Marines, Marauders) while adding counters.

**Recheck:** Recheck at next decision cycle: counter units in production or completed, detection available if needed, and army composition adjusted.

### R03 — Recovery from Low Army and High Bank

**When:** Army supply below 15, bank above 2000, production idle or insufficient, or predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all available production structures, prioritizing combat units (Marines, Marauders, Siege Tanks). If production is insufficient, add Barracks or Factories as prerequisites allow. Convert bank into army by starting upgrades that directly improve combat effectiveness (e.g., Stim, +1 weapons). Do not expand or tech up until army supply is at least 15 and production is active.

**Recheck:** Recheck at next decision cycle: army supply increased, bank reduced, production active, and no idle production structures.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Avoid Tech Tunnel Vision

**When:** Early-midgame, both sides ground-oriented with heavy production and tech; own army strong.

**Mistake → correction:** Overcommitting to a single tech path without scouting, neglecting defense against possible aggression. → Continue strengthening ground forces, increase economy and expansions, and maintain technology development.

**Why:** Leverage economic and tech advantage to build a strong ground army while expanding safely.

**Read for full checks:** `N002`

### L02 — Unknown vs Ground: Avoid Passive Defense

**When:** Early game, own posture unknown with moderate production and heavy tech; opponent ground with heavy defense and economy.

**Mistake → correction:** Staying too defensive for too long, neglecting expansion and map control, and failing to scout for tech switches. → Strengthen ground forces while increasing economy and maintaining production.

**Why:** Build a safe economic and tech lead while preparing for potential early aggression.

**Read for full checks:** `N004`

### L03 — Ground vs Ground: Avoid Drastic Changes

**When:** Early-midgame, own ground-oriented with moderate production and heavy tech; opponent heavy production and possible pressure.

**Mistake → correction:** Making drastic changes to army composition or tech without information, overcommitting to a countered path. → Maintain current army path and continue developing with safety checks.

**Why:** Avoid unnecessary deviations while ensuring defenses are adequate against possible pressure.

**Read for full checks:** `N005`

## Decision Nodes

### [DEFAULT] N001 — Early Tech/Economy Foundation

**Trigger situation:**  
Early game, own posture unknown-oriented with moderate production and heavy tech investment; opponent appears ground-oriented with light defense and heavy economy.

**Direction:**  
Strengthen ground forces while increasing economy and continuing technology development.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Ground Macro Development

**Trigger situation:**  
Early-midgame, own posture ground-oriented with heavy production and tech; opponent also ground-oriented with heavy production and possible pressure.

**Direction:**  
Continue strengthening ground forces, increase economy and expansions, and maintain technology development.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Army Consolidation

**Trigger situation:**  
Midgame, both sides have heavy ground-oriented macro postures with heavy production and tech; own army includes Marines, Marauders, Medivacs.

**Direction:**  
Increase air presence and technology while continuing to strengthen ground forces and economy.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early Defensive Tech

**Trigger situation:**  
Early game, own posture unknown-oriented with moderate production and heavy tech; opponent has heavy defense and heavy economy.

**Direction:**  
Strengthen ground forces while increasing economy and maintaining production.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Stabilized Ground Midgame

**Trigger situation:**  
Early-midgame, own posture ground-oriented with moderate production and heavy tech; opponent has heavy production and possible pressure.

**Direction:**  
Maintain current army path and continue developing with safety checks.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Late-Midgame Air Transition

**Trigger situation:**  
Late-midgame, own posture ground-oriented with heavy production and tech, moderate air presence; opponent ground-oriented with heavy defense.

**Direction:**  
Increase air presence and strengthen air forces while continuing to expand and tech up.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early-Midgame Ground Reinforcement

**Trigger situation:**  
Early-midgame, own posture ground-oriented with moderate production and heavy tech; opponent has heavy production and possible pressure.

**Direction:**  
Strengthen ground forces while increasing economy and maintaining production.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early Expansion and Tech

**Trigger situation:**  
Early game, own posture unknown-oriented with moderate production and heavy tech; opponent has light defense and heavy economy.

**Direction:**  
Strengthen ground forces, increase economy and expansions, and continue technology development.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Ground Stability

**Trigger situation:**  
Midgame, own posture ground-oriented with heavy production and tech; opponent has heavy defense and heavy economy.

**Direction:**  
Strengthen ground forces while increasing economy and production.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Midgame Ground Army with Siege Tanks

**Trigger situation:**  
Midgame, own posture ground-oriented with heavy production and tech; opponent has heavy defense and moderate air presence.

**Direction:**  
Strengthen ground forces while maintaining economy and technology development.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Late-Midgame Ground Defense

**Trigger situation:**  
Late-midgame, own posture ground-oriented with heavy production and tech; opponent has heavy defense and moderate air presence.

**Direction:**  
Strengthen ground forces, increase defense, economy, and expansions.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Midgame Ground Army with Medivacs

**Trigger situation:**  
Midgame, own posture ground-oriented with heavy production and tech; opponent has heavy defense and moderate air presence.

**Direction:**  
Maintain current army path and continue developing with safety checks.

**Read for details:** `N012`

---
