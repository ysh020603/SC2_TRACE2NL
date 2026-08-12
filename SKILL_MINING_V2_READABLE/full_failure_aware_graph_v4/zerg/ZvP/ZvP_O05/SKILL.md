# ZvP_O05 Economy / Expansion / Defense

## Skill Identity

- Skill ID: ZvP_O05
- Matchup: Zerg vs Protoss
- Opening Family: economy / expansion / defense opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg opening focused on economy, expansion, and defense, with a ground-leaning army and moderate production. Technology investment is light or uncertain early, but can develop later.

Develop a strong economy and defensive posture while maintaining flexibility to adapt to Protoss tech choices.

This is a strategic template, not a fixed build order.

## Strategic Characteristics

- Economy: heavy
- Production: moderate
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

### G05 — Zerg production interpretation

- Treat Hatchery/Lair/Hive count, larvae, Overlords, and worker/army larva competition as the production-capacity check.

## V4 Matchup-Specific Corrections

### R01 — Maintain production tempo and economy

**When:** At any time before 6 minutes, if army supply is below 15 and bank is above 1000, or if active production structures are fewer than 2 and bank is above 500.

**Correction:** Queue units from existing hatcheries, prioritizing Zerglings and Queens. If bank exceeds 1500 and no more than 2 bases, build an additional Hatchery at a natural expansion. Ensure worker production is continuous until 2 per mineral patch and 3 per gas geyser.

**Recheck:** Next decision cycle, verify army supply increased and bank decreased.

### R02 — Counter enemy composition

**When:** If enemy intelligence reveals a heavy air composition (e.g., Void Rays, Phoenixes, or Carriers) and own army lacks anti-air units.

**Correction:** Queue Hydralisks or Spore Crawlers at each base. If tech is not available, prioritize Lair and Hydralisk Den. Maintain ground army while adding anti-air. If enemy is heavy ground with Zealots/Stalkers, ensure Roach Warren and Roaches are available.

**Recheck:** Next decision cycle, verify anti-air units or structures are in production or completed.

### R03 — Recover from low army and high bank

**When:** If army supply is below 15 and bank is above 2000, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all available hatcheries, prioritizing Zerglings and Roaches. If production is insufficient, build additional Hatcheries. Do not expand or tech until army supply is above 30. If threatened, use Spine Crawlers for defense.

**Recheck:** Next decision cycle, verify army supply increased and bank decreased.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid tech overcommitment without scouting

**When:** Early midgame, own ground army with Zerglings, opponent unknown but heavy tech.

**Mistake → correction:** Over-committing to a specific tech path or army composition without more information, neglecting scouting or defensive positioning. → Continue developing economy and ground forces, increase production and expansions.

**Why:** Maintain economic lead while preparing for potential tech switches.

**Read for full checks:** `N001`

### L02 — Avoid neglecting scouting and over-investing in tech

**When:** Early game, own Queen, opponent unknown but heavy tech.

**Mistake → correction:** Neglecting scouting and over-investing in tech before confirming the opponent's plan. → Increase economy and expansions, continue ground development.

**Why:** Queens provide defense and creep spread, supporting a macro-oriented start.

**Read for full checks:** `N002`

### L03 — Avoid over-committing to Infestors without scouting for air

**When:** Late midgame, own Zergling/Infestor/Queen/Overseer, opponent ground with Zealots/Stalkers.

**Mistake → correction:** Over-committing to Infestors if the opponent transitions to air, and neglecting scouting to detect tech switches. → Maintain ground army, continue economy, consider upgrades.

**Why:** Infestors provide strong spellcasting against ground-based Protoss armies.

**Read for full checks:** `N005`

## Decision Nodes

### [DEFAULT] N001 — Early Midgame Ground Development

**Trigger situation:**  
Early midgame, own ground army with Zerglings, opponent unknown but heavy tech.

**Direction:**  
Continue developing economy and ground forces, increase production and expansions.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early Game Queen Focus

**Trigger situation:**  
Early game, own Queen, opponent unknown but heavy tech.

**Direction:**  
Increase economy and expansions, continue ground development.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Army with Roaches

**Trigger situation:**  
Early midgame, own Zergling/Roach/Queen, opponent ground with Stalkers.

**Direction:**  
Maintain ground army, continue economy, consider tech upgrades.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early Midgame Queen Defense

**Trigger situation:**  
Early midgame, own Queen, opponent unknown but heavy tech.

**Direction:**  
Maintain economy and defense, continue ground development.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Late Midgame Infestor Tech

**Trigger situation:**  
Late midgame, own Zergling/Infestor/Queen/Overseer, opponent ground with Zealots/Stalkers.

**Direction:**  
Maintain ground army, continue economy, consider upgrades.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early Game Zergling Pressure

**Trigger situation:**  
Early game, own Zerglings, opponent unknown but heavy tech.

**Direction:**  
Increase economy and expansions, maintain ground forces.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Midgame Roach Queen Defense

**Trigger situation:**  
Midgame, own Roach/Queen, opponent ground with Stalkers and Void Rays.

**Direction:**  
Maintain ground army, consider adding anti-air if Void Rays become a threat.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Air Transition

**Trigger situation:**  
Midgame, own Zergling/Infestor/Queen/Overseer, opponent air with Phoenixes.

**Direction:**  
Increase economy and tech, consider adding anti-air units.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Early Midgame Ground Push

**Trigger situation:**  
Early midgame, own Zergling/Queen, opponent ground with Zealots/Stalkers.

**Direction:**  
Increase economy and production, continue ground development.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Midgame Mutalisk Harass

**Trigger situation:**  
Midgame, own Zergling/Mutalisk/Queen, opponent ground with Zealots/Stalkers/Sentries.

**Direction:**  
Increase air presence, continue economy, consider upgrades.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Midgame Ground Tech

**Trigger situation:**  
Midgame, own Zergling/Roach/Queen, opponent ground with Zealots/Stalkers.

**Direction:**  
Increase economy and tech, continue ground development.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Early Game Zealot Defense

**Trigger situation:**  
Early game, own Zerglings, opponent ground with Zealots.

**Direction:**  
Increase economy and expansions, maintain ground forces.

**Read for details:** `N012`

---
