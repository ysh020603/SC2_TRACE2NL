# ZvZ_O04 Economy / Defense / Ground

## Skill Identity

- Skill ID: ZvZ_O04
- Matchup: Zerg vs Zerg
- Opening Family: economy / defense / ground opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg versus Zerg opening that emphasizes a heavy economy and a defensive ground posture, with moderate production and light technology investment in the early game. The plan is to develop safely while keeping options open for adaptation based on scouting.

Develop a strong economy and a solid ground defense while maintaining flexibility to transition into either a ground or air composition depending on the opponent's actions.

This is a strategic template, not a fixed build order. Adapt based on live scouting and enemy intelligence.

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

### R01 — Maintain production tempo and convert bank into army

**When:** Time >= 240 and (army_supply < 15 or (bank >= 800 and (production_idle or production < 2))) and not (predicted_advantage == OverwhelmingDisadvantage)

**Correction:** If army_supply < 15, prioritize building army units from existing production structures; if production is idle or insufficient, add a production structure (e.g., Hatchery or Roach Warren) if prerequisites are met. If bank >= 800 and production is active, queue additional army units to convert resources. Do not expand unless army_supply >= 15 and production is sufficient.

**Recheck:** Recheck at next decision cycle.

### R02 — Adapt ground composition to enemy tech and air cues

**When:** Enemy intelligence shows ground posture with Roach cues or air presence with Mutalisk cues, and current army lacks appropriate counters.

**Correction:** If enemy has Roach cues, ensure you have Roach or Hydralisk production and add a Roach Warren or Hydralisk Den if prerequisites are met. If enemy has Mutalisk cues, add anti-air units (e.g., Hydralisks or Spore Crawlers) and consider transitioning to air if economy allows. Maintain ground army strength while teching.

**Recheck:** Recheck at next decision cycle.

### R03 — Recover from low army and high bank

**When:** army_supply < 15 and bank >= 1000 and (production_idle or production < 2) and (predicted_advantage == OverwhelmingDisadvantage or threatened_owned_zones)

**Correction:** Immediately convert bank into army by queuing units from existing production and adding production structures if needed. Prioritize defensive units and static defense if threatened. Do not expand or tech until army_supply >= 15 and production is active.

**Recheck:** Recheck at next decision cycle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Avoid Economy Complacency

**When:** Midgame, both players have heavy economies and heavy production. Opponent shows moderate tech and ground posture.

**Mistake → correction:** Tempting to just keep producing ground units and expanding economy without considering tech transitions or scouting for tech switches. → Continue to strengthen your ground army, maintain your economy and production, and keep your defense up. Consider adding tech when safe.

**Why:** With both players on heavy economies, the one who transitions more efficiently to a better composition will gain an advantage. Maintaining a strong ground army prevents being caught off guard.

**Read for full checks:** `N002`

### L02 — Late Midgame Ground: Avoid Tech Overcommitment

**When:** Late midgame, both players have heavy economies and heavy production. Opponent shows moderate tech and ground posture with Roach cues.

**Mistake → correction:** Tempting to over-invest in technology without sufficient army, or neglect scouting for tech switches. → Maintain your ground army and economy, continue to strengthen your ground forces, and consider adding upgrades or tech to gain an edge.

**Why:** With heavy tech, you can transition to a more powerful composition like Roach or Hydralisk. Maintaining a strong ground army keeps you safe while you tech up.

**Read for full checks:** `N004`

### L03 — Midgame vs Heavy Tech: Avoid Tech Race

**When:** Midgame, you have a heavy economy and heavy production, but the opponent shows heavy tech and a ground posture with Roach cues.

**Mistake → correction:** Tempting to over-invest in technology without sufficient army, or neglect scouting for tech switches. → Increase your defense and economy, continue your production and tech, and strengthen your ground army. Stabilize and prepare for a potential engagement.

**Why:** The opponent has heavy tech, so you need to ensure your army composition can handle theirs. Increasing defense and economy gives you the resources to tech up and outproduce them.

**Read for full checks:** `N005`

## Decision Nodes

### [DEFAULT] N001 — Early Ground Macro with Heavy Economy

**Trigger situation:**  
Early game, both players are on a ground macro posture with heavy economies. Opponent shows light or uncertain tech and moderate production.

**Direction:**  
Maintain your ground army and economy, strengthen your ground forces, and keep your defense solid. Continue developing with safety checks.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Sustain

**Trigger situation:**  
Midgame, both players have heavy economies and heavy production. Opponent shows moderate tech and ground posture.

**Direction:**  
Continue to strengthen your ground army, maintain your economy and production, and keep your defense up. Consider adding tech when safe.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Early Defense and Economy Boost

**Trigger situation:**  
Early game, you have a moderate economy and moderate expansion, while the opponent has a heavy economy. You need to stabilize and develop.

**Direction:**  
Increase your economy and defense, continue your expansion, and strengthen your ground army. Stabilize before pushing out.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late Midgame Ground Power

**Trigger situation:**  
Late midgame, both players have heavy economies and heavy production. Opponent shows moderate tech and ground posture with Roach cues.

**Direction:**  
Maintain your ground army and economy, continue to strengthen your ground forces, and consider adding upgrades or tech to gain an edge.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Defense and Tech

**Trigger situation:**  
Midgame, you have a heavy economy and heavy production, but the opponent shows heavy tech and a ground posture with Roach cues.

**Direction:**  
Increase your defense and economy, continue your production and tech, and strengthen your ground army. Stabilize and prepare for a potential engagement.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early Midgame Economy and Ground

**Trigger situation:**  
Early midgame, you have a moderate economy but a heavy expansion. Opponent shows a ground posture with moderate production.

**Direction:**  
Increase your economy, maintain your expansion and defense, and strengthen your ground army. Continue developing with safety checks.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early Midgame Expansion and Production

**Trigger situation:**  
Early midgame, you have a heavy economy and heavy expansion, while the opponent has a moderate economy. You can afford to be aggressive.

**Direction:**  
Increase your production and economy, continue your expansion, and strengthen your ground army. Consider applying pressure if you have an advantage.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early Midgame Tech Investment

**Trigger situation:**  
Early midgame, you have a heavy economy and heavy expansion, while the opponent shows heavy production and moderate tech.

**Direction:**  
Increase your tech and production, continue your expansion, and strengthen your ground army. Develop with safety checks.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Late Midgame Air Transition

**Trigger situation:**  
Late midgame, the opponent shows air presence with Mutalisk cues, while you have a ground army. You need to adapt.

**Direction:**  
Increase your defense and economy, continue your production and tech, and consider adding anti-air units or transitioning to air yourself.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Midgame Air Transition

**Trigger situation:**  
Midgame, you have air presence with Mutalisk cues, while the opponent shows a ground posture with heavy tech.

**Direction:**  
Increase your air presence and economy, continue your production and tech, and strengthen your air army. Use Mutalisks for harassment while building a ground defense.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Late Midgame Air and Ground

**Trigger situation:**  
Late midgame, you have air presence with Mutalisk cues, and the opponent shows a ground posture with heavy tech.

**Direction:**  
Continue to increase your air presence and economy, maintain your production and tech, and strengthen both your air and ground armies.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Early Game Production and Expansion

**Trigger situation:**  
Early game, you have a heavy economy but a moderate expansion, while the opponent shows a ground posture.

**Direction:**  
Increase your production and expansion, maintain your defense, and strengthen your ground army. Stabilize and develop.

**Read for details:** `N012`

---
