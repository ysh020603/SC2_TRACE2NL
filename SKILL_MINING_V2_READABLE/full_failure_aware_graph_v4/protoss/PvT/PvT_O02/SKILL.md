# PvT_O02 Technology / Economy / Production

## Skill Identity

- Skill ID: PvT_O02
- Matchup: Protoss vs Terran
- Opening Family: technology / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A flexible Protoss opening that prioritizes technology and economy while keeping production options open. Early game is characterized by light or uncertain information, with a gradual shift toward a ground-oriented army and heavier production as the game progresses.

Develop a technology / economy / production posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

## Strategic Characteristics

- Economy: light_or_uncertain
- Production: light_or_uncertain
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

### G05 — Protoss production interpretation

- Scale Gateways or other unit-producing tech only after power, prerequisites, and production capacity are executable.

## V4 Matchup-Specific Corrections

### R01 — Maintain production tempo and tech progression

**When:** Time >= 240 and (army_supply < 15 or production < 3 or bank > 1000) and not OverwhelmingDisadvantage

**Correction:** Prioritize adding production structures (Gateways or Robo) up to at least 3 active production facilities, and queue units to keep them busy. If tech prerequisites are missing, build the required structure (e.g., Twilight Council or Robotics Facility) before queuing advanced units. Convert excess minerals into additional production or tech, and keep workers mining. Avoid expanding until production is sufficient and army supply is at least 15.

**Recheck:** Next decision cycle: verify production count >= 3, army supply >= 15, and bank < 1000.

### R02 — Counter enemy ground composition with detection and splash

**When:** Enemy Intelligence shows ground posture with Marine, Marauder, SiegeTank, Reaper, Thor, or Medivac, and army supply < 30

**Correction:** Strengthen ground forces by producing units that counter the observed composition: add Colossus or High Templar for bio, Immortals for tanks, and ensure detection (Observer) if cloaked units are possible. Maintain a defensive posture near your bases, and continue expanding economy and production to support a larger army. If Medivacs are present, consider Stalkers or Phoenix for anti-air.

**Recheck:** Next decision cycle: verify army supply >= 30 and that you have at least one detection unit and appropriate counter units.

### R03 — Recover from low army and high bank

**When:** army_supply < 15 and bank > 1500 and (predicted_advantage == OverwhelmingDisadvantage or threat_flags indicate imminent attack)

**Correction:** Immediately convert bank into army: queue units from all available production structures, and if production is insufficient, build additional Gateways or Robo facilities. Prioritize defensive units (e.g., Zealots, Stalkers) and ensure you have a defensive structure (e.g., Shield Battery) if threatened. Do not expand or tech greedily until army supply is at least 15 and the threat is mitigated.

**Recheck:** Next decision cycle: verify army supply >= 15 and bank < 1000, or threat flags cleared.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Stabilize before pushing

**When:** Early-midgame, around 240 seconds, with heavy defense and moderate economy, while the opponent shows a ground posture with Marine cues.

**Mistake → correction:** Over-committing to offense before your defense is solid, potentially leaving you vulnerable to a ground attack. → Increase economy and technology. Strengthen ground forces. Increase defense. Maintain expansion. Continue production.

**Why:** The opponent's ground posture suggests a potential ground attack. Stabilizing your defense while developing your economy and tech is prudent.

**Read for full checks:** `N008`

### L02 — Balanced development under uncertainty

**When:** Early-midgame, around 300-360 seconds, with heavy defense and moderate economy, while the opponent's posture is unknown.

**Mistake → correction:** Over-committing to offense before your defense is solid, risking vulnerability when the opponent's intentions are unclear. → Increase economy and technology. Strengthen ground forces. Increase defense. Maintain expansion. Continue production.

**Why:** With limited information, balanced development keeps options open. Strengthening ground forces provides a solid base for any transition.

**Read for full checks:** `N011`

### L03 — Maintain ground defense against drops

**When:** Late-midgame, around 600 seconds, with heavy economy and production, while the opponent shows a ground posture with SiegeTank, Reaper, Thor, and Medivac.

