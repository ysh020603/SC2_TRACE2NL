# ZvZ_O06 Expansion / Economy / Production

## Skill Identity

- Skill ID: ZvZ_O06
- Matchup: Zerg vs Zerg
- Opening Family: expansion / economy / production opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Zerg versus Zerg opening that prioritizes a heavy economy and expansion posture while maintaining moderate production and light technology investment. The early game focuses on establishing a strong economic base with Queens and Zerglings for safety, then transitions into a ground-oriented midgame with options to tech into air if the opponent commits to Mutalisks.

Develop a strong economy and production base while preserving flexibility to adapt to the opponent's tech choices. Aim to reach a heavy economy and production state by the midgame, with the option to transition into air if the opponent goes Mutalisk.

This is a strategic template, not a fixed build order. Adapt based on live scouting and opponent actions.

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

## V5 Human-Trajectory / Runtime Bridge

- The phase policy below supplies the strategic target distilled from aggregate trajectory states; it is not an action sequence.
- The live router supplies exactly one current execution bottleneck. Resolve it without replacing the phase target with a generic macro rule.
- For Zerg, production capacity is bases plus larva/inject throughput; Overlords and Drones consume the same larva as army, so do not translate facility-count rules from other races.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Early Game Economy and Safety:** Focus on economy and expansion, maintain ground army, light defense, produce Queens and Zerglings.
- **early_midgame — Early-Midgame Development:** Develop economy and production, maintain ground army, consider tech, light defense.
- **midgame — Midgame Ground Army Strengthening:** Strengthen ground army, continue economy and production, maintain defense, consider tech.
- **late_midgame — Late-Midgame Ground Dominance:** Strengthen ground army, maintain production, consider tech, strong defense.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Balance economy and tech with defense

**When:** Early-midgame, both players are on ground with moderate production and tech, and you have a strong economy.

**Mistake → correction:** Focusing solely on economy and neglecting army production, leaving you vulnerable to a sudden attack. → Continue developing economy and production, maintain a moderate ground army, and start teching up. Keep defense light but be ready to react to pressure.

**Why:** Teching early keeps you ahead, while a moderate army deters attacks and allows safe tech investment.

**Read for full checks:** `N002`

### L02 — Match opponent's heavy ground with tech and economy

**When:** Midgame, opponent has heavy ground (Zergling, Roach, Queen) with heavy production and tech; you have moderate ground (Zergling, Hydralisk, Queen) and moderate tech.

**Mistake → correction:** Over-investing in a single unit composition without scouting, risking a surprise switch to air or different ground. → Strengthen your ground army to match the opponent's composition, continue developing economy and production, and consider increasing technology for better units.

**Why:** A strong ground army defends and counters, while economy sustains it. Hydralisks counter Roaches, Zerglings provide mobility.

**Read for full checks:** `N003`

### L03 — Maintain ground strength and tech for efficiency

**When:** Late-midgame, both have heavy ground armies (Zergling, Roach, Queen) with heavy production and moderate tech.

**Mistake → correction:** Falling into a pure ground vs ground fight without considering composition advantage, risking inefficiency. → Continue strengthening your ground army, maintain heavy production, and consider increasing technology to get Roaches or Hydralisks. Keep defense strong.

**Why:** Adding Roaches gives durability, Hydralisks provide anti-air and damage. Heavy economy sustains a large army.

**Read for full checks:** `N004`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
