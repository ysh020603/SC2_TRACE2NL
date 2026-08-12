# TvT_O07 Technology/Economy/Production

## Skill Identity

- Skill ID: TvT_O07
- Matchup: Terran vs Terran
- Opening Family: Technology/Economy/Production
- Method: Prompt-Executable Full V9

## Opening Strategy

A Terran mirror opening that emphasizes heavy technology and economy investment while maintaining moderate production. The early game is characterized by an unknown army posture, with a focus on developing infrastructure and teching up. As the game progresses, the posture becomes ground-oriented with heavy production and technology, and the strategic goal is to build a strong economy and tech base while remaining flexible to adapt to the opponent's actions.

Develop a technology/economy/production posture while preserving flexibility for live observation-driven adaptation.

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

### R01 — Tech-Economy Tempo with Production Scaling

**When:** Before 360s, if bank > 800 and (production < 3 or workers < 30) and no threat flag is OverwhelmingDisadvantage.

**Correction:** Prioritize adding production structures (Barracks, Factory, Starport) up to 3-4 total, and continue worker production toward 30-32. If supply is below 30, add a supply depot only if none is completed, pending, or queued. Keep tech buildings (e.g., Tech Lab, Engineering Bay) progressing if prerequisites are met.

**Recheck:** Next decision cycle: confirm production count >= 3, workers >= 30, and bank < 800.

### R02 — Enemy Composition Counter

**When:** If enemy intelligence reveals a composition with medivacs or air units (e.g., Medivac, Banshee, Viking) and your anti-air or air support is light (e.g., no Marines with Stim, no Cyclones, no Vikings, no Missile Turrets).

**Correction:** Add anti-air capability: produce Marines (if Barracks available) or add a Starport with Tech Lab to produce Vikings or Banshees. If Factory is available, produce Cyclones. Also consider adding a Missile Turret at each base if mineral bank > 500 and no turret is already present.

**Recheck:** Next decision cycle: confirm you have at least 4 anti-air units or 1 Missile Turret per base, and continue production.

### R03 — Recovery from Low Army and High Bank

**When:** If army supply < 15 and bank > 1000, or predicted advantage is OverwhelmingDisadvantage, or a threatened owned zone is detected.

**Correction:** Immediately convert bank into army: queue units from all available production structures (Barracks, Factory, Starport) without stopping. If production is insufficient (e.g., < 3 structures), build additional production structures first, prioritizing Barracks for Marines. Do not expand or tech until army supply is at least 15 and bank is below 500.

**Recheck:** Next decision cycle: confirm army supply >= 15 and bank < 500, or threat flag is cleared.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid premature army investment

**When:** Early game, around 180 seconds, when both players have unknown army postures but heavy technology investment, and your production is moderate while the opponent's is heavy.

**Mistake → correction:** Committing to a large army before knowing the enemy's plan, which can leave you vulnerable to tech switches or economic deficits. → Focus on increasing your economy and expansion while continuing technology development. Strengthen ground forces as a baseline and maintain a defensive posture.

**Why:** With the opponent's army unknown, building a solid economy and tech base allows flexibility to adapt to whatever the opponent reveals.

**Read for full checks:** `N002`

### L02 — Avoid passivity and unsieged engagements

**When:** Midgame, around 420-540 seconds, when both players have ground-oriented macro postures with heavy production and technology, and the opponent shows siege tanks and marines.

**Mistake → correction:** Being too passive, allowing the opponent to gain an economic advantage, or engaging without proper siege setup. → Increase defensive capabilities while continuing to strengthen ground forces. Maintain economy and expansion, and consider adding siege tanks to your composition.

**Why:** With both sides having heavy ground armies, a defensive posture with siege tanks helps hold position while teching and expanding, outlasting the opponent in a macro game.

**Read for full checks:** `N003`

### L03 — Avoid neglecting air defense

**When:** Late midgame, around 600 seconds, when both players have ground-oriented macro postures with heavy production and technology, and the opponent has medivacs while your air presence is light.

**Mistake → correction:** Neglecting air defense, leaving you vulnerable to Medivac drops and healing. → Continue strengthening ground forces while adding air support or anti-air capabilities to counter medivacs. Maintain defensive posture and economy.

**Why:** The opponent's medivacs provide mobility and healing, so adding air units or anti-air helps deal with drops and sustain in engagements.

