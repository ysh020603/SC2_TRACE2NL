# TvP_O07 Economy / Technology / Expansion

## Skill Identity

- Skill ID: TvP_O07
- Matchup: Terran vs Protoss
- Opening Family: economy / technology / expansion opening
- Method: Trajectory-Fusion Full V5

## Opening Strategy

A Terran opening that prioritizes a heavy economy, heavy technology investment, and early expansion while maintaining a ground-oriented army. The build is flexible and observation-driven, aiming to develop a strong macro position before committing to a specific army composition.

Develop a robust economy and technology base while preserving flexibility to adapt to the opponent's observed posture. Aim to reach a strong midgame position with multiple bases, high worker count, and access to key tech units.

This is a strategic template, not a fixed build order. Adapt based on live scouting and enemy intelligence.

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
- For Terran, use completed parents before scaling capacity, and order parent before add-on or dependent work; persistent bank plus low army favors executable unit throughput.
- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.

## V5 Phase Policy Index

Use only the policy for the current routed phase.

- **early_game — Early Ground Defense and Economy:** Develop economy and tech, strengthen ground, maintain defense, scout for tech.
- **early_midgame — Ground Macro with Heavy Tech:** Develop economy and tech, strengthen ground, add production, maintain defense, scout.
- **midgame — Ground Army with Air Transition:** Increase air, strengthen ground, add Medivacs, maintain economy.
- **late_midgame — Stabilization and Defense:** Stabilize, increase defense, maintain army, continue economy, add Medivacs.

## Contrastive Lessons

Use these mistake-to-correction pairs only when the live situation matches.

### L01 — Anti-Air Gap vs Void Rays

**When:** Midgame, around 420 seconds, with a heavy ground army and economy, and enemy scouting shows Zealots and Void Rays.

**Mistake → correction:** Sticking to a pure ground composition without anti-air, leaving your army vulnerable to Void Rays. → Maintain your ground army and continue expanding, but add anti-air units like Marines or Thors to counter potential Void Rays.

**Why:** Your ground army is strong, but Void Rays threaten it. Adding anti-air ensures you can handle mixed compositions.

**Read for full checks:** `N005`

### L02 — Insufficient Anti-Air vs Heavy Air

**When:** Midgame, around 480 seconds, with a heavy ground army and economy, and enemy scouting shows Zealots, Stalkers, Phoenixes, and Observers.

**Mistake → correction:** Continuing to strengthen ground forces without adding anti-air, leaving you unable to fight the enemy's air-heavy army. → Increase your anti-air capabilities by adding Thors, Vikings, or more Marines, while continuing to strengthen your ground army and maintain economy.

**Why:** The opponent's air army is strong, but your heavy economy allows a tech switch to support your ground with anti-air.

**Read for full checks:** `N008`

### L03 — Overreacting to Oracles

**When:** Early-midgame, around 300 seconds, with a heavy ground army and economy, and enemy scouting shows Zealots and Oracles.

**Mistake → correction:** Over-investing in anti-air or abandoning your ground army in response to Oracle harassment. → Maintain your ground army but start preparing anti-air by adding Marines and possibly Thors or Vikings, while continuing to expand and tech.

**Why:** Oracles can harass, but your economy is strong. Adding anti-air defends against air threats without sacrificing your ground core.

**Read for full checks:** `N006`

## Runtime-Routed Decision Nodes

The live platform exposes the unread node whose mined phase and trigger best match the current observation.
