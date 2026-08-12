# PvZ_O03 Technology / Economy / Expansion

## Skill Identity

- Skill ID: PvZ_O03
- Matchup: Protoss vs Zerg
- Opening Family: technology / economy / expansion opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Protoss opening that emphasizes heavy technology investment and economic expansion while keeping production moderate. The early game is flexible, with the option to transition into either a ground-oriented or air-oriented army based on scouting and opponent behavior.

Develop a technology / economy / expansion posture while preserving flexibility for live observation-driven adaptation.

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

## V5 Human-Trajectory / Runtime Bridge

- The phase policy below supplies the strategic target distilled from aggregate trajectory states; it is not an action sequence.
- The live router supplies exactly one current execution bottleneck. Resolve it without replacing the phase target with a generic macro rule.
- For Protoss, spend through completed powered compatible producers before adding capacity; preserve opening tempo and never force a new facility solely from a clock threshold.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Tech/Eco Development with Ground Baseline:** Prioritize economy and tech, maintain production, strengthen ground, keep air options open.
- **early_midgame — Ground Development with Safety Checks:** Strengthen ground, increase production and economy, maintain safety checks.
- **midgame — Ground Army Expansion with Tech Options:** Strengthen ground, consider tech units, maintain economy and production.
- **late_midgame — Ground Army Strengthening with Tech Additions:** Strengthen ground, consider tech units, maintain economy and expansion.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Avoid early army commitment

**When:** Early game, own economy and tech heavy, production moderate, opponent ground-based with light air.

**Mistake → correction:** Committing to a specific army composition before scouting the opponent's tech path, or neglecting defense while focusing on economy. → Continue developing economy and technology while maintaining flexibility. Strengthen ground forces as a baseline, but keep options open for air transition.

**Why:** Early game is about establishing a strong economic and technological foundation. Committing too early to a specific army composition can be punished by scouting and adaptation.

**Read for full checks:** `N001`

### L02 — Balance air commitment with ground defense

**When:** Early-midgame, own army air-oriented with Oracles, heavy production and tech, opponent ground-based with light air.

**Mistake → correction:** Over-committing to air while neglecting ground defense, or failing to adapt if the opponent shows anti-air. → Increase air presence and strengthen air forces. Continue developing technology and economy, but ensure ground defense is not neglected.

**Why:** Oracles provide harassment and scouting, and can transition into Phoenix or Void Ray compositions. Air can be strong against ground-based Zerg, but ground defense remains essential.

**Read for full checks:** `N007`

### L03 — Maintain balanced ground and air forces

**When:** Midgame, own army ground-oriented with Zealots and Void Rays, opponent ground-based with Zerglings, Mutalisks, Corruptors, and Queens.

**Mistake → correction:** Over-committing to Void Rays if the opponent has many Corruptors, or neglecting ground defense. → Strengthen ground forces and maintain Void Rays for anti-air. Continue developing technology and economy.

**Why:** Void Rays provide anti-air and can be effective against Corruptors. A balanced army can handle mixed compositions.

**Read for full checks:** `N010`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
