# PvZ_O02 Technology / Economy / Production

## Skill Identity

- Skill ID: PvZ_O02
- Matchup: Protoss vs Zerg
- Opening Family: technology / economy / production opening
- Method: Failure-Aware Full V4

## Opening Strategy

A flexible Protoss opening that prioritizes technology and economy while keeping production options open. Early game is uncertain, with the potential to transition into a ground-based army or continue teching depending on scouting.

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

### R01 — Maintain production tempo and worker saturation

**When:** At any time, if workers are below 24 by 4:00 or below 30 by 5:00, or if active production structures are fewer than 3 by 5:00, or if bank exceeds 800 minerals with idle production.

**Correction:** Prioritize worker production from all Nexi until saturation (16 per base) is reached. If bank exceeds 800 minerals and production is idle, add a Gateway or tech structure (e.g., Twilight Council) if prerequisites are met, and queue units from existing production. Keep supply providers just in time to avoid blocking.

**Recheck:** Recheck at next decision cycle: workers, active production count, bank, and supply headroom.

### R02 — Adapt to Zerg ground composition

**When:** Enemy Intelligence shows Zergling and Queen cues, or if Zergling or Baneling threat is detected. If army supply is below 30 and bank is above 600 minerals, prioritize army production over tech.

**Correction:** Queue Zealots and Stalkers from Gateways, and add a Robotics Facility if not present to enable Observer for detection. If Banelings are present, ensure Sentries are available for Force Field. Continue worker production but do not let it delay army production.

**Recheck:** Recheck at next decision cycle: enemy composition cues, army supply, bank, and production queue status.

### R03 — Recover from low army and high bank

**When:** If army supply is below 15 and bank is above 1000 minerals, or if predicted advantage is OverwhelmingDisadvantage, or if any owned base is threatened.

**Correction:** Immediately convert bank into army: queue units from all production structures, add Gateways if supply allows (up to 4 total), and ensure supply is not blocking. If production is insufficient, add a Gateway or Warp Gate. Do not expand or tech until army supply is above 30 and threat is mitigated.

**Recheck:** Recheck at next decision cycle: army supply, bank, production count, and threat flags.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Ground vs Ground: Avoid Overcommitting to Tech

**When:** Early-midgame, opponent shows ground posture with Zergling and Queen cues; your own ground posture with Zealot and Stalker cues.

**Mistake → correction:** Tempting to over-invest in technology while neglecting army size, risking falling behind in army strength. → Strengthen ground forces, continue production and technology development, and maintain economy.

**Why:** Both sides ground-oriented, so a strong ground army and tech advantage are key to gaining an edge.

**Read for full checks:** `N007`

### L02 — Ground vs Ground: Avoid Tech Switch Surprise

**When:** Late-midgame, opponent shows ground posture with Queen cues; your own ground posture with Zealot, Stalker, Sentry, and Observer cues.

**Mistake → correction:** Tempting to focus solely on ground army and ignore potential tech switch or large attack, risking being caught off guard. → Strengthen ground forces, continue production and technology development, and maintain economy.

**Why:** Both sides ground-oriented, so a strong ground army and tech advantage are key to gaining an edge.

**Read for full checks:** `N010`

### L03 — Ground vs Ground: Avoid Neglecting Economy

**When:** Midgame, opponent shows ground posture with Queen cues; your own ground posture with Zealot cues.

**Mistake → correction:** Tempting to over-invest in army and tech while neglecting economy, risking being caught off guard by a tech switch or large attack. → Strengthen ground forces, increase production and technology, and maintain economy.

**Why:** Opponent's ground posture suggests potential pressure. Investing in economy and tech while maintaining production provides a solid foundation.

**Read for full checks:** `N011`

## Decision Nodes

### [DEFAULT] N001 — Early Game: Maintain Flexibility

**Trigger situation:**  
At the start of the game, both sides are largely unknown. No reliable combat-unit cues have been observed from the opponent, and your own posture is also undefined.

**Direction:**  
Maintain current army path, keep production and technology development steady, and prepare to adapt based on scouting.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early-Midgame: Continue Development

**Trigger situation:**  
The game progresses into the early-midgame with still limited information. The opponent remains unknown, and your own posture is still developing.

**Direction:**  
Maintain current army path, keep production and technology development steady, and prepare to adapt based on scouting.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame: Maintain Flexibility

**Trigger situation:**  
The game reaches the midgame with the opponent still unknown. No reliable combat-unit cues have been observed, and your own posture remains undefined.

**Direction:**  
Maintain current army path, keep production and technology development steady, and prepare to adapt based on scouting.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame: Maintain Flexibility

**Trigger situation:**  
The game reaches the late-midgame with the opponent still unknown. No reliable combat-unit cues have been observed, and your own posture remains undefined.

**Direction:**  
Maintain current army path, keep production and technology development steady, and prepare to adapt based on scouting.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Early Game: Ground Defense and Tech

**Trigger situation:**  
Early game, the opponent shows a ground posture with Zergling and Queen cues. Your own posture is unknown but with heavy technology investment and heavy defense.

**Direction:**  
Strengthen ground forces, increase defense and economy, and continue technology development.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early Game: Economy and Tech Focus

**Trigger situation:**  
Early game, the opponent shows a ground posture with Zergling and Queen cues. Your own posture is unknown but with heavy technology investment and heavy expansion.

**Direction:**  
Strengthen ground forces, increase economy and production, and continue technology development.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early-Midgame: Ground Army Development

**Trigger situation:**  
Early-midgame, the opponent shows a ground posture with Zergling and Queen cues. Your own posture is ground-oriented with Zealot and Stalker cues.

**Direction:**  
Strengthen ground forces, continue production and technology development, and maintain economy.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early-Midgame: Economy and Tech

**Trigger situation:**  
Early-midgame, the opponent shows a ground posture with Zergling and Queen cues. Your own posture is unknown but with heavy economy and technology investment.

**Direction:**  
Strengthen ground forces, increase production and technology, and maintain economy.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame: Ground Army and Tech

**Trigger situation:**  
Midgame, the opponent shows a ground posture with Zergling, Queen, and Overseer cues. Your own posture is ground-oriented with Zealot, Stalker, Observer, and Immortal cues.

**Direction:**  
Strengthen ground forces, continue production and technology development, and maintain economy.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Late-Midgame: Ground Army and Tech

**Trigger situation:**  
Late-midgame, the opponent shows a ground posture with Queen cues. Your own posture is ground-oriented with Zealot, Stalker, Sentry, and Observer cues.

**Direction:**  
Strengthen ground forces, continue production and technology development, and maintain economy.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Midgame: Ground Army and Tech

**Trigger situation:**  
Midgame, the opponent shows a ground posture with Queen cues. Your own posture is ground-oriented with Zealot cues.

**Direction:**  
Strengthen ground forces, increase production and technology, and maintain economy.

**Read for details:** `N011`

---
