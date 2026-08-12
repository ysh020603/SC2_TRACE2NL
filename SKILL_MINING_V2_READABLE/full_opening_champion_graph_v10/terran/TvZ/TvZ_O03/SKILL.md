# TvZ_O03 Technology / Economy / Production

## Skill Identity

- Skill ID: TvZ_O03
- Matchup: Terran vs Zerg
- Opening Family: technology / economy / production opening
- Method: Opening-Champion Full V10

## Opening Strategy

A Terran opening that emphasizes heavy technology and economy while maintaining moderate production, aiming for a flexible ground-oriented midgame.

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

### G05 — Terran production interpretation

- Scale Barracks/Factory/Starport capacity before ordering add-ons or units that lack a completed parent structure.

## V4 Matchup-Specific Corrections

### R01 — Production Tempo and Bank Conversion

**When:** At 4-6 minutes, if bank is above 800 minerals and production is below 3 active structures, or if army supply is below 10 while production is idle.

**Correction:** Queue units from existing production structures, prioritizing Marines and Marauders. If production structures are insufficient, build a Barracks with a Reactor or a Factory, ensuring prerequisites are met. Convert bank into production capacity before expanding.

**Recheck:** Next decision cycle: verify bank is below 600 and production structures are actively producing.

### R02 — Anti-Air Response to Mutalisks

**When:** If enemy intelligence shows Mutalisks or other air units, and your army lacks sufficient anti-air (e.g., fewer than 4 Marines or no Missile Turrets).

**Correction:** Add anti-air by building Missile Turrets at each base and producing Marines or Thors. If tech lab is available, research Stim Pack and Combat Shield to improve Marine effectiveness. Maintain ground army composition while integrating anti-air.

**Recheck:** Next decision cycle: confirm at least 2 Missile Turrets per base and a mix of anti-air units in the army.

### R03 — Recovery from Low Army and High Bank

**When:** If army supply is below 15 and bank is above 1000 minerals, or if predicted advantage is OverwhelmingDisadvantage.

**Correction:** Immediately queue units from all production structures, prioritizing combat units. If production is insufficient, build additional Barracks or Factories. Do not expand or invest in technology until army supply is above 20 and bank is below 500.

**Recheck:** Next decision cycle: verify army supply is above 20 and bank is below 500, or threat level has decreased.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid neglecting anti-air against Mutalisks

**When:** Late midgame, around 10 minutes, with Siege Tanks, Marines, Medivacs, and Battlecruisers, while the opponent has Zerglings, Mutalisks, and Queens.

**Mistake → correction:** Focusing solely on strengthening your ground army and economy while ignoring anti-air, leaving you vulnerable to Mutalisk harassment. → Maintain your current army composition and defense, while increasing economy. Continue tech development.

**Why:** Your mix of ground and air units gives you flexibility against the opponent's Mutalisks and ground army. Maintaining a strong economy allows you to sustain this composition.

**Read for full checks:** `N005`

### L02 — Avoid overcommitting to army before tech is established

**When:** Early game, around 3 minutes, with an unknown army posture, while the opponent has a Queen and light tech.

**Mistake → correction:** Overcommitting to army production before your heavy tech investment pays off, delaying your economy and tech progression. → Increase production and economy, while maintaining defense and continuing tech development.

**Why:** Your heavy tech investment gives you a long-term advantage, so you can focus on macro. The opponent's light tech suggests they are not rushing, so you have time to develop.

**Read for full checks:** `N006`

### L03 — Avoid staying too ground-heavy without air support

**When:** Late midgame, around 10 minutes, with a ground army of Marines, while the opponent has Zerglings, Mutalisks, and Queens.

**Mistake → correction:** Staying too ground-heavy without air support, leaving you unable to counter the opponent's Mutalisks effectively. → Increase air presence and technology, while continuing to strengthen your ground army. Maintain defense and increase economy and expansions.

**Why:** The opponent's Mutalisks require anti-air capabilities. Investing in air and tech gives you the tools to deal with them while maintaining a strong ground presence.

**Read for full checks:** `N007`

## Decision Nodes

### [DEFAULT] N001 — Early Midgame Ground Development

**Trigger situation:**  
At around 4 minutes, you have a ground-oriented posture with moderate production and heavy tech, while the opponent appears to be on a ground macro path with light or uncertain air.

**Direction:**  
Continue strengthening your ground army while increasing economy and expansions. Maintain current defense and air posture.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Midgame Ground Army Strengthening

**Trigger situation:**  
Around 8 minutes, you have a heavy ground army with Ghosts, Hellions, and Medivacs, while the opponent has a heavy ground composition with Zerglings, Roaches, and Queens.

**Direction:**  
Increase your air presence and technology while continuing to strengthen your ground army. Maintain defense and increase economy and expansions.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Siege Setup

**Trigger situation:**  
Around 7 minutes, you have Siege Tanks, Marines, and Reapers, while the opponent has a heavy ground army with Zerglings and Queens.

**Direction:**  
Maintain your ground army and defense, while increasing economy. Keep tech development going.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Early Midgame Stabilization

**Trigger situation:**  
Around 4 minutes, you have a ground army with Marines, while the opponent has Zerglings and Queens, with light tech.

**Direction:**  
Stabilize your position by increasing production and maintaining defense, while continuing tech development.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Late Midgame Ground and Air Mix

**Trigger situation:**  
Around 10 minutes, you have Siege Tanks, Marines, Medivacs, and Battlecruisers, while the opponent has Zerglings, Mutalisks, and Queens.

**Direction:**  
Maintain your current army composition and defense, while increasing economy. Continue tech development.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Early Game Tech Development

**Trigger situation:**  
Around 3 minutes, you have an unknown army posture, while the opponent has a Queen and light tech.

**Direction:**  
Increase production and economy, while maintaining defense and continuing tech development.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Late Midgame Tech and Air Investment

**Trigger situation:**  
Around 10 minutes, you have a ground army with Marines, while the opponent has Zerglings, Mutalisks, and Queens.

**Direction:**  
Increase air presence and technology, while continuing to strengthen your ground army. Maintain defense and increase economy and expansions.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early Midgame Ground Tech Transition

**Trigger situation:**  
Around 5 minutes, you have Marines, Reapers, and Hellions, while the opponent has Zerglings and Queens.

**Direction:**  
Maintain your ground army and defense, while increasing economy. Continue tech development.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Army Maintenance

**Trigger situation:**  
Around 8 minutes, you have a ground army with Marines, while the opponent has Zerglings and Queens.

**Direction:**  
Maintain your current army path and defense, while keeping economy and tech development steady.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Early Game Defense and Economy

**Trigger situation:**  
Around 3 minutes, you have an unknown army posture, while the opponent has Zerglings and Queens.

**Direction:**  
Increase defense and economy, while continuing production and tech development.

**Read for details:** `N010`

---

### [DEFAULT] N011 — Midgame Air and Ground Mix

**Trigger situation:**  
Around 8 minutes, you have Marines, Reapers, Hellions, and Banshees, while the opponent has Zerglings, Mutalisks, Queens, and Overseers.

**Direction:**  
Increase production and economy, while maintaining defense and continuing tech development.

**Read for details:** `N011`

---