**Read for full checks:** `N004`

## Decision Nodes

### [DEFAULT] N001 — Early-Mid Ground Macro with Heavy Tech

**Trigger situation:**  
Around 240-300 seconds, both players have established a ground-oriented macro posture with heavy production and technology. The opponent shows a ground army with possible pressure, while your own forces are also ground-based with heavy production.

**Direction:**  
Continue developing your economy and technology while strengthening your ground forces. Maintain your current defensive posture and consider increasing your expansion and production.

**Read for details:** `N001`

---

### [DEFAULT] N002 — Early Game Tech Focus with Unknown Army

**Trigger situation:**  
At around 180 seconds, both players have an unknown army posture, but with heavy technology investment. The opponent's production is heavy, while your own production is moderate.

**Direction:**  
Focus on increasing your economy and expansion while continuing your technology development. Strengthen your ground forces as a baseline, and maintain a defensive posture.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Midgame Ground Siege with Heavy Defense

**Trigger situation:**  
Around 420-540 seconds, both players have a ground-oriented macro posture with heavy production and technology. The opponent shows a ground army with siege tanks and marines, while your own forces include marines and hellions.

**Direction:**  
Increase your defensive capabilities while continuing to strengthen your ground forces. Maintain your economy and expansion, and consider adding siege tanks to your composition.

**Read for details:** `N003`

---

### [DEFAULT] N004 — Late-Midgame Ground with Air Support

**Trigger situation:**  
Around 600 seconds, both players have a ground-oriented macro posture with heavy production and technology. The opponent has a moderate air presence with medivacs, while your own air presence is light or uncertain.

**Direction:**  
Continue strengthening your ground forces while considering adding air support to counter the opponent's medivacs. Maintain your defensive posture and economy.

**Read for details:** `N004`

---

### [DEFAULT] N005 — Midgame Ground with Balanced Development

**Trigger situation:**  
Around 420-540 seconds, both players have a ground-oriented macro posture with heavy production and technology. The opponent shows a ground army with siege tanks and medivacs, while your own forces include marines and marauders.

**Direction:**  
Maintain your current development pace, focusing on economy and technology. Strengthen your ground forces and consider adding medivacs for mobility.

**Read for details:** `N005`

---

### [DEFAULT] N006 — Late-Midgame Ground to Air Transition

**Trigger situation:**  
Around 600 seconds, both players have a ground-oriented macro posture with heavy production and technology. The opponent shows a ground army with marines and marauders, while your own forces are also ground-based.

**Direction:**  
Begin transitioning to an air-oriented composition, increasing your air presence and technology. Continue to strengthen your ground forces as a base.

**Read for details:** `N006`

---

### [DEFAULT] N007 — Early-Mid Stabilize and Develop

**Trigger situation:**  
Around 300-360 seconds, both players have a ground-oriented macro posture with heavy production and technology. The opponent shows a ground army with marines, while your own forces include marines and reapers.

**Direction:**  
Stabilize your position by ensuring your defenses are solid, then continue developing your economy and technology. Increase your production to support a stronger army.

**Read for details:** `N007`

---

### [DEFAULT] N008 — Early-Mid Air Transition with Ground Core

**Trigger situation:**  
Around 300-360 seconds, both players have a ground-oriented macro posture with heavy production and technology. The opponent shows a ground army with marines and reapers, while your own forces include siege tanks and medivacs.

**Direction:**  
Increase your air presence and technology, while maintaining a strong ground core. Continue to expand and develop your economy.

**Read for details:** `N008`

---

### [DEFAULT] N009 — Midgame Air Transition with Ground Defense

**Trigger situation:**  
Around 540 seconds, the opponent has a ground-oriented macro posture with heavy production and technology, while your own forces include siege tanks, marines, and banshees.

**Direction:**  
Continue transitioning to an air-oriented composition, increasing your air presence and technology. Maintain a strong defensive posture to protect your economy.

**Read for details:** `N009`

---

### [DEFAULT] N010 — Early Game Tech Focus with Defensive Posture

**Trigger situation:**  
Around 180 seconds, both players have an unknown army posture, but with heavy technology investment. The opponent's production is moderate, while your own production is also moderate.

**Direction:**  
Focus on increasing your production and technology, while maintaining a defensive posture. Continue to expand your economy.

**Read for details:** `N010`

---
