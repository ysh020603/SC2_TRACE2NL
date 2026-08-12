# PvP_O03 Technology / Defense / Economy

## Skill Identity

- Skill ID: PvP_O03
- Matchup: Protoss vs Protoss
- Opening Family: technology / defense / economy opening
- Method: Prompt-Executable Full V9

## Opening Strategy

A Protoss versus Protoss opening that prioritizes heavy technology investment, a solid defensive posture, and a growing economy. The early game is characterized by moderate production and an unknown army composition, with the flexibility to transition into either a ground or air-oriented midgame depending on scouting information.

Develop a technology / defense / economy posture while preserving flexibility for live observation-driven adaptation.

This is a strategic template, not a fixed build order.

## Strategic Characteristics

- Economy: moderate
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

### R01 — Maintain production tempo and tech investment

**When:** At any time before 6 minutes, if active production structures are fewer than 2 or if a tech structure (e.g., Twilight Council, Robotics Facility, Stargate) is not completed or queued, and bank is above 300 minerals.

**Correction:** Queue a Gateway unit if a Gateway is available and not already queued; otherwise, start a Gateway if prerequisites are met. If a tech structure is missing, start one if prerequisites are met. Ensure at least 2 production structures are active or queued. Recheck at next decision cycle.

**Recheck:** At 6 minutes, verify at least 2 production structures are active and at least one tech structure is completed or queued.

### R02 — Counter enemy composition with appropriate tech

**When:** If enemy intelligence reveals a ground-heavy composition (Zealots, Stalkers, Immortals) and your army lacks spell casters (e.g., High Templar) or anti-air, or if enemy shows air units (Void Rays, Oracles) and your army lacks anti-air (e.g., Stalkers, Void Rays, Phoenix).

**Correction:** If enemy is ground-heavy and you lack spell casters, start a Twilight Council if prerequisites are met, then queue High Templar tech. If enemy has air units and you lack anti-air, start a Stargate if prerequisites are met, then queue Phoenix or Void Rays. Recheck at next decision cycle.

**Recheck:** At next decision cycle, confirm the appropriate tech structure is completed or queued and that at least one counter unit is in production or queued.

### R03 — Recover from low army and high bank

**When:** If army supply is below 15 and bank (minerals + gas) is above 1000, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all available production structures, prioritizing combat units (e.g., Zealots, Stalkers). If production structures are idle or insufficient, start additional Gateways if prerequisites are met. Do not expand or invest in technology until army supply is at least 15 and bank is below 500. Recheck at next decision cycle.

**Recheck:** At next decision cycle, verify army supply is at least 15 and bank is below 500, or that production is actively queued.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Avoid Overcommitting Without Anti-Air

**When:** Midgame (7-9 minutes), opponent shows ground posture (Zealots, Stalkers), your army is ground-oriented with Zealots and Immortals.

**Mistake → correction:** Tempting to blindly strengthen ground forces and continue production without considering anti-air, risking vulnerability to an air transition. → Continue strengthening ground army and economy, but maintain defensive posture and consider adding tech like High Templar for spell support.

**Why:** Ground army with Immortals is strong vs enemy ground, especially armored units. Solid economy enables further tech and expansion.

**Read for full checks:** `N004`

### L02 — Ground vs Ground with Oracles: Avoid Ignoring Spell Support

**When:** Late-midgame (10-12 minutes), opponent shows ground posture (Zealots, Stalkers, Immortals, Oracles), your army is ground-oriented with Zealots.

**Mistake → correction:** Tempting to continue pure ground production without adding spell casters, missing opportunities to counter enemy composition. → Continue strengthening ground army and economy, but add tech like High Templar for spell support and maintain defensive posture.

**Why:** Zealots alone can be countered; High Templar provide spell support and improve composition. Economy allows further tech and expansion.

**Read for full checks:** `N007`

### L03 — Air vs Air: Avoid Neglecting Ground Defense

**When:** Late-midgame (10-12 minutes), opponent shows air posture (Zealots, Stalkers, Void Rays, Oracles), your army is air-oriented with Void Rays.

**Mistake → correction:** Tempting to overcommit to air units without ensuring ground defense, risking vulnerability to ground transitions. → Continue strengthening air army and economy, but maintain defensive posture and consider adding tech like Tempests for late-game.

**Why:** Air army with Void Rays is powerful vs air-oriented opponent. Strong economy enables further tech and expansion.

**Read for full checks:** `N009`

## Decision Nodes

