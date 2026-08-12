# PvP_O01 Technology / Economy / Production

## Skill Identity

- Skill ID: PvP_O01
- Matchup: Protoss vs Protoss
- Opening Family: technology / economy / production opening
- Method: Executable-Normalized Full V11

## Opening Strategy

A Protoss versus Protoss opening that emphasizes heavy technology and economy investment while keeping production moderate early. The strategic posture is flexible, allowing transition into either a ground-oriented or air-oriented army depending on scouting information.

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

### R01 — Maintain tech-economy tempo with continuous production

**When:** At any time before 360s, if bank is above 800 minerals and production structures (completed + pending) are fewer than 3, or if any production structure is idle with bank above 400.

**Correction:** Queue a Gateway or Warp Gate if prerequisites are met, or add a tech structure (Cybernetics Core, Twilight Council) if production is sufficient. Prioritize spending bank on production and tech, not on extra bases or upgrades. Keep worker production active until saturation.

**Recheck:** Recheck at next decision cycle.

### R02 — Adapt to enemy air or ground composition

**When:** If enemy intelligence shows a significant air presence (e.g., Void Rays, Phoenixes) or a ground-heavy composition with Zealots/Sentries, and your army lacks appropriate counters.

**Correction:** If air threat, add Stalkers or Phoenixes from existing Gateways; if ground threat, add Sentries for force fields and detection. Ensure tech structures (Cybernetics Core, Twilight Council) are present to support these units. Continue economy and tech development.

**Recheck:** Recheck at next decision cycle.

### R03 — Recover from low army and high bank

**When:** If army supply is below 15 and bank is above 1000 minerals, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all available production structures, prioritizing combat units (Zealots, Stalkers). If production is insufficient, add Gateways or Warp Gates. Do not expand or invest in tech until army supply is above 15 and bank is below 500.

**Recheck:** Recheck at next decision cycle.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground with Warp Prism Harass

**When:** Midgame, opponent shows ground posture with Zealots, Sentries, and Warp Prisms. You have Zealots and a heavy economy.

**Mistake → correction:** Over-committing to a single ground unit type and neglecting support units or upgrades, leaving you vulnerable to Warp Prism harass. → Continue strengthening your ground army and economy. Add Sentries for defensive capabilities and detection.

**Why:** The opponent's use of Warp Prisms suggests potential harass. Sentries can provide shields and force fields to defend. Maintaining a strong economy will support a larger army.

**Read for full checks:** `N004`

### L02 — Early-Midgame Air Threat with Void Rays

**When:** Early-midgame, opponent shows air posture with Void Rays. You have a ground army with Zealots and a strong economy.

**Mistake → correction:** Staying pure ground without anti-air, or over-committing to air without proper tech. → Transition to include anti-air units such as Stalkers or Phoenixes. Continue developing your economy and tech.

**Why:** Void Rays are strong against ground units. Adding anti-air will help defend against an air attack and maintain map control.

**Read for full checks:** `N007`

### L03 — Midgame Air Mass with Void Rays

**When:** Midgame, opponent has an air posture with Void Rays. You have a ground army with Zealots and a strong economy.

**Mistake → correction:** Neglecting anti-air upgrades or staying too passive if the opponent is massing air. → Prioritize adding anti-air units and possibly transition to an air army yourself. Continue developing economy and tech.

**Why:** The opponent's air army is a significant threat. Investing in anti-air or transitioning to air will help you counter their composition.

**Read for full checks:** `N008`

## Decision Nodes

### [DEFAULT] N001 — Early-Mid Ground Macro with Heavy Tech

**Trigger situation:**  
At around 300 seconds, both sides show a ground-oriented posture with heavy production and technology. The opponent is likely fielding Zealots, and your own army is also Zealot-based. Economy and expansions are heavy.

**Direction:**  
Continue strengthening your ground army while increasing economy and technology. Maintain current expansion and production levels.

**Read for details:** `N001`

---

### [POSITIVE] N002 — Ground Macro with Stalker Presence

**Trigger situation:**  
At around 240 seconds, the opponent shows a ground posture with Stalkers, while you have Zealots. Both have heavy production and tech, but your expansion count is uncertain.

**Direction:**  
Increase your economy and continue ground army production. Consider adding Stalkers for anti-air and mobility.

**Read for details:** `N002`

---

### [POSITIVE] N003 — Stabilize and Develop Ground

**Trigger situation:**  
At around 240 seconds, the opponent has a ground posture with Stalkers, while you have Zealots. Your expansion count is uncertain, and you may be slightly behind.

**Direction:**  
Focus on stabilizing your economy and increasing production. Continue tech development but prioritize army safety.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Ground Macro with Warp Prism

**Trigger situation:**  
At around 480 seconds, the opponent shows a ground posture with Zealots, Sentries, and Warp Prisms. You have Zealots and a heavy economy.

**Direction:**  
Continue strengthening your ground army and economy. Consider adding Sentries for defensive capabilities and detection.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game Tech Focus

**Trigger situation:**  
At around 180 seconds, both sides have an unknown army composition, but you are investing heavily in technology. Production is moderate.

**Direction:**  
Continue developing your technology and economy while increasing production. Maintain flexibility to adapt to scouting.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early-Mid Ground with Unknown Opponent

**Trigger situation:**  
At around 240 seconds, you have a ground army with Zealots, but the opponent's army composition is unknown. They have heavy defense and economy.

**Direction:**  
Continue strengthening your ground army and increase your expansion count. Maintain scouting to identify the opponent's tech path.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early-Mid Air Transition

**Trigger situation:**  
At around 360 seconds, the opponent shows an air posture with Void Rays, while you have a ground army with Zealots. Your economy is strong.

**Direction:**  
Consider transitioning to include anti-air units such as Stalkers or Phoenixes. Continue developing your economy and tech.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Air Pressure

**Trigger situation:**  
At around 420 seconds, the opponent has an air posture with Void Rays, while you have a ground army with Zealots. Your economy is strong.

**Direction:**  
Prioritize adding anti-air units and possibly transition to an air army yourself. Continue developing economy and tech.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Late-Mid Ground with Mixed Army

**Trigger situation:**  
At around 600 seconds, the opponent has a ground posture with Stalkers, Sentries, Warp Prisms, and Immortals. You have a mixed ground/air army with Zealots and Void Rays.

**Direction:**  
Continue strengthening your mixed army, focusing on upgrades and maintaining a strong economy. Consider adding more Void Rays for air superiority.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Midgame Air Transition with Carriers

**Trigger situation:**  
At around 540 seconds, the opponent has a ground posture with Stalkers, Sentries, and Immortals. You have an air army with Stalkers and Carriers.

**Direction:**  
Continue building your air army, focusing on Carriers and supporting units. Maintain a strong economy and tech.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Early-Mid Air Mirror

**Trigger situation:**  
At around 300 seconds, both sides show an air posture with Void Rays. You have a mixed army with Zealots, Stalkers, and Oracles.

**Direction:**  
Continue developing your air army, focusing on Void Rays and supporting units. Maintain a strong economy and tech.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Late-Mid Air Superiority

**Trigger situation:**  
At around 600 seconds, the opponent has an air posture with Zealots, Stalkers, and Void Rays. You have an air army with Stalkers and Carriers.

**Direction:**  
Continue building your air army, focusing on Carriers and supporting units. Maintain a strong economy and tech.

**Read for details:** `N012`

---