**Mistake → correction:** Neglecting ground defense, leaving you vulnerable to drops or flanking maneuvers. → Increase economy, production, and technology. Strengthen ground forces. Maintain defense and expansion. Continue air development.

**Why:** The opponent's ground posture suggests a potential ground attack. Strengthening ground forces and maintaining defense is prudent while continuing development.

**Read for full checks:** `N010`

## Decision Nodes

### [DEFAULT] N001 — Early-Midgame Development with Safety Checks

**Trigger situation:**  
At around 240-360 seconds, both sides have limited information. Your own posture is light or uncertain, while the opponent's is also unclear. The main goal is to develop your economy and technology while maintaining a defensive stance.

**Direction:**  
Increase economy, production, and technology. Strengthen ground forces. Maintain defense and expansion. Continue air development.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early Game Development with Safety Checks

**Trigger situation:**  
At around 180 seconds, both sides are in the early game with minimal information. Your own posture is light or uncertain, and the opponent's is also unclear. The focus is on establishing a solid economy and tech base.

**Direction:**  
Increase economy, production, and technology. Strengthen ground forces. Maintain defense and expansion. Continue air development.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Development with Safety Checks

**Trigger situation:**  
At around 420-540 seconds, the game enters the midgame. Information is still limited, but you have had time to develop your economy and tech. The focus remains on balanced growth.

**Direction:**  
Increase economy, production, and technology. Strengthen ground forces. Maintain defense and expansion. Continue air development.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Development with Safety Checks

**Trigger situation:**  
At around 600 seconds, the game is in the late-midgame. Information is still limited, but you have had time to develop your economy and tech. The focus remains on balanced growth.

**Direction:**  
Increase economy, production, and technology. Strengthen ground forces. Maintain defense and expansion. Continue air development.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early-Midgame Ground Defense and Tech

**Trigger situation:**  
At around 240-360 seconds, you have a moderate economy and heavy expansion, while the opponent shows a ground posture with heavy production and tech. You need to strengthen your ground forces and maintain defense.

**Direction:**  
Increase economy, production, and technology. Strengthen ground forces. Maintain defense and expansion. Continue air development.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early Game Defensive Tech

**Trigger situation:**  
At around 180 seconds, you have a heavy defense and moderate economy, while the opponent shows a heavy economy and expansion with a Reaper cue. You need to stabilize and develop.

**Direction:**  
Increase economy and technology. Strengthen ground forces. Increase defense. Maintain expansion. Continue production.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Midgame Ground Army and Tech

**Trigger situation:**  
At around 420-540 seconds, you have a heavy economy and production, while the opponent shows a ground posture with Marine and Marauder. You need to strengthen your ground forces and maintain defense.

**Direction:**  
Increase economy, production, and technology. Strengthen ground forces. Maintain defense and expansion. Continue air development.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early-Midgame Defensive Tech

**Trigger situation:**  
At around 240 seconds, you have a heavy defense and moderate economy, while the opponent shows a ground posture with Marine cue. You need to stabilize and develop.

**Direction:**  
Increase economy and technology. Strengthen ground forces. Increase defense. Maintain expansion. Continue production.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Defensive Tech

**Trigger situation:**  
At around 420 seconds, you have a heavy defense and moderate economy, while the opponent shows a ground posture with Marine and Marauder. You need to stabilize and develop.

**Direction:**  
Increase economy and technology. Strengthen ground forces. Increase defense. Maintain expansion. Continue production.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Late-Midgame Ground Army and Tech

**Trigger situation:**  
At around 600 seconds, you have a heavy economy and production, while the opponent shows a ground posture with SiegeTank, Reaper, Thor, and Medivac. You need to strengthen your ground forces and maintain defense.

**Direction:**  
Increase economy, production, and technology. Strengthen ground forces. Maintain defense and expansion. Continue air development.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early-Midgame Defensive Tech

**Trigger situation:**  
At around 300-360 seconds, you have a heavy defense and moderate economy, while the opponent's posture is unknown. You need to stabilize and develop.

**Direction:**  
Increase economy and technology. Strengthen ground forces. Increase defense. Maintain expansion. Continue production.

**Read for details:** `N011`

---
