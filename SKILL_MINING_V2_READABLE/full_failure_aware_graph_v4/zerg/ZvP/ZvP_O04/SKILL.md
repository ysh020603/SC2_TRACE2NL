# ZvP_O04 Expansion / Economy / Production

## Skill Identity

- Skill ID: ZvP_O04
- Matchup: Zerg vs Protoss
- Opening Family: expansion / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A Zerg opening focused on early economy and expansion, with moderate production and light technology investment. The strategy aims to build a strong economic foundation while maintaining flexibility to adapt to Protoss tech choices.

Develop a expansion / economy / production posture while preserving flexibility for live observation-driven adaptation.

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

### R01 — Maintain production tempo and convert bank into army

**When:** At any time, if bank is above 800 minerals and 400 gas, or if active production structures are fewer than 3 and army supply is below 30, or if supply is not blocked and workers are below 60.

**Correction:** Queue units from all available hatcheries, prioritizing Zerglings and Roaches to maintain ground pressure. If a spawning pool is missing, build it first. If a hatchery is missing, build one at an available expansion. If supply is not blocked and workers are below 60, continue injecting larvae and building workers up to 60. If bank remains high after queuing, build additional hatcheries to increase production capacity.

**Recheck:** Recheck at next decision cycle: ensure bank is below 800 minerals and 400 gas, and that production structures are actively queued.

### R02 — Adapt composition to enemy tech and detection needs

**When:** If enemy intelligence reveals any of: Dark Templar, Warp Prism, Immortal, Phoenix, Oracle, or Void Ray, and your army lacks appropriate counters or detection.

**Correction:** If Dark Templar or Warp Prism is observed, build an Evolution Chamber and research Overseer morph, then morph Overseers from existing overlords. If Immortal is observed, add Roaches or Hydralisks to counter. If Phoenix or Oracle is observed, build a Hydralisk Den and produce Hydralisks, or add Spore Crawlers at bases. If Void Ray is observed, build a Spire and produce Corruptors. Ensure at least one Overseer or Spore Crawler per base for detection.

**Recheck:** Recheck at next decision cycle: confirm that appropriate counter units are in production or completed, and detection is present at each base.

### R03 — Recover from low army and high bank with emergency production

**When:** If army supply is below 15 and bank is above 1000 minerals, or if predicted advantage is OverwhelmingDisadvantage, or if any owned base is threatened.

**Correction:** Immediately queue combat units from all hatcheries, prioritizing Zerglings and Roaches. If a spawning pool is missing, build it. If a hatchery is missing, build one at the nearest safe expansion. Do not build additional supply providers unless supply is blocked. Do not expand. If workers are above 40, do not build more workers until army supply is above 30. If gas is high, consider building a Baneling Nest and morph Banelings if enemy has light units.

**Recheck:** Recheck at next decision cycle: army supply should be above 15, bank should be below 1000 minerals, and no owned base should be under threat.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Detection and Composition vs Dark Templar

**When:** Midgame around 480 seconds, with both players having ground armies. Opponent shows Stalkers, Dark Templars, Warp Prisms, and Observers.

**Mistake → correction:** Neglecting detection and overcommitting to a single unit type, leaving your army vulnerable to Dark Templar harassment and lacking counters to Stalkers. → Continue strengthening your ground army and maintain economy. Add detection (e.g., Overseers) and mix in units that counter Stalkers and Dark Templars (e.g., Banelings).

**Why:** Dark Templars require detection to be fought effectively; a mixed composition with detection prevents devastating losses and handles multiple threats.

**Read for full checks:** `N003`

### L02 — Scouting and Tech Adaptation

**When:** Early-midgame around 300 seconds, with the opponent having a ground posture but no combat units observed. You have Zerglings and Queens.

**Mistake → correction:** Overcommitting to a single unit composition and neglecting scouting, leaving you unprepared for the opponent's heavy tech investment. → Continue developing your ground army and economy. Maintain production and consider increasing technology to match the opponent's heavy investment.

**Why:** The opponent's heavy tech suggests they may be teching to a specific unit; a strong economy and ground army allow you to adapt to whatever they produce.

**Read for full checks:** `N005`

### L03 — Countering Immortals and Warp Prism Drops

**When:** Midgame around 420 seconds, with the opponent having a ground army including Warp Prisms and Immortals. You have a ground army with Zerglings and Queens.

