# PvT_O05 Technology / Economy / Expansion

## Skill Identity

- Skill ID: PvT_O05
- Matchup: Protoss vs Terran
- Opening Family: technology / economy / expansion opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Protoss opening that emphasizes heavy technology investment and economic expansion while keeping production moderate in the early game. The plan is to develop a strong tech-based army and economy, then transition into a heavier production and ground-oriented composition as the game progresses.

Develop a technology / economy / expansion posture while preserving flexibility for live observation-driven adaptation.

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

### R01 — Maintain Tech-Economy Tempo with Production Scaling

**When:** Game time 4-6 minutes, bank above 800 minerals, production structures fewer than 3, and army supply below 20.

**Correction:** Prioritize adding Gateway or Robotic Facility production to convert bank into army. Keep tech buildings (Twilight Council, Forge) queued if prerequisites are met. Avoid expanding until production is active and army supply is at least 15.

**Recheck:** Recheck at next decision cycle: if bank remains above 800 and production is still insufficient, continue adding production and reinforcing army.

### R02 — Counter Terran Bio with Splash and Vision

**When:** Enemy Intelligence shows Marines, Marauders, or Medivacs, and you have at least one Robotics Facility or Templar Archives.

**Correction:** Queue Colossus or High Templar (if Archives) to counter bio. Add Observer for vision if not already present. Maintain ground army strength and continue tech upgrades.

**Recheck:** Recheck at next decision cycle: if enemy composition remains bio-heavy, continue producing splash units and ensure detection is available.

### R03 — Recover from Low Army and High Bank

**When:** Army supply below 15, bank above 1000 minerals, and production is idle or insufficient, or predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all available production structures. If production is insufficient, add Gateways or Robotic Facilities. Prioritize army over expansion or tech. Do not expand until army supply is at least 15 and production is active.

**Recheck:** Recheck at next decision cycle: if army supply is still low and bank remains high, continue reinforcing and adding production.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid neglecting air defense while pushing ground

**When:** Early-mid game (4-6 min) with both sides ground-oriented, opponent has Marines, you have Stalkers and Sentries.

**Mistake → correction:** Focusing solely on ground strength and production, ignoring potential air transitions and overextending without scouting. → Continue strengthening ground army, increase production, maintain economy and tech lead, expand, and add Observers for vision.

**Why:** Opponent likely bio-based ground; your Stalkers/Sentries are solid, tech advantage allows later transitions.

**Read for full checks:** `N002`

### L02 — Avoid neglecting upgrades and positioning in late-midgame

**When:** Late-midgame (10-12 min) with heavy production/tech, opponent has Marines, Reapers, Marauders, Medivacs; you have Colossus, Zealots, Stalkers, Sentries.

**Mistake → correction:** Neglecting upgrades and being caught out of position, allowing a timing attack. → Continue strengthening ground army, increase production, maintain economy/tech, consider High Templar for Storm or mixed composition.

**Why:** Your army is well-rounded with Colossus splash and Zealot tanking; heavy economy sustains large army and upgrades.

**Read for full checks:** `N004`

### L03 — Avoid assuming enemy build without scouting

**When:** Early game (~3 min) with heavy economy/tech, moderate production, unclear army composition, opponent may show Reaper.

**Mistake → correction:** Making assumptions about enemy build without scouting and neglecting defense while teching. → Continue developing economy/tech, increase production, strengthen ground army, maintain defensive posture while expanding.

**Why:** This opening prioritizes long-term advantages; light defense is sufficient as opponent's posture is unclear.

**Read for full checks:** `N001`

## Decision Nodes

### [DEFAULT] N001 — Early Game Tech and Economy Foundation

**Trigger situation:**  
Early game, around 3 minutes, with both sides having heavy economy and technology investment, moderate production, and no clear army composition yet.

**Direction:**  
Continue developing your economy and technology, increase production, and strengthen your ground army. Maintain a defensive posture while expanding.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Mid Game Ground Transition

**Trigger situation:**  
Early-mid game, around 4-6 minutes, with both sides transitioning to a ground-oriented army. Opponent shows Marines, and you have Stalkers and Sentries.

**Direction:**  
Continue strengthening your ground army, increase production, and maintain your economy and tech lead. Keep expanding and consider adding Observers for vision.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Mid-Game Tech Army Assembly

**Trigger situation:**  
Mid-game, around 9 minutes, with both sides having heavy production and tech. Opponent shows a ground army with Marines, Reapers, Marauders, and Medivacs. You have Colossus, Stalkers, Sentries, and Warp Prism.

**Direction:**  
Continue strengthening your ground army, increase production, and maintain your economy and tech. Consider adding more Colossus or transitioning to High Templar for additional spell damage.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Consolidation

**Trigger situation:**  
Late-midgame, around 10-12 minutes, with both sides having heavy production and tech. Opponent shows a ground army with Marines, Reapers, Marauders, and Medivacs. You have Colossus, Zealots, Stalkers, and Sentries.

**Direction:**  
Continue strengthening your ground army, increase production, and maintain your economy and tech. Consider adding High Templar for Storm or transitioning to a more mixed composition if needed.

**Read for details:** `N004`

---
