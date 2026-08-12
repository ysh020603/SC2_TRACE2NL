# PvZ_O01 Technology / Economy / Upgrade

## Skill Identity

- Skill ID: PvZ_O01
- Matchup: Protoss vs Zerg
- Opening Family: technology / economy / upgrade opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Protoss opening that emphasizes heavy technology and economy development while maintaining moderate production. The early game is flexible, with the option to transition into either a ground or air-oriented army based on scouting and game flow. The focus is on establishing a strong economic and technological foundation before committing to a specific army composition.

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

### G05 — Protoss production interpretation

- Scale Gateways or other unit-producing tech only after power, prerequisites, and production capacity are executable.

## V4 Matchup-Specific Corrections

### R01 — Maintain production tempo while preserving tech/economy focus

**When:** Time between 240 and 360 seconds, with bank above 800 minerals, army supply below 15, and production structures (Gateways, Stargates, Robotic Facilities) fewer than 3 completed or under construction.

**Correction:** Prioritize adding production structures (Gateways or Stargates) to reach at least 3 total by 5 minutes, while keeping tech buildings (Cybernetics Core, Twilight Council) on schedule. Queue units from existing production if idle. Do not expand until production is sufficient and army supply is at least 15.

**Recheck:** At next decision cycle, verify production count is at least 3 and no production structure is idle for more than 10 seconds.

### R02 — Counter enemy ground composition with tech units

**When:** Enemy Intelligence indicates a ground-heavy composition with Zerglings, Roaches, or Queens, and you have a Robotics Facility or Stargate completed.

**Correction:** If enemy has Roaches, add Immortals from Robotics Facility. If enemy has mass Zerglings, add Colossi or High Templar for splash damage. If enemy has air presence, add Void Rays or Phoenixes. Maintain a ground core for defense. Prioritize these units in production queues.

**Recheck:** At next decision cycle, verify that at least one counter unit type is in production or completed, and that production is not idle.

### R03 — Recover from low army and high bank

**When:** Army supply below 15, bank above 1500 minerals, and predicted advantage is OverwhelmingDisadvantage or threat flags indicate imminent attack.

**Correction:** Immediately convert bank into army: queue units from all production structures, add production if possible, and prioritize defensive units. Do not expand or tech further until army supply is at least 20. If production is insufficient, build additional Gateways or Stargates.

**Recheck:** At next decision cycle, verify army supply has increased by at least 5 or production is actively building units.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid neglecting army while teching

**When:** Early game around 3 minutes, with heavy economy and technology investment, but army composition not yet defined. Opponent likely on ground macro with Zergling/Queen presence.

**Mistake → correction:** Focusing solely on economy and technology while ignoring production and army composition, leaving you vulnerable to early Zergling pressure. → Continue developing economy and technology, but maintain a flexible army composition. Strengthen ground forces as a baseline, and adapt based on scouting information.

**Why:** This opening prioritizes a strong economic and technological foundation. By not committing to a specific army composition early, you retain flexibility to respond to the opponent's strategy. Strengthening ground forces provides a safe baseline against early pressure.

**Read for full checks:** `N001`

### L02 — Avoid overcommitting to one unit type

**When:** Late-midgame around 10-12 minutes, with a strong ground army and heavy economy/technology. Opponent remains on ground posture with Zerglings, Queens, and Overseers.

**Mistake → correction:** Overcommitting to a single unit type, such as only Immortals and Void Rays, which can be countered if the opponent tech switches to air or mass ground units. → Continue strengthening your ground army and maintain your economic and technological advantage. Consider adding Colossi or High Templar for additional splash damage and spellcasting. Use your Void Rays to harass and provide air support.

**Why:** The opponent's army is still ground-heavy, and your Immortals and Void Rays provide good damage against armored units. Your heavy economy allows you to tech into Colossi or High Templar for a powerful late-game composition.

**Read for full checks:** `N004`

### L03 — Avoid over-committing before scouting

**When:** Early game around 3 minutes, with heavy economy and technology, but no clear army composition. Opponent has a ground posture with no reliable combat-unit cues.