**Mistake → correction:** Relying solely on Roaches, which are countered by Immortals, and neglecting detection against Warp Prism drops. → Increase your production and expansion to support a larger army. Consider adding Roaches or Hydralisks to counter the Immortals and Warp Prisms.

**Why:** Immortals are strong against armored units; adding Roaches and Hydralisks provides effective counters and helps defend against drops.

**Read for full checks:** `N008`

## Decision Nodes

### [DEFAULT] N001 — Early Economy and Ground Foundation

**Trigger situation:**  
Early game, around 180 seconds, with both players expanding and investing in economy. Opponent's tech is heavy but army composition is unknown.

**Direction:**  
Continue developing your economy and ground forces. Maintain production and consider increasing technology to keep pace with the opponent's heavy tech investment.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Midgame Ground Reinforcement

**Trigger situation:**  
Early-midgame around 240 seconds, with both players still expanding. You have Zerglings and Queens, while the opponent remains unknown.

**Direction:**  
Strengthen your ground army and continue economic growth. Maintain production and consider adding more tech to match the opponent's heavy investment.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground vs Ground

**Trigger situation:**  
Midgame around 480 seconds, with both players having ground armies. Opponent shows Stalkers, Dark Templars, Warp Prisms, and Observers.

**Direction:**  
Continue strengthening your ground army and maintain economy. Consider adding detection and units that counter stalkers and dark templars, such as overseers and banelings.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Midgame Air Transition

**Trigger situation:**  
Midgame around 540 seconds, with the opponent showing a heavy air presence including Phoenixes. You have a strong ground army and are considering air.

**Direction:**  
Increase your air presence to counter the Phoenixes. Consider adding Mutalisks or Corruptors, while maintaining your ground army for defense.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early-Midgame Ground Tech

**Trigger situation:**  
Early-midgame around 300 seconds, with the opponent having a ground posture but no combat units observed. You have Zerglings and Queens.

**Direction:**  
Continue developing your ground army and economy. Maintain production and consider increasing technology to match the opponent's heavy investment.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early-Midgame Air Defense

**Trigger situation:**  
Early-midgame around 360 seconds, with the opponent showing an air presence including Phoenixes and Oracles. You have a ground army with Zerglings and Queens.

**Direction:**  
Maintain your ground army and consider adding anti-air units such as Hydralisks or Spore Crawlers. Continue to expand and increase production.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early-Midgame Tech Investment

**Trigger situation:**  
Early-midgame around 360 seconds, with the opponent showing an air presence including Phoenixes and Oracles. You have a ground army and heavy technology.

**Direction:**  
Continue to invest in technology and production. Consider adding anti-air units and expanding further to support a larger army.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Midgame Ground Expansion

**Trigger situation:**  
Midgame around 420 seconds, with the opponent having a ground army including Warp Prisms and Immortals. You have a ground army with Zerglings and Queens.

**Direction:**  
Increase your production and expansion to support a larger army. Consider adding Roaches or Hydralisks to counter the Immortals and Warp Prisms.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Ground vs Ground

**Trigger situation:**  
Midgame around 480 seconds, with the opponent having a ground army including Zealots, Stalkers, Observers, and Immortals. You have a strong ground army.

**Direction:**  
Continue to strengthen your ground army and maintain economy. Consider adding Banelings to counter Zealots and Hydralisks for anti-air support.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Midgame Air Transition

**Trigger situation:**  
Midgame around 540 seconds, with the opponent having a ground army including Dark Templars and Warp Prisms. You have a ground army and are adding air.

**Direction:**  
Increase your air presence with Mutalisks to harass and counter the opponent's ground army. Continue to expand and maintain production.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Late-Midgame Air and Ground

**Trigger situation:**  
Late-midgame around 600 seconds, with the opponent having a ground army including Void Rays. You have a strong ground army with air support.

**Direction:**  
Continue to strengthen your air and ground forces. Consider adding Corruptors to counter Void Rays and maintain your economy.

**Read for details:** `N011`

---

### [DEFAULT] N012 — Early Game Expansion

**Trigger situation:**  
Early game around 180 seconds, with the opponent showing a Zealot. You have a light army and are expanding.

**Direction:**  
Continue to expand and build your economy. Consider adding Queens for defense and scouting to identify the opponent's tech choice.

**Read for details:** `N012`

---
