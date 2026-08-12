# PvP_O02 Technology / Economy / Production

## Skill Identity

- Skill ID: PvP_O02
- Matchup: Protoss vs Protoss
- Opening Family: technology / economy / production opening
- Method: Branch-Faithful Full V7

## Opening Strategy

A Protoss versus Protoss opening that emphasizes technology and economy development while keeping production flexible. Early game is marked by uncertainty in both armies, with a gradual shift toward heavier ground compositions and tech as the game progresses.

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

### R01 — Maintain tech-economy tempo with production scaling

**When:** At any time before 6 minutes, if bank is above 800 minerals and active production structures are fewer than 3, or if any production structure is idle while bank exceeds 400 minerals.

**Correction:** Queue units from existing production structures first; if all are busy and bank remains above 800, add a Gateway or tech structure that fits the opening's technology/economy identity. Prioritize ground units (Zealots, Stalkers) to keep army supply above 15 before considering expansions.

**Recheck:** Recheck at next decision cycle.

### R02 — Counter enemy ground composition with tech and ground army

**When:** If Enemy Intelligence shows a ground-heavy composition (Zealots, Stalkers, Immortals) and your army supply is below 20, or if you lack detection against potential DTs.

**Correction:** Strengthen ground army by queuing Zealots and Stalkers from existing Gateways; if tech allows, add an Immortal or Colossus. Ensure detection (Observer or Oracle) if enemy has stealth-capable units. Continue economy and tech development while maintaining a defensive posture.

**Recheck:** Recheck at next decision cycle.

### R03 — Recover from low army and high bank

**When:** If army supply is below 15 and bank exceeds 1000 minerals, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately convert bank into army by queuing units from all production structures; if production is insufficient, add Gateways (up to 2) and queue Zealots/Stalkers. Prioritize army over economy or tech until army supply is at least 20. Do not expand until army is stable.

**Recheck:** Recheck at next decision cycle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground Defense Priority

**When:** Early midgame, opponent has ground posture with Zealots, heavy economy, moderate production. You have moderate economy and heavy tech.

**Mistake → correction:** Overcommitting to air units or neglecting scouting, assuming the opponent lacks anti-air. → Strengthen your ground army and continue developing economy and technology. Maintain a defensive posture while preparing for a potential ground engagement.

**Why:** The opponent's ground posture suggests a Zealot-heavy army. Ground forces and tech advantage counter their composition.

**Read for full checks:** `N006`

### L02 — Balanced Ground and Tech

**When:** Late midgame, both you and opponent have ground posture with Zealots, Stalkers, Immortals. Both economies and production are heavy.

**Mistake → correction:** Neglecting air defense or overextending economy without adequate defense. → Continue to strengthen your ground army and develop economy and technology. Maintain a defensive posture while preparing for a potential large-scale engagement.

**Why:** Both sides have similar ground compositions. Continuing economy and tech development gives an advantage in upgrades or army size.

**Read for full checks:** `N008`

### L03 — Macro Defense with Unknown Composition

**When:** Early midgame, opponent has heavy economy and expansion, moderate production. You have moderate economy and heavy tech, with heavy expansion.

**Mistake → correction:** Overextending economy without adequate defense or neglecting scouting due to unknown composition. → Strengthen your ground army and continue to develop economy and technology. Maintain a defensive posture while preparing for a potential ground engagement.

**Why:** The opponent's heavy economy suggests a macro-oriented game. Ground forces and tech advantage counter their eventual army.

**Read for full checks:** `N009`

## Decision Nodes

### [DEFAULT] N001 — Early Game Development with Safety Checks

**Trigger situation:**  
At the start of the game, both sides have limited information. Your own production and tech are uncertain, and the opponent's posture is similarly unclear.

**Direction:**  
Maintain current development path with a focus on economy and technology. Keep production flexible to adapt to incoming information.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Late Midgame Development with Safety Checks

**Trigger situation:**  
In the late midgame, both sides have had time to develop. Your own posture remains uncertain, but the opponent's is also still unclear.

**Direction:**  
Continue to develop your economy and technology while maintaining a defensive posture. Keep your army composition flexible to respond to the opponent's eventual composition.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Midgame Development with Safety Checks

**Trigger situation:**  
In the early midgame, you have had time to develop your economy and tech. The opponent's posture is still uncertain, but you have some information.

**Direction:**  
Maintain your current development path, focusing on economy and technology. Keep production flexible to adapt to incoming information.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Development with Safety Checks

**Trigger situation:**  
In the midgame, both sides have had time to develop. Your own posture remains uncertain, but the opponent's is also still unclear.

**Direction:**  
Continue to develop your economy and technology while maintaining a defensive posture. Keep your army composition flexible to respond to the opponent's eventual composition.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game Stabilization and Development

**Trigger situation:**  
In the early game, you have a heavy defense posture and moderate economy, while the opponent has a heavy economy and moderate production. This suggests a potential tech or economic race.

**Direction:**  
Strengthen your ground army and increase your defense while continuing to develop your economy and technology. This is a stabilize-then-develop approach.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early Midgame Ground Development

**Trigger situation:**  
In the early midgame, the opponent has shown a ground posture with Zealots, and their economy is heavy. You have a moderate economy and heavy tech.

**Direction:**  
Strengthen your ground army and continue to develop your economy and technology. Maintain a defensive posture while preparing for a potential ground engagement.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Midgame Ground Stabilization

**Trigger situation:**  
In the midgame, the opponent has a ground posture with Zealots, and their economy and production are heavy. You have a moderate economy and heavy tech, but your expansion is heavy.

**Direction:**  
Strengthen your ground army and increase your defense while continuing to develop your economy and technology. This is a stabilize-then-develop approach.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Late Midgame Ground Development

**Trigger situation:**  
In the late midgame, both you and the opponent have a ground posture with Zealots, Stalkers, and Immortals. Both economies and production are heavy.

**Direction:**  
Continue to strengthen your ground army and develop your economy and technology. Maintain a defensive posture while preparing for a potential large-scale engagement.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Early Midgame Expansion Development

**Trigger situation:**  
In the early midgame, the opponent has a heavy economy and expansion, but their production is moderate. You have a moderate economy and heavy tech, with a heavy expansion.

**Direction:**  
Strengthen your ground army and continue to develop your economy and technology. Maintain a defensive posture while preparing for a potential ground engagement.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Midgame Ground Development with Upgrades

**Trigger situation:**  
In the midgame, both you and the opponent have a ground posture with Zealots and Stalkers. Both economies and production are heavy.

**Direction:**  
Continue to strengthen your ground army and increase your production and technology. Focus on upgrades to gain an edge in engagements.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Midgame Air Transition

**Trigger situation:**  
In the midgame, the opponent has a mixed posture with Zealots and Stalkers, and their economy is heavy. You have a moderate economy and heavy tech, but your expansion is uncertain.

**Direction:**  
Increase your air presence and strengthen your air army. Continue to develop your economy and technology while maintaining a defensive posture.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Midgame Ground Development

**Trigger situation:**  
In the midgame, the opponent has a mixed posture with Zealots and Stalkers, and their economy is heavy. You have a heavy economy and tech, with a heavy expansion.

**Direction:**  
Strengthen your ground army and continue to develop your economy and technology. Maintain a defensive posture while preparing for a potential ground engagement.

**Read for details:** `N012`

---