### [DEFAULT] N001 — Early Game Stabilization

**Trigger situation:**  
Early game, around 3 minutes, with both players having heavy technology investment and moderate production. Opponent posture is unknown, but economy is heavy.

**Direction:**  
Continue developing your economy and technology while maintaining a defensive posture. Strengthen your ground army as a baseline, but remain flexible to transition to air if scouting suggests.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Midgame Ground Commitment

**Trigger situation:**  
Early-midgame, around 5-6 minutes, with the opponent showing a ground posture (Zealots observed). Your own army is still undefined, but you have a heavy economy and defense.

**Direction:**  
Strengthen your ground army to match the opponent's ground-oriented composition. Continue increasing your economy and technology, and maintain a defensive posture.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Air Transition

**Trigger situation:**  
Midgame, around 9 minutes, with the opponent showing a ground posture (Zealots, Stalkers, Oracles). Your own army has transitioned to an air-heavy composition with Void Rays.

**Direction:**  
Continue strengthening your air army and increasing your economy. Maintain a defensive posture while developing your air superiority.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground Army

**Trigger situation:**  
Midgame, around 7-9 minutes, with the opponent showing a ground posture (Zealots, Stalkers). Your own army is ground-oriented with Zealots and Immortals.

**Direction:**  
Continue strengthening your ground army and increasing your economy. Maintain a defensive posture and consider adding more tech (e.g., High Templar) for spell support.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early-Midgame Flexibility

**Trigger situation:**  
Early-midgame, around 4-5 minutes, with the opponent's posture still unknown. Your own economy is moderate, and you have not committed to an army style.

**Direction:**  
Increase your economy and technology while maintaining a defensive posture. Strengthen your ground army as a baseline, but remain flexible to transition to air if scouting suggests.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Late-Midgame Air Integration

**Trigger situation:**  
Late-midgame, around 10-12 minutes, with the opponent showing a ground posture (Zealots, Stalkers, Immortals, Oracles). Your own army is ground-oriented but has added Void Rays.

**Direction:**  
Increase your air presence and strengthen your air army. Continue increasing your economy and maintain a defensive posture.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Late-Midgame Ground Focus

**Trigger situation:**  
Late-midgame, around 10-12 minutes, with the opponent showing a ground posture (Zealots, Stalkers, Immortals, Oracles). Your own army is ground-oriented with Zealots.

**Direction:**  
Continue strengthening your ground army and increasing your economy. Maintain a defensive posture and consider adding more tech (e.g., High Templar) for spell support.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Air Superiority

**Trigger situation:**  
Midgame, around 8-9 minutes, with the opponent showing an air posture (Zealots, Stalkers, Void Rays, Oracles). Your own army is air-oriented with Void Rays.

**Direction:**  
Continue strengthening your air army and increasing your economy. Maintain a defensive posture and consider adding more tech (e.g., Tempests) for late-game.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Late-Midgame Air Dominance

**Trigger situation:**  
Late-midgame, around 10-12 minutes, with the opponent showing an air posture (Zealots, Stalkers, Void Rays, Oracles). Your own army is air-oriented with Void Rays.

**Direction:**  
Continue strengthening your air army and increasing your economy. Maintain a defensive posture and consider adding more tech (e.g., Tempests) for late-game.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Early-Midgame Air Transition

**Trigger situation:**  
Early-midgame, around 5-6 minutes, with the opponent showing a ground posture (Zealots). Your own army has transitioned to an air-oriented composition with Stalkers and Oracles.

**Direction:**  
Continue strengthening your air army and increasing your economy. Maintain a defensive posture and consider adding more tech (e.g., Void Rays) for air superiority.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Midgame Ground with Air Support

**Trigger situation:**  
Midgame, around 8-9 minutes, with the opponent showing an air posture (Zealots, Stalkers, Void Rays, Oracles). Your own army is ground-oriented with Zealots, Warp Prisms, Immortals, and Oracles.

**Direction:**  
Continue strengthening your ground army and increasing your economy. Maintain a defensive posture and consider adding more tech (e.g., High Templar) for spell support.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Early-Midgame Ground Development

**Trigger situation:**  
Early-midgame, around 4-5 minutes, with the opponent's posture still unknown. Your own army is undefined but you have a Stalker.

**Direction:**  
Increase your economy and technology while maintaining a defensive posture. Strengthen your ground army as a baseline, but remain flexible to transition to air if scouting suggests.

**Read for details:** `N012`

---