**Mistake → correction:** Over-committing to a specific army composition before scouting the opponent's tech path, or neglecting defense while focusing on economy. → Continue developing economy and technology while maintaining a flexible army composition. Increase production to prepare for the midgame, and consider expanding further to secure your economy.

**Why:** With a heavy economy and technology, you can afford to invest in a strong midgame army. By not committing to a specific composition early, you retain flexibility to counter the opponent's strategy.

**Read for full checks:** `N005`

## Decision Nodes

### [DEFAULT] N001 — Early Game Tech and Economy Foundation

**Trigger situation:**  
Early game (around 3 minutes) with heavy economy and technology investment, but army composition not yet defined. Opponent is likely on a ground macro posture with Zergling/Queen presence.

**Direction:**  
Continue developing your economy and technology while maintaining a flexible army composition. Strengthen your ground forces as a baseline, but be ready to adapt based on scouting information.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Mid Game Ground Army Development

**Trigger situation:**  
Early-mid game (around 4-6 minutes) with heavy economy and technology, and a developing ground army. Opponent is still on a ground macro posture with Zergling/Queen.

**Direction:**  
Continue strengthening your ground army while maintaining your economic and technological lead. Increase production to support a larger army and consider expanding further to sustain your economy.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Army Consolidation

**Trigger situation:**  
Midgame (around 9 minutes) with a well-established ground army and heavy economy/technology. Opponent has a heavier ground presence with Roaches and Overseers.

**Direction:**  
Continue strengthening your ground army and maintain your economic and technological advantage. Consider adding tech units like Immortals or Colossi to counter the opponent's Roach-heavy composition. Use your Warp Prism for mobility and harassment.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Ground Army with Tech Transition

**Trigger situation:**  
Late-midgame (around 10-12 minutes) with a strong ground army and heavy economy/technology. Opponent remains on a ground posture with Zerglings, Queens, and Overseers.

**Direction:**  
Continue strengthening your ground army and maintain your economic and technological advantage. Consider adding Colossi or High Templar for additional splash damage and spellcasting. Use your Void Rays to harass and provide air support.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game Tech and Economy Focus

**Trigger situation:**  
Early game (around 3 minutes) with heavy economy and technology, but no clear army composition. Opponent has a ground posture with no reliable combat-unit cues.

**Direction:**  
Continue developing your economy and technology while maintaining a flexible army composition. Increase production to prepare for the midgame, and consider expanding further to secure your economy.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early-Mid Game Ground Army with Defense

**Trigger situation:**  
Early-mid game (around 5-6 minutes) with a developing ground army and heavy economy/technology. Opponent has a ground posture with Zerglings and Queens.

**Direction:**  
Continue strengthening your ground army and maintain your economic and technological lead. Increase production to support a larger army, and consider expanding further to sustain your economy. Keep your defense posture moderate to handle potential aggression.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Midgame Air Transition

**Trigger situation:**  
Midgame (around 7-9 minutes) with a transition to an air-oriented army. Opponent has a ground posture with Zerglings, Queens, and Overseers.

**Direction:**  
Continue strengthening your air army and maintain your economic and technological advantage. Use Phoenixes to harass and control the map, and consider adding Void Rays or Oracles for additional air power. Keep a ground core for defense.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early-Mid Game Air Transition

**Trigger situation:**  
Early-mid game (around 5-6 minutes) with a transition to an air-oriented army. Opponent has a ground posture with Queens and Overseers.

**Direction:**  
Continue strengthening your air army and maintain your economic and technological advantage. Use Oracles for harassment and scouting, and consider adding Phoenixes or Void Rays for more air power. Keep a ground core for defense.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Ground Army with Heavy Defense

**Trigger situation:**  
Midgame (around 7 minutes) with a strong ground army and heavy defense. Opponent has a heavy ground presence with Roaches and Overseers.

**Direction:**  
Continue strengthening your ground army and maintain your economic and technological advantage. Consider adding Immortals or Colossi to counter the opponent's Roach-heavy composition. Use your Phoenixes for harassment and to control the map.

**Read for details:** `N009`

---
