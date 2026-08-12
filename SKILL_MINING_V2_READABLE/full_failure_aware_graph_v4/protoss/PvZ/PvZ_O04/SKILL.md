# PvZ_O04 Technology / Economy / Production

## Skill Identity

- Skill ID: PvZ_O04
- Matchup: Protoss vs Zerg
- Opening Family: technology / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Protoss opening that emphasizes heavy technology and economy while keeping production moderate, aiming to develop a strong mid-game position with flexible army composition.

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

### G05 — Protoss production interpretation

- Scale Gateways or other unit-producing tech only after power, prerequisites, and production capacity are executable.

## V4 Matchup-Specific Corrections

### R01 — Maintain Production Tempo and Tech Progression

**When:** At any time before 6 minutes, if army supply is below 15 and bank exceeds 800 minerals, or if production structures are fewer than 3 and tech structures are fewer than 2.

**Correction:** Prioritize building additional Gateways and a Robotics Facility or Stargate if prerequisites are met. Queue units from existing production structures to avoid idle time. Continue worker production until saturation (around 2 per base). Ensure supply providers are added just in time to avoid supply blocks.

**Recheck:** Recheck at next decision cycle: verify production structures count, active queues, and bank. If bank remains high and production is still insufficient, add more production structures.

### R02 — Adapt to Zerg Ground Composition with Anti-Air

**When:** If enemy intelligence reveals a ground-heavy composition with Zerglings, Roaches, or Queens, and no significant air threat, while own army lacks sufficient anti-air capability.

**Correction:** Continue building ground forces (Zealots, Stalkers, Immortals) but include Stalkers or prepare a transition to Void Rays if enemy tech suggests air. Maintain Observer for detection if needed. Keep economy and tech development steady.

**Recheck:** Recheck at next decision cycle: reassess enemy composition and own anti-air count. If enemy air units appear, prioritize Stalkers or Phoenixes.

### R03 — Recover from Low Army and High Bank

**When:** If army supply is below 15 and bank exceeds 1000 minerals, or if predicted advantage is OverwhelmingDisadvantage, or if any owned base is threatened.

**Correction:** Immediately convert bank into army by queuing units from all production structures and building additional production if needed. Prioritize defensive units (Zealots, Stalkers) and ensure supply is not blocked. Do not expand or invest in tech until army supply is above 15 and threat is mitigated.

**Recheck:** Recheck at next decision cycle: verify army supply increased and bank reduced. If still low army, continue production and consider building defensive structures.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Maintain Ground Strength with Anti-Air

**When:** Midgame, own ground posture with Zealots, Stalkers, Observers, Immortals; opponent ground with Zerglings, Queens, Overseers; both heavy tech.

**Mistake → correction:** Focusing solely on ground forces and neglecting anti-air, leaving you vulnerable to a potential air transition. → Continue strengthening ground forces, maintain economy and tech, and consider upgrades. Keep some Stalkers or prepare for air transition.

**Why:** A strong ground presence counters the opponent's ground army and tech, while retaining anti-air capability prevents being caught off guard.

**Read for full checks:** `N003`

### L02 — Leverage Early Air Tech

**When:** Early-mid game, own mixed posture with Void Rays; opponent ground with Zerglings and Queens; both heavy economy.

**Mistake → correction:** Overcommitting to air forces and neglecting ground defense, leaving bases exposed to ground harassment. → Increase air forces, strengthen air army, continue economy and tech. Keep some ground units to protect bases.

**Why:** Early air tech provides an advantage over a ground-focused opponent, but ground defense is essential to secure your economy.

**Read for full checks:** `N008`

### L03 — Stabilize Before Expanding

**When:** Midgame, own ground posture with Zealots; opponent ground with Zerglings and Queens; both heavy economy.

**Mistake → correction:** Pushing out aggressively with your tech advantage without ensuring a stable defensive position. → Stabilize then develop, increase production and tech, maintain defense.

**Why:** Ensuring a stable position before committing to further development prevents overextension and allows safe growth.

**Read for full checks:** `N009`

## Decision Nodes

### [DEFAULT] N001 — Early Game Tech Development

**Trigger situation:**  
Early game, own posture unknown or ground-oriented, opponent ground posture with light tech, both heavy economy.

**Direction:**  
Strengthen ground forces, increase economy and technology, maintain defense and expansions.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Mid Ground Consolidation

**Trigger situation:**  
Early-mid game, own ground posture with Zealots and Stalkers, opponent ground with Zerglings and Queens, both heavy economy.

**Direction:**  
Continue strengthening ground forces, increase economy and production, maintain tech development.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Tech

**Trigger situation:**  
Midgame, own ground posture with Zealots, Stalkers, Observers, Immortals, opponent ground with Zerglings, Queens, Overseers, both heavy tech.

**Direction:**  
Continue strengthening ground forces, maintain economy and tech, consider upgrades.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Mid Ground Stability

**Trigger situation:**  
Late-mid game, own ground posture with Zealots and Stalkers, opponent ground with Zerglings, Roaches, Queens, both heavy tech.

**Direction:**  
Maintain ground strength, continue economy and tech, consider defensive upgrades.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early-Mid Tech Expansion

**Trigger situation:**  
Early-mid game, own ground posture with Stalkers and Sentries, opponent ground with Zerglings and Queens, both heavy economy.

**Direction:**  
Increase economy and expansions, continue production and tech, strengthen ground forces.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Midgame Air Transition

**Trigger situation:**  
Midgame, own air posture with Phoenixes, opponent ground with Zerglings, Queens, Overseers, both heavy tech.

**Direction:**  
Increase air forces, strengthen air army, continue economy and tech.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early Game Defensive Tech

**Trigger situation:**  
Early game, own ground posture with Zealots, opponent ground with Queens, both heavy economy.

**Direction:**  
Increase economy and expansions, continue production and tech, maintain defense.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early-Mid Air Tech

**Trigger situation:**  
Early-mid game, own mixed posture with Void Rays, opponent ground with Zerglings and Queens, both heavy economy.

**Direction:**  
Increase air forces, strengthen air army, continue economy and tech.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Stabilization

**Trigger situation:**  
Midgame, own ground posture with Zealots, opponent ground with Zerglings and Queens, both heavy economy.

**Direction:**  
Stabilize then develop, increase production and tech, maintain defense.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Late-Mid Air Dominance

**Trigger situation:**  
Late-mid game, own air posture with Phoenixes, opponent ground with Mutalisks, Roaches, Queens, both heavy tech.

**Direction:**  
Increase air forces, strengthen air army, continue economy and tech.

**Read for details:** `N010`

---
